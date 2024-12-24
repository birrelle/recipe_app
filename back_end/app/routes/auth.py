from flask import Blueprint, Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, 
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies
)
from flask_cors import CORS
from app.crud import crud_users
# from bson import ObjectId
from datetime import timedelta
from app.utils import bcrypt
from app.schemas import User
import os
from dotenv import load_dotenv



# # Configuration
# app.config['MONGO_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/authdb')
# app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
# app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
# app.config['JWT_COOKIE_SECURE'] = True  # For HTTPS
# app.config['JWT_COOKIE_CSRF_PROTECT'] = True

# # Initialize extensions
# mongo = PyMongo(app)
# bcrypt = Bcrypt(app)
# jwt = JWTManager(app)
# CORS(app, supports_credentials=True)

# # Custom JSON encoder for MongoDB ObjectId
# class JSONEncoder(flask.json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return flask.json.JSONEncoder.default(self, o)
# app.json_encoder = JSONEncoder

auth_bp = Blueprint('auth', __name__)

# User Registration
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password']

    # Validate input
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    # Check if user already exists
    existing_user = crud_users.get_user_by_username(username=email)
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409

    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create new user
    user_data = {
        'username': email,
        'password': hashed_password,
    }
    user = User(**user_data)

    user_id = crud_users.create_user(user_data)

    return jsonify({
        'message': 'User registered successfully',
        'user_id': user_id
    })

# User Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    # Find user
    user = crud_users.get_user_by_username(username=email)
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    # Check password
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Create tokens
    access_token = create_access_token(identity=str(user.user_id))
    refresh_token = create_refresh_token(identity=str(user.user_id))

    # Create response with cookies
    response = jsonify({
        'message': 'Login successful',
        'user': {
            'id': str(user.user_id),
            'username': user.username
        }
    })
    
    # Set tokens in HTTP-only cookies
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response

# Token Refresh
@auth_bp.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    
    response = jsonify({'message': 'Token refreshed successfully'})
    set_access_cookies(response, new_access_token)
    
    return response

# Logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(response)
    return response

# Protected Route Example
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = crud_users.get_user_by_id(user_id=current_user_id)
    
    return jsonify({
        'message': 'Access granted',
        'user': {
            'id': str(user.user_id),
            'username': user.username
        }
    })

# Error Handlers
# @auth_bp.unauthorized_loader
# def unauthorized_response(callback):
#     return jsonify({
#         'message': 'Unauthorized',
#         'error': 'Missing or invalid token'
#     }), 401

# @auth_bp.invalid_token_loader
# def invalid_token_response(callback):
#     return jsonify({
#         'message': 'Unauthorized',
#         'error': 'Invalid token'
#     }), 401

# @auth_bp.expired_token_loader
# def expired_token_response(jwt_header, jwt_payload):
#     return jsonify({
#         'message': 'Token expired',
#         'error': 'Please log in again'
#     }), 401

