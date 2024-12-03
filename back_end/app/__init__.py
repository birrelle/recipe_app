from .crud import *
from .routes import recipes_bp, users_bp, collections_bp
from .database import *
from .schemas import *
from .utils import *
from config import config_by_name
from flask import Flask
from flask_cors import CORS
import os
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app(config_name="dev"):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    mongo.init_app(app)

    # Initialize the database
    # database.db.init_app(app)

    # Register blueprints
    app.register_blueprint(recipes_bp, url_prefix="/recipes")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(collections_bp, url_prefix="/collections")

    return app

# app = create_app()