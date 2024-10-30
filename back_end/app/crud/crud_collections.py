from app.schemas import PyObjectId
from app.database.db import collections_collection
from pymongo.errors import PyMongoError
from app.schemas import CollectionsSchema

# CRUD Operations for Collections

# CREATE: Insert a new collection
def create_collection(collection_data: CollectionsSchema) -> str:
    try:
        result = collections_collection.insert_one(collection_data.dict())
        if not result.inserted_id:
            raise Exception("Failed to insert collection", 500)


        return str(result.inserted_id)

    except PyMongoError as e:
        print(f"MongoDB insertion error: {e}")
        raise PyMongoError("An error occurred while inserting the collection", 500)


# READ: Get a collection by ID
def get_collection_by_id(collections_id: str) -> CollectionsSchema:
    try:
        if not PyObjectId.is_valid(collections_id):
            raise Exception("Invalid collection ID", 400)
        
        collection = collections_collection.find_one({"id": PyObjectId(collections_id)})
        if not collection:
            raise Exception("Collection not found", 404)
        
        collection["id"] = str(collection["id"])  # Convert ObjectId to string for JSON serialization
        return collection

    except PyMongoError as e:
        print(f"MongoDB retrieval error: {e}")
        raise PyMongoError("An error occurred while retrieving the collection", 500)

# UPDATE: Update a collection by ID
def update_collection(collection_id: str, updated_data: CollectionsSchema):
    try:
        if not PyObjectId.is_valid(collection_id):
            raise Exception("Invalid collection ID", 400)
        
        result = collections_collection.update_one(
            {"id": PyObjectId(collection_id)},
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
        
        result = collections_collection.delete_one({"id": PyObjectId(collection_id)})
        if result.deleted_count == 0:
            raise Exception("Collection not found", 404)
        
        return {"message": "Collection deleted successfully"}

    except PyMongoError as e:
        print(f"MongoDB deletion error: {e}")
        raise PyMongoError("An error occurred while deleting the collection", 500)
