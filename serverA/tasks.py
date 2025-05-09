from datetime import datetime, timedelta
#from celery.schedules import crontab
from celery import Celery
from flask_mailman import EmailMessage

from factory import create_app,mail
from models import User, Quiz, Score, Badge

from celery.schedules import crontab
import csv
from io import StringIO
import os
import json 
import google.generativeai as genai
 # Load environment variables from .env

# Configure the Generative AI client
gemini_api_key = os.getenv("GOOGLE_API_KEY")
if not gemini_api_key:
    print("Warning: GOOGLE_API_KEY environment variable not set. AI features will be disabled.")
    # Handle this case appropriately - maybe disable the report generation
else:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.0-flash') 

def make_celery():
    app = create_app()
    
    celery = Celery(
        'tasks',
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0'
    )
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
            
    celery.conf.update(
        timezone='Asia/Kolkata',  # timezone
        enable_utc=True,
        task_track_started=True,  #task track
        result_expires=3600,  # Expiry 1 hour
    )

    celery.Task = ContextTask
    return celery

celery = make_celery()


# Tasks

#AI tasks

# --- AI Report Generation Function (keep as before) ---
@celery.task(name='tasks.generate_ai_report', bind=True, max_retries=3, ignore_result=True)
def generate_ai_report(self, quiz_title, questions_data, score_percentage):
    """Generates an AI report using Google Gemini."""
    if not model:  # Check if model is initialized
        print("AI Report generation skipped: Model not available.")
        return json.dumps({
            "summary": "AI analysis is currently unavailable.",
            "strengths": [],
            "weaknesses": [],
            "suggestions": ["Please review your answers manually."]
        })

    prompt = f"""
    Analyze the following quiz results and provide an insightful report in JSON format.
    The user attempted a quiz titled "{quiz_title}" and scored {score_percentage:.2f}%.

    Here's a breakdown of the questions, the user's selected options, and the correct options:
    """
    for item in questions_data:
        prompt += f"\n- Question: {item['question']}\n"
        prompt += f"  User's Answer: {item['selected_option']}\n"
        prompt += f"  Correct Answer: {item['correct_option']}\n"
        prompt += f"  Outcome: {'Correct' if item['selected_option'] == item['correct_option'] else 'Incorrect'}\n"

    prompt += """
    Based on this information, provide a JSON object with the following keys:
    - "summary": A brief overall summary of the user's performance (2-3 sentences).
    - "strengths": A list of topics or types of questions the user seems to understand well (based on correct answers). If none are obvious, provide an encouraging remark.
    - "weaknesses": A list of topics or types of questions where the user struggled (based on incorrect answers). Be constructive.
    - "suggestions": A list of actionable suggestions for improvement, possibly mentioning specific areas from the 'weaknesses'.

    Return ONLY the raw JSON with no markdown formatting, code blocks, or other text. Ensure the output is valid JSON.
    Also the response should have a conversational tone as if you are directly guiding the user from a mentor's perspective.
    """

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Remove markdown code block if present
        if response_text.startswith("```") and "```" in response_text[3:]:
            # Find the first code block
            start_pos = response_text.find("\n") + 1
            end_pos = response_text.rfind("```")
            # Extract just the JSON content
            json_text = response_text[start_pos:end_pos].strip()
        else:
            json_text = response_text
            
        # Attempt to parse the response to validate JSON
        parsed_report = json.loads(json_text)
        
        # Ensure the expected keys exist, even if empty lists/strings
        parsed_report.setdefault("summary", "AI analysis generated, but summary missing.")
        parsed_report.setdefault("strengths", [])
        parsed_report.setdefault("weaknesses", [])
        parsed_report.setdefault("suggestions", [])
        
        return json.dumps(parsed_report)  # Return the validated/parsed JSON string

    except json.JSONDecodeError as e:
        print(f"AI Warning: Response was not valid JSON: {response_text}")
        print(f"JSON parsing error: {e}")
        fallback_report = json.dumps({
            "summary": "AI analysis could not be parsed correctly.",
            "strengths": [],
            "weaknesses": [],
            "suggestions": ["Please review your answers manually."]
        })
        return fallback_report
    except Exception as e:
        print(f"Error generating AI report: {e}")
        error_report = json.dumps({
            "summary": f"An error occurred during AI analysis.",
            "strengths": [],
            "weaknesses": [],
            "suggestions": ["Please review your answers manually."]
        })
        return error_report



@celery.task(name='tasks.send_email', bind=True, max_retries=3,ignore_result=True)
def send_email(self, subject, recipient, body, attachments=None):
    """Send email using SMTP with retries"""
    try:
        with mail.get_connection(
            host= 'smtp.gmail.com',
            port= 587,
            username= 'mail.whiz.it@gmail.com',
            password= os.environ.get('MAIL_PASSWORD'),
            use_tls=    True,
            timeout=    50,
        ) as connection:
            msg = EmailMessage(
                subject=subject,                
                from_email='mail.whiz.it@gmail.com',
                to=[recipient],
                connection=connection,
                body=body
            )
            #if '<' in body and '>' in body:
            msg.content_subtype = "html"
            
            
            if attachments:
                for filename, content, mimetype in attachments:
                    msg.attach(filename, content, mimetype)
                    
            msg.send()
            
        return f"Email sent successfully to {recipient}"
    except ConnectionRefusedError as e:
        # exponential retyrs
        retry_in = 60 * (2 ** self.request.retries)  # 60s, 120s, 240s
        raise self.retry(exc=e, countdown=retry_in, max_retries=3)
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise e
    
# signup message  
@celery.task(name='tasks.signup_msg',ignore_result=True)
def signup_msg(user_id):
    
    user = User.query.get(user_id)
    if not user.email:
        return "User has no email"
    
    html_content = f"""
    <html>
        <body>
            <h2>Welcome to QuizApp,{user.full_name}!</h2>
            <p>Thank you for signing up.</p>
            <p>Start taking quizzes now!</p>
            <table role="presentation" style="margin: 20px 0;">
                <tr>
                    <td align="center">
                        <a href="http://127.0.0.1:5000" 
                        style="padding: 10px 20px; background-color: #64cf68; color: white; text-decoration: none; border: 4px solid white; border-radius:8rem;font-weight:bold; display: inline-block; font-size: 16px;">
                        Take a Quiz🡵</a>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """
    
    send_email.delay(
        subject="Welcome to QuizApp!",
        recipient=user.email,
        body=html_content
    )
    
    return "Welcome message sent successfully"


## NEW Tasks
@celery.task(name='tasks.send_daily_reminders',ignore_result=True)
def send_daily_reminders():
    """Send daily reminders to inactive users or users with new quizzes"""
    try:
        yesterday = datetime.now() - timedelta(days=1)
        users = User.query.all()
        
        for user in users:
            if not user.email:  # Skip users without email
                continue
                
            datetime_last = user.updated_at
            last_login = datetime_last.replace(tzinfo=None)
            
            if last_login < yesterday:
                new_quizzes = Quiz.query.filter(
                    Quiz.created_at > last_login
                ).all()
                
                if new_quizzes:
                    html_content = f"""
                    <h2>New Quizzes Available!</h2>
                    <p>Hello {user.full_name},</p>
                    <p>There are {len(new_quizzes)} new quizzes available.</p>
                    <p>Login to attempt them!</p>
                    """
                    
                    #send_email.delay(
                       # subject="New Quizzes Available!",
                      #  recipient=user.email,
                       # body=html_content
                    #)
                    # Use the existing send_email task instead of implementing email sending here
                    send_email.delay(
                        subject="New Quizzes Available!",
                        recipient=user.email,
                        body=html_content
                    )
                    
                else:   
                    html_content = f"""
                    <h2>Don't Miss Out!</h2>
                    <p>Hello {user.full_name},</p>
                    <p>It's been a while since you last logged in.</p>
                    <p>Don't miss out on new quizzes!</p>
                    """
                    
                    send_email.delay(
                        subject="Don't Miss Out!",
                        recipient=user.email,
                        body=html_content
                    )
        
        return "Daily reminders sent successfully"
    except Exception as e:
        print(f"Error in daily reminders: {str(e)}")
        raise e

@celery.task(name='tasks.send_monthly_report',ignore_result=True)
def send_monthly_report():
    """Generate and send monthly activity reports"""
    try:
        today = datetime.now()
        #first_of_month = today.replace(day=1)
        #last_month_end = first_of_month - timedelta(days=1)
        #last_month_start = last_month_end.replace(day=1)
        last_month_start = today - timedelta(days=30)
        users = User.query.all()
        
        for user in users:
            if not user.email:  # Skip users without email
                continue
                
            '''monthly_scores = Score.query.filter(
                Score.user_id == user.id,
                Score.created_at.between(last_month_start, last_month_end)
            ).all()'''
            monthly_scores = Score.query.filter(
                Score.user_id == user.id,
                Score.created_at > last_month_start
            ).all()
            print(monthly_scores)
            if monthly_scores:
                total_quizzes = len(monthly_scores)
                avg_score = sum(score.total_score for score in monthly_scores) / total_quizzes
                
                html_content = f"""
                <h2>Monthly Activity Report - {last_month_start.strftime('%B %Y')}</h2>
                <p>Dear {user.full_name},</p>
                <h3>Your Monthly Statistics:</h3>
                <ul>
                    <li>Total Quizzes Taken: {total_quizzes}</li>
                    <li>Average Score: {avg_score:.2f}%</li>
                </ul>
                <h3>Quiz Details:</h3>
                <table border="1">
                    <tr><th>Quiz Id</th><th>Score</th><th>Date</th></tr>
                    {"".join(
                        f"<tr><td>{score.quiz_id}</td>"
                        f"<td>{score.total_score}%</td>"
                        f"<td>{score.created_at.strftime('%Y-%m-%d')}</td></tr>"
                        for score in monthly_scores
                    )}
                </table>
                """
                
                send_email.delay(
                    subject=f"Monthly Activity Report - {last_month_start.strftime('%B %Y')}",
                    recipient=user.email,
                    body=html_content
                )
        
        return "Monthly reports sent successfully"
    except Exception as e:
        print(f"Error in monthly reports: {str(e)}")
        raise e

# user history export mailed
@celery.task(name='tasks.generate_quiz_csv',ignore_result=True)
def generate_quiz_csv(user_id):
    
    try:
        user = User.query.get(user_id)
        if not user or not user.email:
            raise ValueError("User not found or has no email")
            
        scores = Score.query.filter_by(user_id=user_id).all()
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Quiz ID', 'Chapter ID', 'Date', 'Score', 'Remarks'])
        
        for score in scores:
            writer.writerow([
                score.quiz_id,
                score.quiz.chapter_id,
                score.created_at.strftime('%Y-%m-%d'),
                score.total_score,
            ])
        
        csv_content = output.getvalue()
        output.close()
        
        send_email.delay(
            subject="Your Quiz History Export",
            recipient=user.email,
            body="<p>Please find attached your quiz history export.</p>",
            attachments=[('quiz_history.csv', csv_content, 'text/csv')]
        )
        
        return "CSV generated and sent successfully"
    except Exception as e:
        print(f"Error generating CSV: {str(e)}")
        raise e
    
# user trigg exprot
@celery.task(name='tasks.user_csv')
def user_csv(user_id):
    """Generate CSV export of user's quiz history"""
    try:
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
            
        scores = Score.query.filter_by(user_id=user_id).all()
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Quiz ID', 'Chapter ID', 'Date', 'Score', 'Remarks'])
        
        for score in scores:
            writer.writerow([
                score.quiz_id,
                score.quiz.chapter_id,
                score.created_at.strftime('%Y-%m-%d'),
                score.total_score,
            ])
        
        csv_content = output.getvalue()
        output.close()
        
      
        return csv_content
    except Exception as e:
        print(f"Error generating CSV: {str(e)}")
        raise e

        
    


# celery beats
 
'''
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(86400,send_daily_reminders.s(), name='add everyday')

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(2629800,send_monthly_report.s(), name='add everyday')
'''   
    
'''
celery.conf.beat_schedule = {
    'send_daily_reminders': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(hour=20, minute=00),
    },
    'send_monthly_report': {
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(0, 0, day_of_month='1'),  # First day of each month
    },
   
}
'''
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=18, minute=12),send_daily_reminders.s(), name='send_daily_reminders'
    )
    sender.add_periodic_task(
        crontab(20, 12, day_of_month='8'),send_monthly_report.s(), name='send_monthly_report'
    )
    #(min/h/doM/MoY/d) Crontab format

@celery.task
def test(arg):
    print(arg)

@celery.task(name='tasks.notify_badge_earned', ignore_result=True)
def notify_badge_earned(user_id, badge_id):
    user = User.query.get(user_id)
    badge = Badge.query.get(badge_id)
    if not user or not badge or not user.email:
        return "User or badge not found, or user has no email."
    html_content = f"""
    <html>
        <body>
            <h2>Congratulations, {user.full_name}!</h2>
            <p>You have earned a new badge: <b>{badge.name}</b>!</p>
            <p>Description: {badge.description or ''}</p>
            <p>Keep learning and exploring to earn more badges!</p>
        </body>
    </html>
    """
    send_email.delay(
        subject=f"You've earned a new badge: {badge.name}",
        recipient=user.email,
        body=html_content
    )
    return f"Badge notification sent to {user.email} for badge {badge.name}"
