from flask import Flask, request
from pymongo import MongoClient, ASCENDING
from flask_cors import CORS
from app.routes import auth_bp, recipes_bp, users_bp, collections_bp
import os
import sys
from pathlib import Path
from app import create_app
from dotenv import load_dotenv


# Load the environment variable for the Flask app
# Load the appropriate .env file
env = os.getenv("FLASK_ENV")
dotenv_file = f".env.{env}"
load_dotenv(dotenv_file)

# os.environ['FLASK_ENV'] = os.getenv('FLASK_ENV', 'testing')
app = create_app(env)

if __name__ == '__main__':
    # Run the Flask application
    app.run()
