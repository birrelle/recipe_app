from flask import Blueprint, jsonify, request
from app.crud import crud_collections
from pymongo.errors import PyMongoError
from app.schemas import CollectionsSchema

# Define a Blueprint for the 'collections' routes
collections_bp = Blueprint('collections', __name__)

# CREATE collection endpoint
@collections_bp.route('', methods=['POST'])
def create_new_collection():
    try:
        data = request.json
        collection = CollectionsSchema(**data)

        if not collection:
            raise Exception("Invalid input: No data provided", 400)

        collection_id = crud_collections.create_collection(collection)
        return jsonify({"id": collection_id, "message": "Collection created successfully"})

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# READ collection by ID endpoint
@collections_bp.route('/<collection_id>', methods=['GET'])
def get_collection(collection_id):
    try:
        collection = crud_collections.get_collection_by_id(collection_id)
        return jsonify(collection)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# UPDATE collection endpoint
@collections_bp.route('/<collection_id>', methods=['PUT'])
def update_existing_collection(collection_id):
    try:
        data = request.json
        collection = CollectionsSchema(**data)

        if not collection:
            raise Exception("Invalid input: No data provided", 400)

        response = crud_collections.update_collection(collection_id, collection)
        return jsonify(response)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# DELETE collection by ID endpoint
@collections_bp.route('/<collection_id>', methods=['DELETE'])
def delete_collection_by_id(collection_id):
    try:
        response = crud_collections.delete_collection(collection_id)
        return jsonify(response)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)