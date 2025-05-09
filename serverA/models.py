from flask_sqlalchemy import SQLAlchemy
#from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta
import jwt
from config import Config as cfg
JWT_SECRET_KEY = cfg.JWT_SECRET_KEY
JWT_EXPIRATION_DELTA = cfg.JWT_EXPIRATION_DELTA
import json

# Initialize database and bcrypt

db = SQLAlchemy()

# JWT secret key

# new way bbase
class DBase(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Region(DBase):
    __tablename__ = 'regions'
    
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    flag_emoji = db.Column(db.String(10), nullable=True)  # For displaying region flags
    subjects = db.relationship('Subject', backref='region', lazy=True)
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'flag_emoji': self.flag_emoji
        }

class User(DBase):
    __tablename__ = 'users'
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)    
    qualification = db.Column(db.String(120), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    role = db.Column(db.String(10), nullable=False, default='user')  # 'user' or 'admin'
    remember_token = db.Column(db.String(100), nullable=True)
    passport = db.relationship('UserPassport', backref='user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_jwt(self):
        payload = {
            'user_id': self.id,
            'role': self.role,
            'exp': datetime.now() + JWT_EXPIRATION_DELTA
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

    @staticmethod
    def decode_jwt(token):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token expired
        except jwt.InvalidTokenError:
            return None  # Invalid token

class Badge(db.Model):
    __tablename__ = 'badges'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(255), nullable=True)  # URL or emoji
    criteria = db.Column(db.Text, nullable=True)     # JSON or text description

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'criteria': self.criteria
        }

class UserPassport(DBase):
    __tablename__ = 'user_passports'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    regions_explored = db.Column(db.Text, nullable=True)  # JSON string of region IDs and exploration dates
    total_cultural_points = db.Column(db.Integer, default=0)
    badges_earned = db.Column(db.Text, nullable=True)  # JSON string of earned badge IDs
    
    def add_region_explored(self, region_id):
        regions = json.loads(self.regions_explored or '{}')
        regions[str(region_id)] = datetime.now().isoformat()
        self.regions_explored = json.dumps(regions)
        
    def add_badge(self, badge_id):
        badges = json.loads(self.badges_earned or '[]')
        if badge_id not in badges:
            badges.append(badge_id)
            self.badges_earned = json.dumps(badges)

    def get_badges(self):
        badge_ids = json.loads(self.badges_earned or '[]')
        return Badge.query.filter(Badge.id.in_(badge_ids)).all()

class Subject(DBase):
    __tablename__ = 'subjects'

    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=True)
    cultural_context = db.Column(db.Text, nullable=True)  # Additional cultural information
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade="all, delete-orphan")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'region': self.region.name if self.region else None,
            'cultural_context': self.cultural_context
        }
        
class Chapter(DBase):
    __tablename__ = 'chapters'

    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade="all, delete-orphan")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'subject': self.subject.name if self.subject else None
        }
class Quiz(DBase):
    __tablename__ = 'quizzes'

    title = db.Column(db.String(120), nullable=False)
    date_of_quiz = db.Column(db.DateTime, nullable=False)
    time_duration = db.Column(db.Interval, nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")
    scores = db.relationship('Score', backref='quiz', lazy=True, cascade="all, delete-orphan")
    release_at = db.Column(db.DateTime, nullable=True)

class Question(DBase):
    __tablename__ = 'questions'

    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(120), nullable=False)
    option2 = db.Column(db.String(120), nullable=False)
    option3 = db.Column(db.String(120), nullable=True)
    option4 = db.Column(db.String(120), nullable=True)
    correct_option = db.Column(db.Integer, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    cultural_context = db.Column(db.Text, nullable=True)  # Additional cultural information about the question
    difficulty_level = db.Column(db.Integer, default=1)  # 1-5 scale for cultural knowledge depth

class Score(DBase):
    __tablename__ = 'scores'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    timestamp_of_attempt = db.Column(db.DateTime, default=datetime.now)
    responses = db.Column(db.Text, nullable=False)
    total_score = db.Column(db.Float, nullable=False)
    ai_report = db.Column(db.Text, nullable=True)
   

def init_db(app):
    db.init_app(app)    
    with app.app_context():
        db.create_all()
        #  admin
        if not User.query.filter_by(role='admin').first():
            admin = User(
                email='admin@example.com',
                full_name='Administrator',
                role='admin'
            )
            admin.set_password('admin0')  # Admin password
            db.session.add(admin)

        # Default user
        if not User.query.filter_by(email='testuser@example.com').first():
            user = User(
                email='testuser@example.com',
                full_name='Test User',
                role='user'
            )
            user.set_password('testing')
            db.session.add(user)
            db.session.commit()
        else:
            user = User.query.filter_by(email='testuser@example.com').first()

        # Regions
        region_data = [
            {'name': 'Asia', 'description': 'Explore the rich cultures of Asia', 'flag_emoji': '🌏'},
            {'name': 'Europe', 'description': 'Discover European heritage', 'flag_emoji': '🌍'},
            {'name': 'Africa', 'description': 'Experience African traditions', 'flag_emoji': '🌍'},
            {'name': 'Americas', 'description': 'Learn about American cultures', 'flag_emoji': '🌎'},
            {'name': 'Oceania', 'description': 'Explore Pacific cultures', 'flag_emoji': '🌏'}
        ]
        regions = []
        for r in region_data:
            region = Region.query.filter_by(name=r['name']).first()
            if not region:
                region = Region(**r)
                db.session.add(region)
                db.session.commit()
            regions.append(region or Region.query.filter_by(name=r['name']).first())

        # Subjects
        subject_data = [
            {'name': 'Asian History', 'description': 'History of Asia', 'region': regions[0], 'cultural_context': 'Ancient civilizations, dynasties, and modern nations.'},
            {'name': 'European Art', 'description': 'Art in Europe', 'region': regions[1], 'cultural_context': 'Renaissance, Baroque, and Modern art.'},
            {'name': 'African Music', 'description': 'Music of Africa', 'region': regions[2], 'cultural_context': 'Traditional and contemporary African music.'},
            {'name': 'American Politics', 'description': 'Politics in the Americas', 'region': regions[3], 'cultural_context': 'Democracy, revolutions, and modern governance.'},
            {'name': 'Oceania Geography', 'description': 'Geography of Oceania', 'region': regions[4], 'cultural_context': 'Islands, cultures, and natural wonders.'}
        ]
        subjects = []
        for s in subject_data:
            subject = Subject.query.filter_by(name=s['name']).first()
            if not subject:
                subject = Subject(
                    name=s['name'],
                    description=s['description'],
                    region_id=s['region'].id,
                    cultural_context=s['cultural_context']
                )
                db.session.add(subject)
                db.session.commit()
            subjects.append(subject or Subject.query.filter_by(name=s['name']).first())

        # Chapters
        chapter_data = [
            {'name': 'Ancient Asia', 'description': 'Ancient Asian civilizations', 'subject': subjects[0]},
            {'name': 'Renaissance Art', 'description': 'European Renaissance', 'subject': subjects[1]},
            {'name': 'Drumming Traditions', 'description': 'African drumming', 'subject': subjects[2]},
            {'name': 'US Constitution', 'description': 'Founding documents', 'subject': subjects[3]},
            {'name': 'Pacific Islands', 'description': 'Geography of Pacific islands', 'subject': subjects[4]}
        ]
        chapters = []
        for c in chapter_data:
            chapter = Chapter.query.filter_by(name=c['name']).first()
            if not chapter:
                chapter = Chapter(
                    name=c['name'],
                    description=c['description'],
                    subject_id=c['subject'].id
                )
                db.session.add(chapter)
                db.session.commit()
            chapters.append(chapter or Chapter.query.filter_by(name=c['name']).first())

        # Quizzes
        quiz_data = [
            {'title': 'Quiz on Ancient Asia', 'date_of_quiz': datetime.now(), 'time_duration': timedelta(minutes=10), 'remarks': 'Test your knowledge!', 'chapter': chapters[0]},
            {'title': 'Quiz on Renaissance Art', 'date_of_quiz': datetime.now(), 'time_duration': timedelta(minutes=10), 'remarks': 'Test your knowledge!', 'chapter': chapters[1]},
            {'title': 'Quiz on African Drumming', 'date_of_quiz': datetime.now(), 'time_duration': timedelta(minutes=10), 'remarks': 'Test your knowledge!', 'chapter': chapters[2]},
            {'title': 'Quiz on US Constitution', 'date_of_quiz': datetime.now(), 'time_duration': timedelta(minutes=10), 'remarks': 'Test your knowledge!', 'chapter': chapters[3]},
            {'title': 'Quiz on Pacific Islands', 'date_of_quiz': datetime.now(), 'time_duration': timedelta(minutes=10), 'remarks': 'Test your knowledge!', 'chapter': chapters[4]}
        ]
        quizzes = []
        for q in quiz_data:
            quiz = Quiz.query.filter_by(title=q['title']).first()
            if not quiz:
                quiz = Quiz(
                    title=q['title'],
                    date_of_quiz=q['date_of_quiz'],
                    time_duration=q['time_duration'],
                    remarks=q['remarks'],
                    chapter_id=q['chapter'].id
                )
                db.session.add(quiz)
                db.session.commit()
            quizzes.append(quiz or Quiz.query.filter_by(title=q['title']).first())

        # Questions
        question_data = [
            {'question_statement': 'Which dynasty is known as the longest-ruling in Chinese history?', 'option1': 'Han', 'option2': 'Zhou', 'option3': 'Qin', 'option4': 'Tang', 'correct_option': 2, 'quiz': quizzes[0], 'cultural_context': 'The Zhou dynasty ruled for over 800 years.', 'difficulty_level': 2},
            {'question_statement': 'Who painted the Mona Lisa?', 'option1': 'Michelangelo', 'option2': 'Raphael', 'option3': 'Leonardo da Vinci', 'option4': 'Donatello', 'correct_option': 3, 'quiz': quizzes[1], 'cultural_context': 'Leonardo da Vinci was a Renaissance artist.', 'difficulty_level': 1},
            {'question_statement': 'Which instrument is central to West African drumming?', 'option1': 'Djembe', 'option2': 'Tabla', 'option3': 'Taiko', 'option4': 'Bongo', 'correct_option': 1, 'quiz': quizzes[2], 'cultural_context': 'The djembe is a traditional African drum.', 'difficulty_level': 1},
            {'question_statement': 'What year was the US Constitution signed?', 'option1': '1776', 'option2': '1787', 'option3': '1801', 'option4': '1812', 'correct_option': 2, 'quiz': quizzes[3], 'cultural_context': 'The US Constitution was signed in 1787.', 'difficulty_level': 2},
            {'question_statement': 'Which is the largest island in Oceania?', 'option1': 'Fiji', 'option2': 'New Zealand', 'option3': 'Papua New Guinea', 'option4': 'Australia', 'correct_option': 4, 'quiz': quizzes[4], 'cultural_context': 'Australia is the largest island and country in Oceania.', 'difficulty_level': 1}
        ]
        for q in question_data:
            if not Question.query.filter_by(question_statement=q['question_statement']).first():
                question = Question(
                    question_statement=q['question_statement'],
                    option1=q['option1'],
                    option2=q['option2'],
                    option3=q['option3'],
                    option4=q['option4'],
                    correct_option=q['correct_option'],
                    quiz_id=q['quiz'].id,
                    cultural_context=q['cultural_context'],
                    difficulty_level=q['difficulty_level']
                )
                db.session.add(question)
                db.session.commit()

        # Badges
        badge_data = [
            {'name': 'Explorer', 'description': 'Explore your first region', 'icon': '🧭', 'criteria': 'Explore 1 region'},
            {'name': 'Quiz Master', 'description': 'Score 90%+ in a quiz', 'icon': '🏅', 'criteria': 'Score 90% or more in any quiz'},
            {'name': 'Culture Guru', 'description': 'Earn 500 cultural points', 'icon': '🎓', 'criteria': 'Earn 500 cultural points'},
            {'name': 'Globetrotter', 'description': 'Explore all regions', 'icon': '🌐', 'criteria': 'Explore all regions'}
        ]
        badges = []
        for b in badge_data:
            badge = Badge.query.filter_by(name=b['name']).first()
            if not badge:
                badge = Badge(
                    name=b['name'],
                    description=b['description'],
                    icon=b['icon'],
                    criteria=b['criteria']
                )
                db.session.add(badge)
                db.session.commit()
            badges.append(badge or Badge.query.filter_by(name=b['name']).first())

        # User Passport for default user
        if user and not user.passport:
            passport = UserPassport(
                user_id=user.id,
                regions_explored=json.dumps({str(regions[0].id): datetime.now().isoformat()}),
                total_cultural_points=120,
                badges_earned=json.dumps([badges[0].id])
            )
            db.session.add(passport)
            db.session.commit()

