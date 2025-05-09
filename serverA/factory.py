from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_cors import CORS
from config import Config
from models import init_db
from flask_mailman import Mail
from werkzeug.middleware.proxy_fix import ProxyFix

jwt = JWTManager()
cache = Cache()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    init_db(app)
    jwt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    
    # Configure CORS
    CORS(app, 
         resources={r"/*": {"origins": app.config['CORS_ORIGINS']}},
         supports_credentials=True,
         allow_headers=app.config['CORS_HEADERS'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Add security headers middleware
    @app.after_request
    def add_security_headers(response):
        for header, value in app.config['SECURITY_HEADERS'].items():
            response.headers[header] = value
        return response
    
    # Add error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Add ProxyFix middleware
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    return app
