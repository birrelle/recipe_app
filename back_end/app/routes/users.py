from flask import Blueprint, jsonify, request
from app.crud import crud_users
from pymongo.errors import PyMongoError
from app.schemas import UserSchema

# Define a Blueprint for the 'users' routes
users_bp = Blueprint('users', __name__)

# CREATE user endpoint
@users_bp.route('', methods=['POST'])
def create_new_user():
    try:
        data = request.json
        user = UserSchema(**data)

        if not user:
            raise Exception("Invalid input: No data provided", 400)

        user_id = crud_users.create_user(user)
        return jsonify({"id": user_id, "message": "User created successfully"})

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# READ user by ID endpoint
@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = crud_users.get_user_by_id(user_id)
        return jsonify(user)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# UPDATE user endpoint
@users_bp.route('/<user_id>', methods=['PUT'])
def update_existing_user(user_id):
    try:
        data = request.json
        user = UserSchema(**data)

        if not user:
            raise Exception(f"Invalid input: No data provided", 400)

        response = crud_users.update_user(user_id, user)
        return jsonify(response)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# DELETE user by ID endpoint
@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    try:
        response = crud_users.delete_user(user_id)
        return jsonify(response)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)