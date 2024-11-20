from app.utils import SearchType
from app.database.db import recipes_collection
from pymongo.errors import PyMongoError
from typing import List
from app.schemas import Recipe
import re
from app.utils import PyObjectId
from bson import ObjectId

# CRUD Operations for Recipes
#HOW DO I CREATE INSTANCES OF DB

# CREATE: Insert a new recipe
def create_recipe(recipe: Recipe) -> str:
    try:
        try:
            recipe = Recipe(**recipe)
        except ValueError as e:
            print(f"Invalid Recipe object")
            raise ValueError(e)
        
        recipe = recipe.dict()
        recipe["course"] = list(recipe["course"])

        result = recipes_collection.insert_one(recipe)

        if not result.inserted_id:
            raise Exception("Failed to insert recipe", 500)

        return str(result.inserted_id)

    except PyMongoError as e:
        print(f"MongoDB insertion error: {e}")
        raise PyMongoError("An error occurred while inserting the recipe", 500)


# READ: Get a recipe by ID
def get_recipe_by_id(recipe_id: str) -> Recipe:
    try:
        if not PyObjectId.is_valid(recipe_id):
            raise Exception("Invalid recipe ID", 400)
    
        recipe = recipes_collection.find_one({"_id": PyObjectId(recipe_id)})
        if not recipe:
            raise Exception("Recipe not found", 404)

        # recipe["id"] = str(recipe["id"])  # Convert PyObjectId to string for JSON serialization
        return Recipe(**recipe)

    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the recipe", 500)
    
# READ: Get all recipes for a given user
def get_all_recipes_by_user(user_id: str) -> List[Recipe]:
    try:
        if not PyObjectId.is_valid(user_id):
            raise Exception("Invalid user ID", 400)
        
        cursor = recipes_collection.find({"user_id": PyObjectId(user_id)})
        
        recipes = []
        for recipe in cursor:
            # recipe['id'] = str(recipe['id'])
            # recipe['user_id'] = str(recipe['user_id'])
            recipe = Recipe(**recipe)
            recipes.append(recipe)
        
        return recipes
    
    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the recipes", 500)

# READ: Get multiple recipes by ID
def get_many_recipes_by_id(recipe_ids: List[str]) -> List[Recipe]:
    try:
        object_ids = []
        for recipe_id in recipe_ids:
            if not PyObjectId.is_valid(recipe_id):
                raise Exception("Invalid recipe ID", 400)
            object_ids.append(PyObjectId(recipe_id))
        
        cursor = recipes_collection.find({"_id": {"$in": object_ids}})
        
        recipes = []
        for recipe in cursor:
            # recipe['id'] = str(recipe['id'])
            # recipe['user_id'] = str(recipe['user_id'])
            recipe = Recipe(**recipe)
            recipes.append(recipe)
        
        return recipes
    
    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the recipes", 500)

# READ: Get all recipes in the collection
def get_all_recipes() -> List[Recipe]:
    try:
        cursor = recipes_collection.find({})

        if not cursor:
            return []

        recipes = []
        for recipe in cursor:
            # recipe['id'] = str(recipe['id'])
            # recipe['user_id'] = str(recipe['user_id'])
            recipe = Recipe(**recipe)

            recipes.append(recipe)

        return recipes
    
    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the recipes", 500)
    
# READ: Search recipes by name or ingredient
def search_recipes(
        search_term: str,
        search_type: SearchType,
        user_id: str
    ) -> List[Recipe]:
        
        pattern = f"{re.escape(search_term)}"
        
        search_field = ""
        if search_type == SearchType.RECIPE:
            search_field = "title"
        elif search_type == SearchType.INGREDIENT:
            search_field = "ingredients.name"
        
        query = {
            "user_id": PyObjectId(user_id),
            search_field: {
                "$regex": pattern,
                "$options": "i"
            }
        }
        
        cursor = recipes_collection.find(query)

        recipes = []
        for recipe in list(cursor):
            # recipe['id'] = str(recipe['id'])
            # recipe['user_id'] = str(recipe['user_id'])
            recipe = Recipe(**recipe)
            recipes.append(recipe)
            
        return recipes

# UPDATE: Update a recipe by ID
def update_recipe(recipe_id: str, updated_data: Recipe) -> str:
    try:
        try:
            updated_data = Recipe(**updated_data)
        except ValueError as e:
            print(f"Invalid Recipe object")
            raise ValueError(e)

        if not PyObjectId.is_valid(recipe_id):
            raise Exception("Invalid recipe ID", 400)

        result = recipes_collection.update_one(
            {"_id": PyObjectId(recipe_id)},
            {"$set": updated_data.dict()}
        )
        if result.matched_count == 0:
            raise Exception("Recipe not found", 404)
        
        return {"message": "Recipe updated successfully"}

    except PyMongoError as e:
        print(f"MongoDB updating error: {e}")
        raise PyMongoError("An error occurred while updating the recipe", 500)

# DELETE: Delete a recipe by ID
def delete_recipe(recipe_id: str):
    try:
        if not PyObjectId.is_valid(recipe_id):
            raise Exception("Invalid recipe ID", 400)

        result = recipes_collection.delete_one({"_id": PyObjectId(recipe_id)})
        if result.deleted_count == 0:
            raise Exception("Recipe not found", 404)

        return {"message": "Recipe deleted successfully"}

    except PyMongoError as e:
        print(f"MongoDB deletion error: {e}")
        raise PyMongoError("An error occurred while deleting the recipe", 500)

# DELETE: Delete all recipes
def delete_all_recipes():
    try:
        recipes_collection.delete_many({})

        return {"message": "Recipes deleted successfully"}

    except PyMongoError as e:
        print(f"MongoDB deletion error: {e}")
        raise PyMongoError("An error occurred while deleting the recipes", 500)
