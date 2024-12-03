# test_crud_collections.py
from app.crud import crud_collections
import pytest
from flask import Flask
from config import TestingConfig
from app.utils import PyObjectId
from app.utils import enums

collection = {"name": "Favorites",
                "user_id": "673939ecbce83aa91d4e20ab",
                "recipe_ids": ["673939ecbce83aa91d4e20aa", "673939e155abdf31fbf15fef", "673939e155abdf31fbf15ff0"]}
collection_2 = {"name": "Thanksgiving",
                "user_id": "672af6cd3d7885e1b7eaf6d4",
                "recipe_ids": ["673939cf5a425b66cc8c3dd2", "672af6cd3d7885e1b7eaf6d4", "673939ba7cb7a2ab4a91f6fa"]}
bad_collection = {"name": "Fav dinners",
                "recipe_ids": ["673939cf5a425b66cc8c3dd2", "672af6cd3d7885e1b7eaf6d4", "673939ba7cb7a2ab4a91f6fa"]}
bad_collection_2 = {"user_id": "672af6cd3d7885e1b7eaf6d4",
                "recipe_ids": ["673939cf5a425b66cc8c3dd2", "672af6cd3d7885e1b7eaf6d4", "673939ba7cb7a2ab4a91f6fa"]}
updated_collection = {"name": "Favorite Desserts",
                "user_id": "673939ecbce83aa91d4e20ab",
                "recipe_ids": ["673939ecbce83aa91d4e20aa", "673939e155abdf31fbf15fef", "673939e155abdf31fbf15ff0"]}
        
def test_create_collection():
    # Test correct insertion
    response = crud_collections.create_collection(collection_data=collection)
    assert PyObjectId.is_valid(response)

def test_fail_create_collection():
    # Test error handling for missing required fields
    with pytest.raises(ValueError) as exc_info:
        crud_collections.create_collection(collection_data=bad_collection)

    assert "user_id" and "field required" in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        crud_collections.create_collection(collection_data=bad_collection_2)

    assert "name" and "field required" in str(exc_info.value)

def test_get_collection():
    # Test correct retrieval
    crud_collections.delete_all_collections()
    collection_id = crud_collections.create_collection(collection_data=collection)

    assert PyObjectId.is_valid(collection_id)
    
    response = crud_collections.get_collection_by_id(collections_id=collection_id)
    assert response.name == "Favorites"
    assert str(response.user_id) == "673939ecbce83aa91d4e20ab"
    

def test_fail_get_collection():
    # Test invalid retrieval
    crud_collections.delete_all_collections()
    collection_id = "672af6cd3d7885e1b7eaf6d4"

    with pytest.raises(Exception) as exc_info:
        crud_collections.get_collection_by_id(collections_id=collection_id)
    
    assert "Collection not found" in str(exc_info.value)

def test_get_collection_by_user():
    # Test correct retrieval by user
    crud_collections.delete_all_collections()
    crud_collections.create_collection(collection_data=collection)
    crud_collections.create_collection(collection_data=collection_2)

    response = crud_collections.get_all_collections_by_user(user_id="673939ecbce83aa91d4e20ab")

    assert len(response) == 1
    assert response[0].name == "Favorites"
    
def test_fail_get_collection_by_user():
    # Test invalid retrival by user
    crud_collections.delete_all_collections()
    crud_collections.create_collection(collection_data=collection)

    response = crud_collections.get_all_collections_by_user(user_id="6738eab60f9babcf62eea6df")
    assert len(response) == 0

def test_get_multiple_collections_by_id():
    # Test correct retrieval of all collections
    crud_collections.delete_all_collections()
    collection_id_1 = crud_collections.create_collection(collection_data=collection)
    collection_id_2 = crud_collections.create_collection(collection_data=updated_collection)
    crud_collections.create_collection(collection_data=collection_2)

    assert PyObjectId.is_valid(collection_id_1)
    assert PyObjectId.is_valid(collection_id_2)

    response = crud_collections.get_many_collections_by_id(collection_ids=[collection_id_1, collection_id_2])
    for item in response:
        assert str(item.collection_id) in [collection_id_1, collection_id_2]
    
    response = sorted(response, key=lambda item: item.name)
    assert response[0].name == "Favorite Desserts"
    assert len(response) == 2

def test_2_get_multiple_collections_by_id():
    # Test retrieval of collections with bad id
    crud_collections.delete_all_collections()
    collection_id = crud_collections.create_collection(collection_data=collection)
    crud_collections.create_collection(collection_data=collection_2)

    response = crud_collections.get_many_collections_by_id(collection_ids=[collection_id, "673939ecbce83aa91d4e20ab"])
    assert len(response) == 1
    assert response[0].name == "Favorites"

def test_update_collection():
    # Test correct update
    crud_collections.delete_all_collections()
    collection_id = crud_collections.create_collection(collection_data=collection)
    assert PyObjectId.is_valid(collection_id)

    new_collection = updated_collection
    new_collection['collection_id'] = collection_id

    response = crud_collections.update_collection(collection_id=collection_id, updated_data=updated_collection)
    assert response["message"] == "Collection updated successfully"

    response = crud_collections.get_collection_by_id(collections_id=collection_id)
    assert response.name == "Favorite Desserts"

def test_fail_update_collection():
    # Test error handling for updating with invalid data
    crud_collections.delete_all_collections()
    collection_id = crud_collections.create_collection(collection_data=collection)
    assert PyObjectId.is_valid(collection_id)

    with pytest.raises(ValueError) as exc_info:
        crud_collections.update_collection(collection_id=collection_id, updated_data=bad_collection)

    assert "user_id" and "field required" in str(exc_info.value)

def test_delete_collection():
    # Test correct delete
    crud_collections.delete_all_collections()
    collection_id = crud_collections.create_collection(collection_data=collection)
    crud_collections.create_collection(collection_data=updated_collection)
    assert PyObjectId.is_valid(collection_id)

    response = crud_collections.delete_collection(collection_id=collection_id)
    assert response["message"] == "Collection deleted successfully"

    response = crud_collections.get_all_collections()
    assert len(response) == 1

def test_fail_delete_collection():
    # Test invalid delete
    crud_collections.delete_all_collections()
    collection_id = "672af6cd3d7885e1b7eaf6d4"

    with pytest.raises(Exception) as exc_info:
        crud_collections.delete_collection(collection_id=collection_id)
    
    assert "Collection not found" in str(exc_info.value)

def test_delete_all():
    # Test correct delete all
    crud_collections.create_collection(collection_data=collection)
    response = crud_collections.get_all_collections()

    assert len(response) == 1
    crud_collections.delete_all_collections()
    response = crud_collections.get_all_collections()

    assert len(response) == 0


def test_get_all_collections():
    # Test correct retrieval of all collections
    crud_collections.delete_all_collections()
    collection_id_1 = crud_collections.create_collection(collection_data=collection)
    collection_id_2 = crud_collections.create_collection(collection_data=updated_collection)

    assert PyObjectId.is_valid(collection_id_1)
    assert PyObjectId.is_valid(collection_id_2)

    response = crud_collections.get_all_collections()
    for item in response:
        assert str(item.collection_id) in [collection_id_1, collection_id_2]
    
    assert len(response) == 2

def test_fail_get_all_collections():
    # Test retrieval of no collections
    crud_collections.delete_all_collections()

    response = crud_collections.get_all_collections()
    assert len(response) == 0

