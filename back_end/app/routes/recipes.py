from flask import Blueprint, jsonify, request
from app.crud import crud_recipes
from app.schemas import RecipesSchema
from pymongo.errors import PyMongoError

# Define a Blueprint for the 'recipes' routes
recipes_bp = Blueprint('recipes', __name__)

# CREATE recipe endpoint
@recipes_bp.route('', methods=['POST'])
def create_new_recipe():
    try:
        data = request.json
        recipe = RecipesSchema(**data)
        print("Recipe", recipe)

        if not recipe:
            raise Exception("Invalid input: No data provided", 400)

        recipe_id = crud_recipes.create_recipe(recipe)
        print("ID", recipe_id)

        return jsonify({"id": recipe_id, "message": "Recipe created successfully"})

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# READ recipe by ID endpoint
@recipes_bp.route('/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    try:
        recipe = crud_recipes.get_recipe_by_id(recipe_id)
        print("Recipe", recipe)

        return jsonify(recipe)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)
    
# get all recipes
#  page = int(request.args.get('page', 1))
#     limit = int(request.args.get('limit', 10))
#     tag = request.args.get('tag')
#     search = request.args.get('search')
    
#     recipes = await recipe_service.get_recipes(
#         page=page,
#         limit=limit,
#         tag=tag,
#         search=search
#     )
#     return jsonify([recipe.dict(by_alias=True) for recipe in recipes])

# UPDATE recipe endpoint
@recipes_bp.route('/<recipe_id>', methods=['PUT'])
def update_existing_recipe(recipe_id):
    try:
        data = request.json
        recipe = RecipesSchema(**data)
        if not recipe:
            raise Exception("Invalid input: No data provided", 400)

        response = crud_recipes.update_recipe(recipe_id, recipe)
        return jsonify(response)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)

# DELETE recipe by ID endpoint
@recipes_bp.route('/<recipe_id>', methods=['DELETE'])
def delete_recipe_by_id(recipe_id):
    try:
        response = crud_recipes.delete_recipe(recipe_id)
        return jsonify(response)

    except PyMongoError as e:
        print(f"Database error occurred: {str(e)}", 500)
        raise PyMongoError(f"Database error occurred: {str(e)}", 500)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", 500)
        raise Exception(f"An unexpected error occurred: {str(e)}", 500)
