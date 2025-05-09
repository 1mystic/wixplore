from factory import create_app, cache
from api import init_routes
from models import Region, User, UserPassport, db

app = create_app()
cache.init_app(app)
init_routes(app)
