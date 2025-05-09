from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quizmdb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '1mystic2')  # Use a more secure secret key in .env
    JWT_EXPIRATION_DELTA = False
    JWT_ACCESS_TOKEN_EXPIRES = False  # minutes

    # Redis and Celery
    REDIS_URL = 'redis://localhost:6379/0'
    CELERY_BROKER_URL ='redis://localhost:6379/0'
    CELERY_RESULT_BACKEND ='redis://localhost:6379/0'

    # Caching
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://localhost:6379/0'
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))  # 5 minutes default cache timeout

    # Mail
    MAIL_PORT = 587
    MAIL_USERNAME = 'mail.whiz.it@gmail.com'
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Should be set in .env
    MAIL_USE_TLS = True    
    MAIL_DEFAULT_SENDER = 'mail.whiz.it@gmail.com'
    MAIL_TIMEOUT = 30  # timeout sec
    MAIL_USE_SSL = False

    # CORS Configuration
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://localhost:5173',
        'http://127.0.0.1:5173'
    ]
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_HEADERS = [
        'Content-Type',
        'Authorization',
        'X-Requested-With',
        'Accept',
        'Origin'
    ]
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    CORS_EXPOSE_HEADERS = ['Content-Type', 'Authorization']

    # Security Headers
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': "default-src 'self'; connect-src 'self' http://localhost:5173;"
    }