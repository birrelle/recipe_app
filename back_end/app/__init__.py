from .crud import *
from .routes import auth_bp, recipes_bp, users_bp, collections_bp
from .database import *
from .schemas import *
from .utils import *
from config import config_by_name
from flask import Flask
from flask_cors import CORS
import os
from flask_pymongo import PyMongo
from app.utils import bcrypt, jwt_manager


mongo = PyMongo()

def create_app(config_name="dev"):
    app = Flask(__name__)
    
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000",  # React development server
                # "https://yourdomain.com",  # Production frontend domain
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": [
                "Content-Type", 
                "Authorization", 
                "Access-Control-Allow-Credentials"
            ],
            "supports_credentials": True
        }
    })
    app.config.from_object(config_by_name[config_name])
    mongo.init_app(app)
    jwt_manager.init_app(app) 
    bcrypt.init_app(app)

    # Initialize the database
    # database.db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(recipes_bp, url_prefix="/api/recipes")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(collections_bp, url_prefix="/api/collections")

    return app

# app = create_app()