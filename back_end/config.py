# import os
# from datetime import timedelta

# class Config:

#     SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
#     MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017')
#     DB_NAME = os.environ.get('DB_NAME', 'recipe_app')
#     JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-jwt-secret')
#     JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
#     UPLOAD_FOLDER = 'uploads'

import os

class Config:
    # SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DB_NAME=os.getenv('recipe_app_db')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    MONGODB_URI = os.getenv('TEST_MONGODB_URI', 'mongodb://localhost:27017/test_db')

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}