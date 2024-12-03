from flask import Blueprint, jsonify, request
from app.crud import crud_collections, crud_users
from pymongo.errors import PyMongoError
from app.schemas import Collection
from typing import List
from app.utils.enums import UpdateType

# Define a Blueprint for the 'collections' routes
collections_bp = Blueprint('collections', __name__)

# CREATE collection endpoint
@collections_bp.route('', methods=['POST'])
def create_new_collection():
    try:
        collection = request.json

        if not collection:
            raise Exception("Invalid input: No data provided", 400)

        collection_id = crud_collections.create_collection(collection_data=collection)

        try:
            crud_users.update_user_upon_item_creation(user_id=collection["user_id"], item_id=collection_id, update_type=UpdateType.COLLECTION)
        except Exception as e:
            print(f"Error updating user: {str(e)}", 500)
            raise Exception(f"Error updating user: {str(e)}", 500)

        print("collection_id", collection_id)
        return jsonify({"id": collection_id, "message": "Collection created successfully"})

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# READ collection by ID endpoint
@collections_bp.route('/<collection_id>', methods=['GET'])
def get_collection(collection_id: str):
    try:
        collection = crud_collections.get_collection_by_id(collections_id=collection_id)
        return collection.json()

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# READ all collections for a user
@collections_bp.route('/user/<user_id>', methods=['GET'])
def get_all_collections_for_user(user_id: str):
    try:
        collections = crud_collections.get_all_collections_by_user(user_id=user_id)
        return [collection.json() for collection in collections]
    
    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# READ all collections
@collections_bp.route('/all', methods=['GET'])
def get_all_collections():
    try:
        collections = crud_collections.get_all_collections()

        return [collection.json() for collection in collections]
    
    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# UPDATE collection endpoint
@collections_bp.route('/<collection_id>', methods=['PUT'])
def update_existing_collection(collection_id: str):
    try:
        collection = request.json
        if not collection:
            raise Exception("Invalid input: No data provided", 400)

        response = crud_collections.update_collection(collection_id=collection_id, updated_data=collection)
        return jsonify(response)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# UPDATE add recipe to collection endpoint
@collections_bp.route('/<collection_id>/add_recipes', methods=['PUT'])
def add_recipes_to_collection(collection_id: str, recipe_ids: List[str]):
    try:
        collection = crud_collections.get_collection_by_id(collections_id=collection_id)
        
        recipe_id_list = collection.recipe_ids
        for recipe_id in recipe_ids:
            if recipe_id not in recipe_id_list:
                recipe_id_list.append(recipe_id)

        collection.recipe_ids = recipe_id_list

        response = crud_collections.update_collection(collection_id=collection_id, collection=collection)
        return jsonify(response)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# DELETE collection by ID endpoint
@collections_bp.route('/<collection_id>', methods=['DELETE'])
def delete_collection_by_id(collection_id: str):
    try:
        response = crud_collections.delete_collection(collection_id=collection_id)
        return jsonify(response)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)