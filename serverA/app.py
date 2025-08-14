from flask import Flask
from flask_cors import CORS
from config import Config
from models import db

def create_app():
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(Config)
	db.init_app(app)
	CORS(app, origins=[Config.FRONTEND_ORIGIN], supports_credentials=True)

	# Register blueprints
	from routes.quiz import quiz_bp
	from routes.upload import upload_bp
	from routes.agents import agents_bp
	app.register_blueprint(quiz_bp, url_prefix='/api/quiz')
	app.register_blueprint(upload_bp, url_prefix='/api/upload')
	app.register_blueprint(agents_bp, url_prefix='/api/agents')

	return app

if __name__ == "__main__":
	app = create_app()
	app.run(debug=True)
    
app = create_app()
cache.init_app(app)
init_routes(app)
app = create_app()
cache.init_app(app)
init_routes(app)
