from app.database.db import collections_collection
from pymongo.errors import PyMongoError
from typing import List
from app.schemas import Collection
from app.utils import PyObjectId
from bson import ObjectId

# CRUD Operations for Collections

# CREATE: Insert a new collection
def create_collection(collection_data: Collection) -> str:
    try:
        try:
            collection_data = Collection(**collection_data)
        except ValueError as e:
            print(f"Invalid Collection object")
            raise ValueError(e)

        collection_id = ObjectId()
        collection_data.collection_id = collection_id

        result = collections_collection.insert_one(collection_data.dict())
        if not result.inserted_id:
            raise Exception("Failed to insert collection", 500)


        return str(collection_id)

    except PyMongoError as e:
        print(f"MongoDB insertion error: {e}")
        raise PyMongoError("An error occurred while inserting the collection", 500)


# READ: Get a collection by ID
def get_collection_by_id(collections_id: str) -> Collection:
    try:
        if not PyObjectId.is_valid(collections_id):
            raise Exception("Invalid collection ID", 400)
        
        collection = collections_collection.find_one({"collection_id": PyObjectId(collections_id)})
        if not collection:
            raise Exception("Collection not found", 404)
        
        # collection["id"] = str(collection["id"])  # Convert PyObjectId to string for JSON serialization
        return Collection(**collection)

    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the collection", 500)
    
# READ: Get all collections for a given user
def get_all_collections_by_user(user_id: str) -> List[Collection]:
    try:
        if not PyObjectId.is_valid(user_id):
            raise Exception("Invalid user ID", 400)
        
        coll = get_all_collections()
        cursor = collections_collection.find({"user_id": PyObjectId(user_id)})

        collections = []
        for collection in list(cursor):
            # collection['id'] = str(collection['id'])
            # collection['user_id'] = str(collection['user_id'])
            collection = Collection(**collection)
            collections.append(collection)

        return collections
    
    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the collections", 500)
    
# READ: Get multiple collections by ID
def get_many_collections_by_id(collection_ids: List[str]) -> List[Collection]:
    try:
        object_ids = []
        for collection_id in collection_ids:
            if not PyObjectId.is_valid(collection_id):
                raise Exception("Invalid collection ID", 400)
            object_ids.append(PyObjectId(collection_id))
        
        cursor = collections_collection.find({"collection_id": {"$in": object_ids}})
        
        collections = []
        for collection in cursor:
            # collection['id'] = str(collection['id'])
            # collection['user_id'] = str(collection['user_id'])
            collection = Collection(**collection)
            collections.append(collection)
        
        return collections
    
    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the recipes", 500)

# READ: Get all collections
def get_all_collections() -> List[Collection]:
    try:
        cursor = collections_collection.find({})

        collections = []
        for collection in list(cursor):
            # collection['id'] = str(collection['id'])
            # collection['user_id'] = str(collection['user_id'])
            collection = Collection(**collection)
            collections.append(collection)

        return collections
    
    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the collections", 500)

# UPDATE: Update a collection by ID
def update_collection(collection_id: str, updated_data: Collection):
    try:
        try:
            updated_data = Collection(**updated_data)
        except ValueError as e:
            print(f"Invalid Collection object")
            raise ValueError(e)
        
        if not PyObjectId.is_valid(collection_id):
            raise Exception("Invalid collection ID", 400)
        
        result = collections_collection.update_one(
            {"collection_id": PyObjectId(collection_id)},
            {"$set": updated_data.dict()}
        )
        if result.matched_count == 0:
            raise Exception("Collection not found", 404)
        
        return {"message": "Collection updated successfully"}

    except PyMongoError as e:
        print(f"MongoDB updating error: {e}")
        raise PyMongoError("An error occurred while updating the collection", 500)

# DELETE: Delete a collection by ID
def delete_collection(collection_id: str):
    try:
        if not PyObjectId.is_valid(collection_id):
            raise Exception("Invalid collection ID", 400)
        
        result = collections_collection.delete_one({"collection_id": PyObjectId(collection_id)})
        if result.deleted_count == 0:
            raise Exception("Collection not found", 404)
        
        return {"message": "Collection deleted successfully"}

    except PyMongoError as e:
        print(f"MongoDB deletion error: {e}")
        raise PyMongoError("An error occurred while deleting the collection", 500)

# DELETE: Delete all collections
def delete_all_collections():
    try:
        collections_collection.delete_many({})

        return {"message": "Collections deleted successfully"}

    except PyMongoError as e:
        print(f"MongoDB deletion error: {e}")
        raise PyMongoError("An error occurred while deleting the collections", 500)
