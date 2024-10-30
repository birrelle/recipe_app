from app.database.db import recipes_collection
from pymongo.errors import PyMongoError
from typing import List
from app.schemas import RecipesSchema
from app.schemas import PyObjectId

# CRUD Operations for Recipes
#HOW DO I CREATE INSTANCES OF DB

# CREATE: Insert a new recipe
def create_recipe(recipe_data: RecipesSchema) -> str:
    try:
        recipe = recipe_data.dict()
        recipe["course"] = list(recipe["course"])

        result = recipes_collection.insert_one(recipe)
        if not result.inserted_id:
            raise Exception("Failed to insert recipe", 500)

        return str(result.inserted_id)

    except PyMongoError as e:
        print(f"MongoDB insertion error: {e}")
        raise PyMongoError("An error occurred while inserting the recipe", 500)


# READ: Get a recipe by ID
def get_recipe_by_id(recipe_id: str) -> RecipesSchema:
    try:
        if not PyObjectId.is_valid(recipe_id):
            raise Exception("Invalid recipe ID", 400)

        recipe = recipes_collection.find_one({"id": PyObjectId(recipe_id)})
        if not recipe:
            raise Exception("Recipe not found", 404)

        recipe["id"] = str(recipe["id"])  # Convert ObjectId to string for JSON serialization
        return RecipesSchema(**recipe)

    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the recipe", 500)

# READ: Get all recipes in the collection
def get_all_recipes() -> List[RecipesSchema]:
    try:
        recipes = recipes_collection.find({})
        
        for recipe in recipes:
            recipe["id"] = str(recipe["id"])
        return recipes
    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the recipes", 500)

# READ: Get all recipes associated with one user
def get_recipes_by_user_id(user_id: str) -> List[RecipesSchema]:
    try:
        if not PyObjectId.is_valid(user_id):
            raise Exception("Invalid user ID", 400)
        
        recipes = recipes_collection.fin

# UPDATE: Update a recipe by ID
def update_recipe(recipe_id: str, updated_data: RecipesSchema):
    try:
        if not PyObjectId.is_valid(recipe_id):
            raise Exception("Invalid recipe ID", 400)

        result = recipes_collection.update_one(
            {"id": PyObjectId(recipe_id)},
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

        result = recipes_collection.delete_one({"id": PyObjectId(recipe_id)})
        if result.deleted_count == 0:
            raise Exception("Recipe not found", 404)

        return {"message": "Recipe deleted successfully"}

    except PyMongoError as e:
        print(f"MongoDB deletion error: {e}")
        raise PyMongoError("An error occurred while deleting the recipe", 500)
