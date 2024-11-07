from app.database.db import users_collection
from pymongo.errors import PyMongoError
from app.schemas import User
from typing import List
from app.utils import PyObjectId

# CRUD Operations for Users

# CREATE: Insert a new user
def create_user(user_data: User) -> str:
    try:
        result = users_collection.insert_one(user_data.dict())
        if not result.inserted_id:
            raise Exception("Failed to insert user", 500)

        return str(result.inserted_id)

    except PyMongoError as e:
        print(f"MongoDB insertion error: {e}")
        raise PyMongoError("An error occurred while inserting the recipe", 500)


# READ: Get a user by ID
def get_user_by_id(user_id: str) -> User:
    try:
        if not PyObjectId.is_valid(user_id):
            raise Exception("Invalid user ID", 400)
        
        user = users_collection.find_one({"id": PyObjectId(user_id)})
        if not user:
            raise Exception("User not found", 404)
        
        user["id"] = str(user["id"])  # Convert ObjectId to string for JSON serialization
        return user

    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the recipe", 500)

# READ: Get all users
def get_all_users() -> List[User]:
    try:
        users = users_collection.find({})

        if not users:
            return []

        for user in users:
            user['id'] = str(user['id'])
            user = User(**user)

        return users
    
    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the collections", 500)

# UPDATE: Update a user by ID
def update_user(user_id: str, updated_data: User):
    try:
        if not PyObjectId.is_valid(user_id):
            raise Exception("Invalid user ID", 400)

        result = users_collection.update_one(
            {"id": PyObjectId(user_id)},
            {"$set": updated_data.dict()}
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
        
        result = users_collection.delete_one({"id": PyObjectId(user_id)})
        if result.deleted_count == 0:
            raise Exception("User not found", 404)
        
        return {"message": "User deleted successfully"}

    except PyMongoError as e:
        print(f"MongoDB deletion error: {e}")
        raise PyMongoError("An error occurred while deleting the recipe", 500)
