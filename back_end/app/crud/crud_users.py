from app.database.db import users_collection
from pymongo.errors import PyMongoError
from app.schemas import User
from typing import List
from app.utils import PyObjectId
from app.utils.enums import UpdateType
from bson import ObjectId

# CRUD Operations for Users

# CREATE: Insert a new user
def create_user(user_data: User) -> str:
    try:
        try:
            user_data = User(**user_data)
        except ValueError as e:
            print(f"Invalid User object")
            raise ValueError(e)
        
        user_id = ObjectId()
        user_data.user_id = user_id
        
        result = users_collection.insert_one(user_data.dict())
        if not result.inserted_id:
            raise Exception("Failed to insert user", 500)

        return str(user_id)

    except PyMongoError as e:
        print(f"MongoDB insertion error: {e}")
        raise PyMongoError("An error occurred while inserting the recipe", 500)


# READ: Get a user by ID
def get_user_by_id(user_id: str) -> User:
    try:
        if not PyObjectId.is_valid(user_id):
            raise Exception("Invalid user ID", 400)
        
        user = users_collection.find_one({"user_id": PyObjectId(user_id)})
        if not user:
            raise Exception("User not found", 404)
        
        # user["id"] = str(user["id"])  # Convert PyObjectId to string for JSON serialization
        return User(**user)

    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the recipe", 500)
    
# READ: Get a user by username
def get_user_by_username(username: str) -> User:
    try:        
        user = users_collection.find_one({"username": username})
        if not user:
            return None
        
        return User(**user)

    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the recipe", 500)
    

# READ: Get all users
def get_all_users() -> List[User]:
    try:
        cursor = users_collection.find({})

        users = []
        for user in cursor:
            # user['id'] = str(user['id'])
            user = User(**user)
            users.append(user)

        return users
    
    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the users", 500)

# UPDATE: Update a user by ID
def update_user(user_id: str, updated_data: User):
    try:
        try:
            updated_data = User(**updated_data)
        except ValueError as e:
            print(f"Invalid User object")
            raise ValueError(e)
        
        if not PyObjectId.is_valid(user_id):
            raise Exception("Invalid user ID", 400)

        result = users_collection.update_one(
            {"user_id": PyObjectId(user_id)},
            {"$set": updated_data.dict()}
        )
        if result.matched_count == 0:
            raise Exception("User not found", 404)

        return {"message": "User updated successfully"}

    except PyMongoError as e:
        print(f"MongoDB updating error: {e}")
        raise PyMongoError("An error occurred while updating the recipe", 500)
    
# UPDATE: Update a user by ID
def update_user_upon_item_creation(user_id: str, item_id: str, update_type: UpdateType):
    try:
        if not PyObjectId.is_valid(user_id):
            raise Exception("Invalid user ID", 400)
        
        user = get_user_by_id(user_id=user_id)

        if not user:
            raise Exception("User not found", 404)
        
        if update_type == UpdateType.RECIPE:
            recipe_ids = user.recipe_ids
            if not recipe_ids:
                recipe_ids = [item_id]
            else:
                if item_id not in recipe_ids:
                    recipe_ids.append(item_id)

            user.recipe_ids = recipe_ids
        
        elif update_type == UpdateType.COLLECTION:
            collection_ids = user.collection_ids
            if not collection_ids:
                collection_ids = [item_id]
            else:
                if item_id not in collection_ids:
                    collection_ids.append(item_id)

            user.collection_ids = collection_ids
        
        result = users_collection.update_one(
            {"user_id": PyObjectId(user_id)},
            {"$set": user.dict()}
        )
        if result.matched_count == 0:
            raise Exception("User not found", 404)

        return {"message": "User updated successfully"}

    except PyMongoError as e:
        print(f"MongoDB updating error: {e}")
        raise PyMongoError("An error occurred while updating the recipe", 500)

# DELETE: Delete a user by ID
def delete_user(user_id: str):
    try:
        if not PyObjectId.is_valid(user_id):
            raise Exception("Invalid user ID", 400)
        
        result = users_collection.delete_one({"user_id": PyObjectId(user_id)})
        if result.deleted_count == 0:
            raise Exception("User not found", 404)
        
        return {"message": "User deleted successfully"}

    except PyMongoError as e:
        print(f"MongoDB deletion error: {e}")
        raise PyMongoError("An error occurred while deleting the recipe", 500)

# DELETE: Delete all users
def delete_all_users():
    try:
        users_collection.delete_many({})

        return {"message": "Users deleted successfully"}

    except PyMongoError as e:
        print(f"MongoDB deletion error: {e}")
        raise PyMongoError("An error occurred while deleting the users", 500)