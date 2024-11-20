from .crud import *
from .routes import recipes_bp, users_bp, collections_bp
from .database import *
from .schemas import *
from .utils import *
from config import config
from flask import Flask
from flask_cors import CORS
import os


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])

    # Initialize the database
    # database.db.init_app(app)

    # Register blueprints
    app.register_blueprint(recipes_bp, url_prefix="/recipes")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(collections_bp, url_prefix="/collections")

    return app

app = create_app(os.getenv('FLASK_ENV', 'default'))