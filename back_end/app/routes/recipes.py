from flask import Blueprint, jsonify, request
from app.crud import crud_recipes
from app.schemas import Recipe
from app.utils import SearchType
from pymongo.errors import PyMongoError

# Define a Blueprint for the 'recipes' routes
recipes_bp = Blueprint('recipes', __name__)

# CREATE recipe endpoint
@recipes_bp.route('', methods=['POST'])
def create_new_recipe():
    try:
        data = request.json
        recipe = Recipe(**data)
        print("Recipe", recipe)

        if not recipe:
            raise Exception("Invalid input: No data provided", 400)

        recipe: Recipe = crud_recipes.create_recipe(recipe=recipe)
        print("ID", recipe['id'])

        return jsonify({"id": recipe['id'], "message": "Recipe created successfully"})

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
        print("Recipe", recipe)

        return jsonify(recipe)

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
        print("Recipes", recipes)

        return jsonify(recipes)
    
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
        print("Recipes", recipes)

        return jsonify(recipes)
    
    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

    
# READ recipes with a recipe name given the user
@recipes_bp.route('/search>', methods=['GET'])
def search_recipes(user_id: str, search_type: SearchType, search_term: str):
    try:

        recipes = crud_recipes.search_recipes(user_id=user_id, search_type=search_type, search_term=search_term)
        print("Recipes", recipes)

        return jsonify(recipes)
    
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
        data = request.json
        recipe = Recipe(**data)
        if not recipe:
            raise Exception("Invalid input: No data provided", 400)

        response = crud_recipes.update_recipe(recipe_id=recipe_id, recipe=recipe)
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
