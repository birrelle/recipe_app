from app.database.db import users_collection
from pymongo.errors import PyMongoError
from app.schemas import User
from typing import List
from app.utils import PyObjectId

# CRUD Operations for Users

# CREATE: Insert a new user
def create_user(user_data: User) -> str:
    try:
        try:
            user_data = User(**user_data)
        except ValueError as e:
            print(f"Invalid User object")
            raise ValueError(e)
        
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
        
        user = users_collection.find_one({"_id": PyObjectId(user_id)})
        if not user:
            raise Exception("User not found", 404)
        
        # user["id"] = str(user["id"])  # Convert PyObjectId to string for JSON serialization
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
            {"_id": PyObjectId(user_id)},
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
        
        result = users_collection.delete_one({"_id": PyObjectId(user_id)})
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