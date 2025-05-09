from flask import request, g, jsonify, send_from_directory, render_template, send_file
import json
from datetime import timedelta
from dateutil import parser
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt_identity
from flask_jwt_extended import get_jwt_header, get_current_user,get_jwt,get_jti
from models import User,db,Chapter,Quiz,Question,Score,Subject,Region,UserPassport,Badge
from functools import wraps

from tasks import *
from celery.result import AsyncResult

from io import BytesIO

#from flask_caching import Cache

#cache = Cache()



import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv() # Load environment variables from .env

# Configure the Generative AI client
gemini_api_key = os.getenv("GOOGLE_API_KEY")
if not gemini_api_key:
    print("Warning: GOOGLE_API_KEY environment variable not set. AI features will be disabled.")
    # Handle this case appropriately - maybe disable the report generation
else:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.0-flash') 



from factory import cache

def init_routes(app): 
        
    expired_tokens = []
       
   
    # CUstom decoraters

    def admin_only(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            #check id user has role admin 
            user = User.query.get(current_user)
            #
            if user.role != 'admin':
                return jsonify(message='Admin only!'),403
            return fn(*args, **kwargs)
        return wrapper

    def jwt_valid_token(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            jwt_data = get_jwt()
            jti = jwt_data['jti']

            # Check  token in blacklist
            if jti in expired_tokens:  # later repace by db
                return jsonify(message="Token has been revoked"), 401
            
            return fn(*args, **kwargs)
        
        return wrapper



    @app.route('/api/send-notification', methods=['POST'])
    #@jwt_required()
    def send_notification():
        try:
            task = send_email.delay(
                subject="Test notification",
                recipient= "mozojoy4@gmail.com",
                body="This is a test notification"
            )
            return jsonify({
                "status": "success",
                "message": "Email task queued successfully",
                "task_id": str(task.id)
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Failed to queue email task: {str(e)}"
            }), 500


    @app.route('/api/export-quiz-history', methods=['POST'])
    @jwt_required()
    def export_quiz_history():
        try:
            current_user_id = get_jwt_identity()
            task = generate_quiz_csv.delay(current_user_id)
            return jsonify({
                'message': 'Export started. You will receive an email when it\'s ready.',
                'task_id': str(task.id)
            }), 202
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # user triggered csv export 
    @app.route('/api/export_csv', methods=['GET','POST'])
    @jwt_required()
    def export_csv():
        user_id = get_jwt_identity()
        task = user_csv.delay(user_id)
        result = task.get()  # Wait for the task to complete (adjust timeout as needed) timeout=60
        
        if result:
            return send_file(
                BytesIO(result.encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name='user_data.csv'
            )
        else:
            return {'error': 'Failed to generate CSV'}, 400
   
    #__________________________________________________________
    
    @app.route('/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        
        email = data.get('email', '')
        password = data.get('password', '')
        full_name = data.get('full_name', '')

        if User.query.filter_by(email=email).first():
            return jsonify(message="User already exists"), 400

        new_user = User(        
            email=email,
            full_name=full_name,
            role='user'
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=str(new_user.id),expires_delta=False)
        
        try :
            signup_msg.delay(new_user.id)
        except Exception as e:
            print(f"Error in sending email: {str(e)}")
            return jsonify(message="Error in sending email"), 500
        
        return jsonify(access_token=access_token, role=new_user.role), 201


    @app.route('/login', methods=['POST'])
    def login():
        remember_token = request.headers.get('token')
        if remember_token:
            user = User.query.filter_by(remember_token=remember_token).first()
            if user:
                access_token = remember_token
                return jsonify(access_token=access_token, role=user.role), 200
            
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')

        user = User.query.filter_by(email=email).first()
        
        if user and user.role == 'Blocked':
            return jsonify(message="User is blocked"), 403

        if user and user.check_password(password):
            access_token =  create_access_token(identity=str(user.id),expires_delta=False)
            user.remember_token = access_token
            db.session.commit()
            
            return jsonify(access_token=access_token, role=user.role,username = user.full_name), 200
        else:
            return jsonify(message="Invalid credentials"), 401

   


    @app.route('/logout', methods=['POST'])
    @jwt_required() 
    @jwt_valid_token
    def logout():
        try:
            #  user id from JWT token
            current_user_id = get_jwt_identity()
            
          
            user = User.query.get(current_user_id)
            if not user:
                return jsonify({'message': 'User not found'}), 404
            
            # Clear remember token
            user.remember_token = None
            db.session.commit()
            
            # Get current JWT token
            jti = get_jwt()['jti']
            
            # Add to blacklist
            expired_tokens.append(jti)
            
           
            db.session.commit()
            
            return jsonify({'message': 'Successfully logged out'}), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Logout failed', 'error': str(e)}), 500


    # api routes 
    @app.route('/api/subjects', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    
    def get_subjects():
        subj_data = Subject.query.all()
        subj_data = list(map(lambda x: x.serialize(), subj_data))
        return jsonify(subj_data)

    @app.route('/api/subjects', methods=['POST'])
    @jwt_required()
    @jwt_valid_token
    @admin_only
    def create_subject():
        new_subject_data = request.get_json()
        nname=str(new_subject_data.get('name'))
        print(nname)
        old_sub = Subject.query.filter_by(name=nname).first().name if Subject.query.filter_by(name=nname).first() else None
        
        
        if old_sub :
            if nname.lower() == old_sub.lower():
                return jsonify({'message': 'Subject already exists'}), 400
                
        new_subject = Subject(
            name=str(new_subject_data.get('name')),
            description=str(new_subject_data.get('description', ''))
        )
        db.session.add(new_subject)
        db.session.commit()
        return jsonify(new_subject.serialize()), 201

    @app.route('/api/subjects/<int:id>', methods=['PUT'])
    @jwt_required()
    @jwt_valid_token
    @admin_only
    def update_subject(id):
        
        updated_data = request.get_json()
        
        newname=str(updated_data.get('name'))        
        old_sub = Subject.query.filter_by(name=newname).first().name if Subject.query.filter_by(name=newname).first() else None
        
        
        if old_sub :
            if newname.lower() == old_sub.lower():
                return jsonify({'message': 'Subject already exists'}), 400
            
            
        subj = Subject.query.get(id)
        if not subj:
            return jsonify({'message': 'Subject not found'}), 404
        subj.name = updated_data['name']
        subj.description = updated_data['description']
        db.session.commit()
        return jsonify(subj.serialize())

    @app.route('/api/subjects/<int:id>', methods=['DELETE'])
    @jwt_required()
    @jwt_valid_token
    @admin_only
    def delete_subject(id):
        subj = Subject.query.get(id)
        if not subj:
            return jsonify({'message': 'Subject not found'}), 404
        db.session.delete(subj)
        db.session.commit()
        return jsonify(subj.serialize()), 204



    # Chapters 
    @app.route('/api/chapters', methods=['GET', 'POST'])
    @jwt_required()  
    @jwt_valid_token  
    def chapters():
        if request.method == 'GET':
            
            def get_chapters():
                subject_id = request.args.get('subject_id', type=int)
                chapters_query = Chapter.query
                if subject_id:
                    chapters_query = chapters_query.filter_by(subject_id=subject_id)
                chapters = chapters_query.all()
                chapters_data = []
                for chapter in chapters:
                    chapter_data = chapter.serialize()
                    chapter_data['subject_id'] = chapter.subject_id
                    chapters_data.append(chapter_data)
                return jsonify(chapters_data)
            return get_chapters()
            
        elif request.method == 'POST':
            @admin_only 
            def create_chapter():
                data = request.get_json()  
                subject = Subject.query.get(data.get('subject_id'))  
                if not subject:
                    return jsonify({'message': 'Subject not found'}), 404
                
                # Create new ch
                chapter = Chapter(
                    name=data['name'],
                    description=data.get('description', ''),
                    subject_id=subject.id
                )
                db.session.add(chapter)
                db.session.commit()
                
              
                return jsonify(chapter.serialize()), 201
            
            return create_chapter()

    # Single Chapter by id
    @app.route('/api/chapters/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    @jwt_required()
    @jwt_valid_token
    def chapter_operations(id):
        chapter = Chapter.query.get_or_404(id) 
        
        if request.method == 'GET':
            return jsonify(chapter.serialize())
        
        @admin_only  
        def handle_admin_ops():
            if request.method == 'PUT':
                data = request.get_json()
                chapter.name = data['name']
                chapter.description = data.get('description', '')
                if 'subject_id' in data:
                    subject = Subject.query.get(data['subject_id'])
                    if not subject:
                        return jsonify({'message': 'Subject not found'}), 404
                    chapter.subject_id = subject.id
                db.session.commit()
                return jsonify(chapter.serialize())
            
            elif request.method == 'DELETE':
                db.session.delete(chapter)
                db.session.commit()
                return '', 204
        
        return handle_admin_ops()

    # Quizzes  all quizzes || create a new one
    @app.route('/api/quizzes', methods=['GET', 'POST'])
    @jwt_required()
    @jwt_valid_token
    def quizzes():
        if request.method == 'GET':
            #@cache.cached(timeout=10, query_string=True)
            def get_quizzes():
                chapter_id = request.args.get('chapter_id', type=int)
                subject_id = request.args.get('subject_id', type=int)
                quizzes_query = Quiz.query
                if chapter_id:
                    quizzes_query = quizzes_query.filter_by(chapter_id=chapter_id)
                if subject_id:
                    quizzes_query = quizzes_query.join(Chapter).filter(Chapter.subject_id == subject_id)
                    
                quizzes = quizzes_query.all()
                
                return jsonify([{
                    'id': quiz.id,
                    'title': quiz.title,
                    'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d %H:%M'),
                    'time_duration': str(quiz.time_duration),
                    'remarks': quiz.remarks,
                    'chapter_id': quiz.chapter_id,
                    'question_count': len(quiz.questions),
                    'chapter_name': Chapter.query.get(quiz.chapter_id).name,
                    'subject_name': Subject.query.get(Chapter.query.get(quiz.chapter_id).subject_id).name,
                    'release_at': quiz.release_at.strftime('%Y-%m-%d %H:%M') if quiz.release_at else None
                } for quiz in quizzes])
                
            return get_quizzes()
        
        elif request.method == 'POST':
            @admin_only
            def create_quiz():
                data = request.get_json()
                chapter = Chapter.query.get(data.get('chapter_id'))
                if not chapter:
                    return jsonify({'message': 'Chapter not found'}), 404
                
                quiz = Quiz(
                    title=data['title'],
                    date_of_quiz = parser.isoparse(data['date_of_quiz']),
                    time_duration=timedelta(minutes=int(data['duration_minutes'])),
                    remarks=data.get('remarks', ''),
                    chapter_id=chapter.id,
                    release_at = parser.isoparse(data['release_at'] if 'release_at' in data else None)
                )
                db.session.add(quiz)
                db.session.commit()
                
                return jsonify({
                    'id': quiz.id,
                    'title': quiz.title,
                    'date_of_quiz': quiz.date_of_quiz.isoformat(),
                    'time_duration': str(quiz.time_duration),
                    'remarks': quiz.remarks,
                    'chapter_id': quiz.chapter_id,
                    'release_at': quiz.release_at.isoformat() if quiz.release_at else None
                }), 201
            
            return create_quiz()
        
    # Single Quiz - id
    @app.route('/api/quizzes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    @jwt_required()
    @jwt_valid_token
    def quiz_operations(id):
        quiz = Quiz.query.get_or_404(id)
        chapter_name = Chapter.query.get(quiz.chapter_id).name
        subject_name = Subject.query.get(Chapter.query.get(quiz.chapter_id).subject_id).name
        questions = Question.query.filter_by(quiz_id=quiz.id).all()
        if request.method == 'GET':
            return jsonify({
                'id': quiz.id,
                'title': quiz.title,
                'date_of_quiz': quiz.date_of_quiz.isoformat(),
                'time_duration': str(quiz.time_duration),
                'remarks': quiz.remarks,
                'chapter_id': quiz.chapter_id,
                'chapter_name': chapter_name,
                'subject_name': subject_name,
                'questions': [{
                    'id': q.id,
                    'question_statement': q.question_statement,
                    'options': [q.option1, q.option2, q.option3, q.option4],
                    #'correct_option': q.correct_option
                } for q in questions],
                'question_count': len(questions)
            })
        
        elif request.method == 'PUT':
            @admin_only
            def update_quiz():
                data = request.get_json()
                quiz.title = data['title']
                quiz.date_of_quiz = parser.isoparse(data['date_of_quiz'])
                quiz.time_duration = timedelta(minutes=int(data['duration_minutes']))
                quiz.remarks = data.get('remarks', '')
                if 'chapter_id' in data:
                    chapter = Chapter.query.get(data['chapter_id'])
                    if not chapter:
                        return jsonify({'message': 'Chapter not found'}), 404
                    quiz.chapter_id = chapter.id
                db.session.commit()
                return jsonify({
                    'id': quiz.id,
                    'title': quiz.title,
                    'date_of_quiz': quiz.date_of_quiz.isoformat(),
                    'time_duration': str(quiz.time_duration),
                    'remarks': quiz.remarks,
                    'chapter_id': quiz.chapter_id
                })
            
            return update_quiz()
        
        elif request.method == 'DELETE':
            @admin_only
            def delete_quiz():
                db.session.delete(quiz)
                db.session.commit()
                return '', 204
            
            return delete_quiz()
        

    # all questions for all quizzes
    @app.route('/api/questions', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    #@cache.cached(timeout=10, query_string=True)
    def all_questions():
        if request.method == 'GET':
            quiz_id = request.args.get('quiz_id', type=int)
            chapter_id = request.args.get('chapter_id', type=int)
            
            questions_query = Question.query
            if quiz_id:
                questions_query = questions_query.filter_by(quiz_id=quiz_id)
            if chapter_id:
                questions_query = questions_query.join(Quiz).filter(Quiz.chapter_id == chapter_id)
                
            questions = questions_query.all()
            
            return jsonify([{
                'id': q.id,
                'question_statement': q.question_statement,
                'options': [q.option1, q.option2, q.option3, q.option4],
                'correct_option': q.correct_option,
                'quiz_id': q.quiz_id,
                'chapter_id': q.quiz.chapter_id
            } for q in questions]), 200

    #add new question
    @app.route('/api/questions', methods=['POST'])
    @jwt_required()
    @jwt_valid_token
    @admin_only
    def create_question():
        data = request.get_json()
        question = Question(
            question_statement=data['question_statement'],
            option1=data['option1'],
            option2=data['option2'],
            option3=data['option3'],
            option4=data['option4'],
            correct_option=data['correct_option'],
            quiz_id=data['quiz_id']
        )
        db.session.add(question)
        db.session.commit()
        
        return jsonify({
            'id': question.id,
            'question_statement': question.question_statement,
            'option1': question.option1,
            'option2': question.option2,
            'option3': question.option3,
            'option4': question.option4,
            'correct_option': question.correct_option,
            'quiz_id': question.quiz_id
        }), 201
        

    @app.route('/api/questions/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    @jwt_required()
    @jwt_valid_token
    def question_operations(id):
        question = Question.query.get_or_404(id)
        
        if request.method == 'GET':
            return jsonify({
                'id': question.id,
                'question_statement': question.question_statement,
                'option1': question.option1,
                'option2': question.option2,
                'option3': question.option3,
                'option4': question.option4,
                'correct_option': question.correct_option,
                'quiz_id': question.quiz_id
            })  
            
        elif request.method == 'PUT':
            @admin_only
            def update_question():
                data = request.get_json()
                question.question_statement = data['question_statement']
                question.option1 = data['option1']
                question.option2 = data['option2']
                question.option3 = data.get('option3', '')
                question.option4 = data.get('option4', '')
                question.correct_option = data['correct_option']
                db.session.commit()
                return jsonify({
                    'id': question.id,
                    'question_statement': question.question_statement,
                    'option1': question.option1,
                    'option2': question.option2,
                    'option3': question.option3,
                    'option4': question.option4,
                    'correct_option': question.correct_option,
                    'quiz_id': question.quiz_id
                })
            
            return update_question()
        
        elif request.method == 'DELETE':
            @admin_only
            def delete_question():
                db.session.delete(question)
                db.session.commit()
                return '', 204
            
            return delete_question()

        

                
                
    # quiz specific questions
    @app.route('/api/quizzes/<int:quiz_id>/questions', methods=['GET', 'POST'])
    @jwt_required()
    @jwt_valid_token
    def ques(quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        
        if request.method == 'GET':
            questions_data = [{
                'id': q.id,
                'question_statement': q.question_statement,
                'option1': q.option1,
                'option2': q.option2,
                'option3': q.option3,
                'option4': q.option4,
            'correct_option': q.correct_option
            } for q in quiz.questions]
            return jsonify(questions_data)
        
        elif request.method == 'POST':
            @admin_only
            def create_ques():
                data = request.get_json()
                question = Question(
                    question_statement=data['question_statement'],
                    option1=data['option1'],
                    option2=data['option2'],
                    option3=data['option3'],
                    option4=data['option4'],
                    correct_option=data['correct_option'],
                    quiz_id=quiz.id
                )
                db.session.add(question)
                db.session.commit()
                
                return jsonify({
                    'id': question.id,
                    'question_statement': question.question_statement,
                    'option1': question.option1,
                    'option2': question.option2,
                    'option3': question.option3,
                    'option4': question.option4,
                    'correct_option': question.correct_option,
                    'quiz_id': question.quiz_id
                }), 201
            
            return create_question()
        
    @app.route('/api/quizzes/<int:quiz_id>/questions/<int:question_id>', methods=['GET', 'PUT', 'DELETE'])
    @jwt_required()
    @jwt_valid_token
    def ques_operations(quiz_id, question_id):
        question = Question.query.get_or_404(question_id)
        
        if request.method == 'GET':
            return jsonify({
                'id': question.id,
                'question_statement': question.question_statement,
                'option1': question.option1,
                'option2': question.option2,
                'option3': question.option3,
                'option4': question.option4,
                'correct_option': question.correct_option,
                'quiz_id': question.quiz_id
            })
            
        elif request.method == 'PUT':
            @admin_only
            def update_question():
                data = request.get_json()
                question.question_statement = data['question_statement']
                question.option1 = data['option1']
                question.option2 = data['option2']
                question.option3 = data.get('option3', '')
                question.option4 = data.get('option4', '')
                question.correct_option = data['correct_option']
                db.session.commit()
                return jsonify({
                    'id': question.id,
                    'question_statement': question.question_statement,
                    'option1': question.option1,
                    'option2': question.option2,
                    'option3': question.option3,
                    'option4': question.option4,
                    'correct_option': question.correct_option,
                    'quiz_id': question.quiz_id
                })
            
            return update_question()
        
        elif request.method == 'DELETE':
            @admin_only
            def delete_question():
                db.session.delete(question)
                db.session.commit()
                return '', 204
            
            return delete_question()
        
    # score history ai gen ai
    @app.route('/api/scores/<int:score_id>/full_report', methods=['GET'])
    @jwt_required()
    # @jwt_valid_token # Apply necessary auth
    def get_full_quiz_report(score_id):
        # --- Fetch the Score Record ---
        score = Score.query.filter_by(id=score_id).first()
        if not score:
            return jsonify({'message': 'Score record not found'}), 404

        # --- Authorization Check (Optional but Recommended) ---
        # current_user_id = get_jwt_identity()
        # if score.user_id != current_user_id:
        #     return jsonify({'message': 'Forbidden: You do not own this score record'}), 403

        # --- Fetch Associated Data ---
        quiz = Quiz.query.get(score.quiz_id)
        questions = Question.query.filter_by(quiz_id=score.quiz_id).order_by(Question.id).all() # Ensure consistent order
        user = User.query.get(score.user_id)

        if not quiz or not questions:
             return jsonify({'message': 'Associated quiz or question data not found'}), 404

        # --- Reconstruct Question History ---
        quiz_history = []
        try:
            # Use eval carefully or ideally store responses as JSON string in DB
            responses = eval(score.responses)
            if not isinstance(responses, list) or len(responses) != len(questions):
                 print(f"Warning: Response list length mismatch for score {score_id}")
                 # Handle mismatch - maybe pad with null or return error
                 # For simplicity here, we'll proceed but it might lead to index errors
                 # A more robust solution is needed if this happens often.
                 # Pad responses if shorter:
                 if len(responses) < len(questions):
                     responses.extend([None] * (len(questions) - len(responses)))


        except Exception as e:
            print(f"Error parsing responses for score {score_id}: {e}")
            # Return an error or default history
            return jsonify({'message': 'Error processing score responses data'}), 500

        for i, question in enumerate(questions):
             selected_option = responses[i] if i < len(responses) else "Error: Missing Response" # Safety check
             quiz_history.append({
                 'question': question.question_statement,
                 'selected_option': selected_option,
                 'correct_option': question.correct_option
             })

        # --- Parse the AI Report JSON ---
        ai_report_data = None
        if score.ai_report:
            try:
                ai_report_data = json.loads(score.ai_report)
            except json.JSONDecodeError:
                print(f"Error decoding AI report JSON for score {score_id}")
                # Provide a default/error structure if parsing fails
                ai_report_data = {
                    "summary": "Error retrieving AI analysis.",
                    "strengths": [], "weaknesses": [], "suggestions": []
                }
        else:
            # Provide a default structure if no report was stored
            ai_report_data = {
                "summary": "AI analysis was not generated or is unavailable.",
                "strengths": [], "weaknesses": [], "suggestions": []
            }


        # --- Construct the Final Response ---
        full_report = {
            'score_id': score.id,
            'quiz_title': quiz.title,
            'user': user.full_name if user else 'Unknown User',
            'score': score.total_score,
            'timestamp': score.timestamp_of_attempt.isoformat() if score.timestamp_of_attempt else None,
            'questions': quiz_history, # The detailed question breakdown
            'ai_report': ai_report_data # The parsed AI report object
        }

        return jsonify(full_report), 200

   

    @app.route('/api/quizzes/<int:score_id>/user/<string:user>/history', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    def get_quiz_history(score_id, user):
        
        user = User.query.filter_by(full_name=user).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        user_id = user.id
        score = Score.query.filter_by(id=score_id, user_id=user_id).first()
        if not score:
            return jsonify({'message': 'No score found for this quiz and user'}), 404
        quiz_id = score.quiz_id
        quiz = Quiz.query.get_or_404(quiz_id)
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        
        responses = eval(score.responses)  # Convert string representation of list back to list
        
        quiz_history = []
        for i, question in enumerate(questions):
            quiz_history.append({
                'question': question.question_statement,
                'selected_option': responses[i],
                'correct_option': question.correct_option
            })
        
        return jsonify({
            'quiz_title': quiz.title,
            'score': score.total_score,
            'timestamp': score.timestamp_of_attempt.isoformat(),
            'questions': quiz_history
        })
        
    @app.route('/api/quizzes/<int:quiz_id>/submit', methods=['POST'])
    @jwt_required()
    def submit_quiz(quiz_id):
        # --- Get Quiz and Request Data ---
        quiz = Quiz.query.get_or_404(quiz_id)
        data = request.get_json()
        answers = data.get('answers', {})

        # --- Get Questions and Calculate Score ---
        all_questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.id).all()
        total_questions = len(all_questions)
        if total_questions == 0:
            return jsonify({'message': 'Quiz has no questions'}), 400

        try:
            answers = {int(k): v for k, v in answers.items()}
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid format for answers key'}), 400

        correct_answers = 0
        response_list = []
        questions_for_ai = []
        cultural_points_earned = 0

        for q in all_questions:
            selected_option = answers.get(q.id)
            response_list.append(selected_option)
            is_correct = (q.correct_option == selected_option)
            if is_correct:
                correct_answers += 1
                # Add cultural points based on question difficulty
                cultural_points_earned += q.difficulty_level * 10
            questions_for_ai.append({
                'question': q.question_statement,
                'selected_option': selected_option if selected_option is not None else "Not Answered",
                'correct_option': q.correct_option,
            })

        score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        user_id = get_jwt_identity()

        # --- Generate AI Report ---
        ai_report_json_string = generate_ai_report(
            quiz_title=quiz.title,
            questions_data=questions_for_ai,
            score_percentage=score_percentage
        )

        # --- Update User's Passport ---
        user = User.query.get(user_id)
        if not user.passport:
            passport = UserPassport(user_id=user_id)
            db.session.add(passport)
            db.session.commit()
            user.passport = passport

        # Add cultural points
        user.passport.total_cultural_points += cultural_points_earned

        # Get the region ID from the quiz's chapter's subject
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id)
        if subject and subject.region_id:
            user.passport.add_region_explored(subject.region_id)

        # --- BADGE LOGIC ---
        # Quiz Master badge (score >= 90%)
        quiz_master_badge = Badge.query.filter_by(name='Quiz Master').first()
        if score_percentage >= 90 and quiz_master_badge:
            badges = json.loads(user.passport.badges_earned or '[]')
            if quiz_master_badge.id not in badges:
                user.passport.add_badge(quiz_master_badge.id)
                db.session.commit()
                notify_badge_earned.delay(user_id, quiz_master_badge.id)

        # Culture Guru badge (500+ cultural points)
        culture_guru_badge = Badge.query.filter_by(name='Culture Guru').first()
        if culture_guru_badge and user.passport.total_cultural_points >= 500:
            badges = json.loads(user.passport.badges_earned or '[]')
            if culture_guru_badge.id not in badges:
                user.passport.add_badge(culture_guru_badge.id)
                db.session.commit()
                notify_badge_earned.delay(user_id, culture_guru_badge.id)

        # Add badges based on performance
        if score_percentage >= 90:
            user.passport.add_badge("Cultural Master")
        elif score_percentage >= 80:
            user.passport.add_badge("Cultural Explorer")
        elif score_percentage >= 70:
            user.passport.add_badge("Cultural Learner")

        # --- Save Score and Report to Database ---
        quiz_score = Score(
            user_id=user_id,
            quiz_id=quiz.id,
            total_score=score_percentage,
            responses=str(response_list),
            ai_report=ai_report_json_string
        )
        db.session.add(quiz_score)
        db.session.commit()

        # --- Return Response ---
        return jsonify({
            'message': 'Quiz submitted successfully.',
            'score': score_percentage,
            'correct_answers': correct_answers,
            'total_questions': total_questions,
            'score_id': quiz_score.id,
            'cultural_points_earned': cultural_points_earned
        }), 201


    @app.route('/api/users/scores', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    #@cache.memoize(timeout=5)
    def get_user_scores():
        user_id = get_jwt_identity()
        scores = Score.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': score.id,
            'quiz_id': score.quiz_id,
            'user_id': score.user_id,
            'quiz_title': score.quiz.title,
            'responses' : score.responses,
            'score': score.total_score,
            'timestamp': score.timestamp_of_attempt.isoformat()
        } for score in scores])
    

    @app.route('/api/allusers/scores', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    #@cache.cached(timeout=6)
    def all_user_scores():
        user_id = get_jwt_identity()
        scores = Score.query.all()
        
        user_data = [{
            'quiz_id': score.quiz_id,
            'user_id': score.user_id,
            'quiz_title': score.quiz.title,
            'score': score.total_score,
            'timestamp': score.timestamp_of_attempt.isoformat(),
            'user_status': User.query.get(score.user_id).role == 'user'
        } for score in scores]       
        return jsonify(user_data)
        
        
    @app.route('/api/admin_dash', methods=['GET'])
    @jwt_required()       
    @jwt_valid_token
    @admin_only    
    #@cache.cached(timeout=10)
    def admin_dash_stat():
        user_count = User.query.filter(User.role != 'admin').count()
        
        quiz_count = Quiz.query.count()
        question_count = Question.query.count()
        score_count = Score.query.count()
        subjects = Subject.query.count()
        chapters = Chapter.query.count()
        return jsonify({
                'subjects': subjects,
            'chapters': chapters,
            'quiz_count': quiz_count,
            'question_count': question_count,
            'user_count': user_count
            
        })
        
    @app.route('/api/leaderboard', methods=['GET'])
    @cache.cached(timeout=120)
    def leaderboard():
        users = User.query.filter(User.role == 'user').all()
        
        leaderboard = [
            {
            'name': user.full_name,
            'score': round(sum(s.total_score for s in Score.query.filter_by(user_id=user.id).all()), 1)
            }
            for user in users
        ]
        
        # desc sort
        leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
        
        return jsonify(leaderboard)
        
    
    @app.route('/api/user/<usern>', methods=['GET'])   
    #@cache.cached(timeout=10)
    def get_user_profile(usern):
        
        user = User.query.filter_by(full_name=usern).first()
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        users = User.query.filter(User.role == 'user').all()
        
        leaderboard = [
            {
                'name': user.full_name,
                'score': sum(s.total_score for s in Score.query.filter_by(user_id=user.id).all())
            }
            for user in users
        ]

        # desc sort 
        leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        #user = User.query.get_or_404(uid)
        uid = user.id
        name = user.full_name
        email = user.email
        quiz_count = Score.query.filter_by(user_id=uid).count()
        quiz_attempted = [q.quiz_id for q in Score.query.filter_by(user_id=uid).all()]
        
        chapters_covered = Quiz.query.filter(Quiz.id.in_(quiz_attempted)).distinct(Quiz.chapter_id).count()
        subjects_covered = Chapter.query.filter(Chapter.id.in_([q.chapter_id for q in Quiz.query.filter(Quiz.id.in_(quiz_attempted)).all()])).distinct(Chapter.subject_id).count()
        score_list = [s.total_score for s in Score.query.filter_by(user_id=uid).all()]
        avg_score = sum(score_list) / len(score_list) if score_list else 0
        avg_score = round(avg_score, 1)
        best_score = max(score_list) if score_list else 0
        
        user_rank = next((i+1 for i, u in enumerate(leaderboard) if u['name'] == name), None)
        
        
        return jsonify({
            'name': name,
            'email': email,
            'quiz_count': quiz_count,
            'chapters_covered': chapters_covered,
            'subjects_covered': subjects_covered,
            'average_score': avg_score,
            'best_score': best_score,
            'user_rank': user_rank,
            'all_attempts': len(score_list),
            'total_chapters': Chapter.query.count(),
            'total_subjects': Subject.query.count(),
            'total_quizzes': Quiz.query.count()
        })
        
    @app.route('/api/user/<int:id>', methods=['GET']) 
    @jwt_required()
    @jwt_valid_token
    @admin_only
    def user_data_id(id):
        try :
            
            user = User.query.get_or_404(id)
            uid = user.id
            name = user.full_name
            email = user.email            
            score_list = [s.total_score for s in Score.query.filter_by(user_id=uid).all()]
            avg_score = sum(score_list) / len(score_list) if score_list else 0
            avg_score = round(avg_score, 1)
            best_score = max(score_list) if score_list else 0
            best_score = round(best_score, 1)
            status = user.role == 'user'
            
            return jsonify({
                'name': name,
                'email': email,                            
                'avg_score': avg_score,
                'best_score': best_score,
                'all_attempts': len(score_list),   
                'user_status': status         
            })   
        except Exception as e:
            return jsonify({'error': str(e)}), 500
         
    @app.route('/api/block_user/<int:id>/', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    @admin_only
    def block_user(id):
        try : 
            user = User.query.get(id)
            if not user:
                return jsonify({'message': 'User not found'}), 404
            user.role = "Blocked"
            db.session.commit()
            return jsonify({'message': 'User blocked'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    @app.route('/api/unblock_user/<int:id>/', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    @admin_only
    def unblock_user(id):
        try : 
            user = User.query.get(id)
            if not user:
                return jsonify({'message': 'User not found'}), 404
            user.role = "user"
            db.session.commit()
            return jsonify({'message': 'User unblocked'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
   
    
   
    # new ai report page end points
    @app.route('/api/user/performance-data', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    @cache.cached(timeout=60)
    def get_user_performance_data():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Get all scores for the user
        scores = Score.query.filter_by(user_id=user_id).all()
        
        if not scores:
            return jsonify({
                'user': {
                    'full_name': user.full_name,
                    'email': user.email
                },
                'message': 'No quiz attempts recorded.',
                'raw_data_for_ai': 'No quiz attempts recorded.'
            }), 200

        # Calculate overall performance metrics
        total_score = sum(score.total_score for score in scores)
        overall_average_score = total_score / len(scores) if scores else 0
        
        # Get unique quizzes attempted
        quiz_ids = set(score.quiz_id for score in scores)
        quizzes = Quiz.query.filter(Quiz.id.in_(quiz_ids)).all()
        
        # Get chapters and subjects covered
        chapter_ids = set(quiz.chapter_id for quiz in quizzes)
        chapters = Chapter.query.filter(Chapter.id.in_(chapter_ids)).all()
        
        subject_ids = set(chapter.subject_id for chapter in chapters)
        subjects = Subject.query.filter(Subject.id.in_(subject_ids)).all()
        
        # Calculate per-chapter performance
        chapter_performance = {}
        for chapter in chapters:
            chapter_quizzes = [quiz for quiz in quizzes if quiz.chapter_id == chapter.id]
            chapter_quiz_ids = [quiz.id for quiz in chapter_quizzes]
            chapter_scores = [score for score in scores if score.quiz_id in chapter_quiz_ids]
            
            if chapter_scores:
                avg_score = sum(score.total_score for score in chapter_scores) / len(chapter_scores)
                last_attempt = max(score.timestamp_of_attempt for score in chapter_scores)
                
                subject = next((s for s in subjects if s.id == chapter.subject_id), None)
                subject_name = subject.name if subject else "Unknown Subject"
                
                chapter_performance[chapter.id] = {
                    'chapter_id': chapter.id,
                    'chapter_name': chapter.name,
                    'subject_id': chapter.subject_id,
                    'subject_name': subject_name,
                    'average_score': avg_score,
                    'quizzes_taken': len(chapter_scores) if chapter_scores else 0,
                    'last_attempt': last_attempt.isoformat()
                }
        
        # Sort chapters by performance (weakest first)
        weakest_chapters = sorted(
            chapter_performance.values(),
            key=lambda x: x['average_score']
        )
        
        # Prepare raw data for AI analysis
        raw_data = f"""
        User: {user.full_name}
        Total Quiz Attempts: {len(scores)}
        Overall Average Score: {overall_average_score:.2f}%
        
        Chapter Performance:
        {', '.join(f"{chapter['chapter_name']} ({chapter['subject_name']}): {chapter['average_score']:.2f}% ({chapter['quizzes_taken']} attempts)" for chapter in chapter_performance.values())}
        
        Recent Scores:
        {', '.join(f"Quiz {score.quiz_id}: {score.total_score:.2f}%" for score in sorted(scores, key=lambda x: x.timestamp_of_attempt, reverse=True)[:5])}
        """
        
        # Prepare the response
        response_data = {
            'user': {
                'full_name': user.full_name,
                'email': user.email
            },
            'performance': {
                'quizzes_taken': len(scores),
                'overall_average_score': overall_average_score,
                'total_study_time_seconds': sum(score.total_score for score in scores) * 60, # Estimate study time
            },
            'breakdown': {
                'weakest_chapters': weakest_chapters[:5],  # Top 5 weakest chapters
            },
            'raw_data_for_ai': raw_data
        }
        
        return jsonify(response_data), 200

# Add another endpoint for AI insights
    @app.route('/api/user/ai-insights', methods=['POST'])
    @jwt_required()
    @jwt_valid_token
    @cache.cached(timeout=360)
    def get_user_ai_insights():
        data = request.get_json()
        performance_data = data.get('performance_data')
        
        if not performance_data:
            return jsonify({'error': 'No performance data provided'}), 400
        
        try:
            prompt = f"""
            You are an expert academic advisor and quiz performance analyst.
            Analyze the following user performance data from a quiz platform and generate a detailed, encouraging, and actionable report.

            <h2>The user's performance data is:</h2>
            --- START DATA ---
            {performance_data}
            --- END DATA ---

            <p>Based <b>only</b> on the data provided above, generate a specified and focused genuine report search web for links/sources to get better info 
            with the following sections using Markdown formatting:</p>

            <h2> Performance Summary</h2>
            <p>Provide a brief overview of the user's overall performance, mentioning the average score and number of quizzes taken. Maintain an encouraging tone.</p>

            <h2> Key Strengths</h2>
            <p>Identify 1-2 subject areas or chapter topics where the user demonstrates strong performance (higher average scores). Be specific. If performance is consistent or low everywhere, acknowledge that honestly but gently.</p>

            <h2> Areas for Improvement</h2>
            <p>Identify the top 2-3 subject areas or chapter topics where the user's scores are lowest. Clearly state these are opportunities for growth.</p>

            <h2> Actionable Suggestions & Strategies</h2>
            <p>Provide specific, actionable advice based on the weak areas identified. Suggest:</p>
            <ul>
                <li>Specific chapters/subjects to prioritize for review.</li>
                <li>Possible study techniques (e.g., "review notes for [Chapter X]", "try practice problems on [Subject Y]", "revisit the basics of [Topic Z]").</li>
                <li>Encourage consistent practice.</li>
                <li>DO NOT suggest external resources unless specifically asked or implied by the data (focus on improving within the platform's content).</li>
            </ul>

            <h2> Statistical Snapshot</h2>
            <p>Present a few key statistics clearly (e.g., Overall Average Score, Total Quizzes, Weakest Chapter Score, Strongest Chapter Score).</p>
            """
            
            response = model.generate_content(prompt)
            ai_content = response.text
            
            return jsonify({
                'content': ai_content
            }), 200
        except Exception as e:
            print(f"Error generating AI insights: {e}")
            return jsonify({
                'error': f"Failed to generate AI insights: {str(e)}"
            }), 500

    # New endpoints for Global Knowledge Weaver features
    
    @app.route('/api/regions', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    def get_regions():
        regions = Region.query.all()
        return jsonify([region.serialize() for region in regions])

    @app.route('/api/regions/<int:id>', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    def get_region(id):
        region = Region.query.get_or_404(id)
        return jsonify(region.serialize())

    @app.route('/api/regions', methods=['POST'])
    @jwt_required()
    @jwt_valid_token
    @admin_only
    def create_region():
        data = request.get_json()
        new_region = Region(
            name=data['name'],
            description=data.get('description'),
            flag_emoji=data.get('flag_emoji')
        )
        db.session.add(new_region)
        db.session.commit()
        return jsonify(new_region.serialize()), 201

    @app.route('/api/user/passport', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    def get_user_passport():
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user.passport:
            passport = UserPassport(user_id=current_user_id)
            db.session.add(passport)
            db.session.commit()
            user.passport = passport
        
        return jsonify({
            'regions_explored': json.loads(user.passport.regions_explored or '{}'),
            'total_cultural_points': user.passport.total_cultural_points,
            'badges_earned': json.loads(user.passport.badges_earned or '[]')
        })

    @app.route('/api/user/passport/explore-region/<int:region_id>', methods=['POST'])
    @jwt_required()
    @jwt_valid_token
    def explore_region(region_id):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user.passport:
            passport = UserPassport(user_id=current_user_id)
            db.session.add(passport)
            db.session.commit()
            user.passport = passport
        user.passport.add_region_explored(region_id)
        db.session.commit()

        # --- BADGE LOGIC ---
        # Explorer badge (first region)
        explorer_badge = Badge.query.filter_by(name='Explorer').first()
        regions = json.loads(user.passport.regions_explored or '{}')
        badges = json.loads(user.passport.badges_earned or '[]')
        if explorer_badge and len(regions) >= 1 and explorer_badge.id not in badges:
            user.passport.add_badge(explorer_badge.id)
            db.session.commit()
            notify_badge_earned.delay(current_user_id, explorer_badge.id)

        # Globetrotter badge (all regions)
        globetrotter_badge = Badge.query.filter_by(name='Globetrotter').first()
        all_region_ids = [str(r.id) for r in Region.query.all()]
        if globetrotter_badge and all(rid in regions for rid in all_region_ids) and globetrotter_badge.id not in badges:
            user.passport.add_badge(globetrotter_badge.id)
            db.session.commit()
            notify_badge_earned.delay(current_user_id, globetrotter_badge.id)

        return jsonify({'message': 'Region explored successfully'})

    @app.route('/api/user/passport/add-badge', methods=['POST'])
    @jwt_required()
    @jwt_valid_token
    def add_badge():
        current_user_id = get_jwt_identity()
        data = request.get_json()
        badge_id = data.get('badge_id')
        badge = Badge.query.get(badge_id)
        if not badge:
            return jsonify({'error': 'Badge not found'}), 404
        user = User.query.get(current_user_id)
        if not user.passport:
            passport = UserPassport(user_id=current_user_id)
            db.session.add(passport)
            db.session.commit()
            user.passport = passport
        user.passport.add_badge(badge_id)
        db.session.commit()
        # Trigger badge notification
        notify_badge_earned.delay(current_user_id, badge_id)
        return jsonify({'message': 'Badge added successfully'})

    @app.route('/api/subjects/by-region/<int:region_id>', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    def get_subjects_by_region(region_id):
        subjects = Subject.query.filter_by(region_id=region_id).all()
        return jsonify([subject.serialize() for subject in subjects])

    @app.route('/api/questions/<int:id>/cultural-context', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    def get_question_cultural_context(id):
        question = Question.query.get_or_404(id)
        return jsonify({
            'cultural_context': question.cultural_context,
            'difficulty_level': question.difficulty_level
        })

    # --- BADGE ENDPOINTS ---
    @app.route('/api/badges', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    def get_badges():
        badges = Badge.query.all()
        return jsonify([badge.serialize() for badge in badges])

    @app.route('/api/badges', methods=['POST'])
    @jwt_required()
    @jwt_valid_token
    @admin_only
    def create_badge():
        data = request.get_json()
        badge = Badge(
            name=data['name'],
            description=data.get('description'),
            icon=data.get('icon'),
            criteria=data.get('criteria')
        )
        db.session.add(badge)
        db.session.commit()
        return jsonify(badge.serialize()), 201

    @app.route('/api/user/badges', methods=['GET'])
    @jwt_required()
    @jwt_valid_token
    def get_user_badges():
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.passport:
            return jsonify([])
        badges = user.passport.get_badges()
        return jsonify([badge.serialize() for badge in badges])
        return jsonify([badge.serialize() for badge in badges])