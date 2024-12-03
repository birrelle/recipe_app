from flask import Blueprint, jsonify, request
from app.crud import crud_recipes, crud_users
from app.schemas import Recipe
from app.utils import SearchType, UpdateType
from pymongo.errors import PyMongoError
from typing import List
import json

# Define a Blueprint for the 'recipes' routes
recipes_bp = Blueprint('recipes', __name__)


# CREATE recipe endpoint
@recipes_bp.route('', methods=['POST'])
def create_new_recipe():
    try:
        recipe = request.json

        if not recipe:
            raise Exception("Invalid input: No data provided", 400)

        recipe_id = crud_recipes.create_recipe(recipe=recipe)
        
        try:
            crud_users.update_user_upon_item_creation(user_id=recipe["user_id"], item_id=recipe_id, update_type=UpdateType.RECIPE)
        except Exception as e:
            print(f"Error updating user: {str(e)}", 500)
            raise Exception(f"Error updating user: {str(e)}", 500)

        return jsonify({"id": recipe_id, "message": "Recipe created successfully"})

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# READ recipe by ID endpoint
@recipes_bp.route('/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id: str):
    try:
        recipe = crud_recipes.get_recipe_by_id(recipe_id=recipe_id)
        
        return recipe.json()

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)
    
# READ multiple recipes by ID endpoint
@recipes_bp.route('/many', methods=['GET'])
def get_many_recipes():
    try:
        recipe_ids = request.json
        recipes = crud_recipes.get_many_recipes_by_id(recipe_ids=recipe_ids)

        return [recipe.json() for recipe in recipes]

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)
    
# READ all recipes for a user
@recipes_bp.route('/user/<user_id>', methods=['GET'])
def get_all_recipes_for_user(user_id: str):
    try:
        recipes = crud_recipes.get_all_recipes_by_user(user_id=user_id)

        return [recipe.json() for recipe in recipes]
    
    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# READ all recipes
@recipes_bp.route('/all', methods=['GET'])
def get_all_recipes():
    try:
        recipes = crud_recipes.get_all_recipes()

        return [recipe.json() for recipe in recipes]
    
    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

    
# READ recipes with a recipe name given the user
@recipes_bp.route('/search', methods=['GET'])
def search_recipes():
    try:
        user_id = request.json['user_id']
        search_type = request.json['search_type']
        search_term = request.json['search_term']

        recipes = crud_recipes.search_recipes(user_id=user_id, search_type=search_type, search_term=search_term)

        return [recipe.json() for recipe in recipes]
    
    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)
    

# UPDATE recipe endpoint
@recipes_bp.route('/<recipe_id>', methods=['PUT'])
def update_existing_recipe(recipe_id: str):
    try:
        recipe = request.json
        if not recipe:
            raise Exception("Invalid input: No data provided", 400)

        response = crud_recipes.update_recipe(recipe_id=recipe_id, updated_data=recipe)
        return jsonify(response)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# DELETE recipe by ID endpoint
@recipes_bp.route('/<recipe_id>', methods=['DELETE'])
def delete_recipe_by_id(recipe_id: str):
    try:
        response = crud_recipes.delete_recipe(recipe_id=recipe_id)
        return jsonify(response)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)
