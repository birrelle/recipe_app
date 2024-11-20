# test_crud_users.py
from app.crud import crud_users
import pytest
from flask import Flask
from config import TestingConfig
from app.utils import PyObjectId
from app.schemas import User

user = { "username": "username_1",
        "collection_ids": ["673939ecbce83aa91d4e20aa"],
        "recipe_ids": ["673939cf5a425b66cc8c3dd2", "672af6cd3d7885e1b7eaf6d4"]}
user_2 = { "username": "username_2",
        "recipe_ids": ["672af6cd3d7885e1b7eaf6d4"]}
bad_user = {"recipe_ids": ["673939cf5a425b66cc8c3dd2", "672af6cd3d7885e1b7eaf6d4", "673939ba7cb7a2ab4a91f6fa"]}
updated_user = {"username": "new_username",
                "collection_ids": [],
                "recipe_ids": ["673939cf5a425b66cc8c3dd2", "672af6cd3d7885e1b7eaf6d4", "673939ba7cb7a2ab4a91f6fa"]}

app = Flask(__name__)
app.config.from_object(TestingConfig)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
        
def test_create_user():
    # Test correct insertion
    response = crud_users.create_user(user_data=user)
    assert PyObjectId.is_valid(response)

def test_fail_create_user():
    # Test error handling for missing required fields
    with pytest.raises(ValueError) as exc_info:
        crud_users.create_user(user_data=bad_user)

    assert "username" and "field required" in str(exc_info.value)

def test_get_user():
    # Test correct retrieval
    crud_users.delete_all_users()
    user_id = crud_users.create_user(user_data=user)

    assert PyObjectId.is_valid(user_id)
    
    response = crud_users.get_user_by_id(user_id=user_id)
    assert response.username == "username_1"
    assert str(response.collection_ids[0]) == "673939ecbce83aa91d4e20aa"
    

def test_fail_get_user():
    # Test invalid retrieval
    crud_users.delete_all_users()
    user_id = "672af6cd3d7885e1b7eaf6d4"

    with pytest.raises(Exception) as exc_info:
        crud_users.get_user_by_id(user_id=user_id)
    
    assert "User not found" in str(exc_info.value)

def test_update_user():
    # Test correct update
    crud_users.delete_all_users()
    user_id = crud_users.create_user(user_data=user)
    assert PyObjectId.is_valid(user_id)

    response = crud_users.update_user(user_id=user_id, updated_data=updated_user)
    assert response["message"] == "User updated successfully"

    response = crud_users.get_user_by_id(user_id=user_id)
    assert response.username == "new_username"

def test_fail_update_user():
    # Test error handling for updating with invalid data
    crud_users.delete_all_users()
    user_id = crud_users.create_user(user_data=user)
    assert PyObjectId.is_valid(user_id)

    with pytest.raises(ValueError) as exc_info:
        crud_users.update_user(user_id=user_id, updated_data=bad_user)

    assert "username" and "field required" in str(exc_info.value)

def test_delete_user():
    # Test correct delete
    crud_users.delete_all_users()
    user_id = crud_users.create_user(user_data=user)
    crud_users.create_user(user_data=updated_user)
    assert PyObjectId.is_valid(user_id)

    response = crud_users.delete_user(user_id=user_id)
    assert response["message"] == "User deleted successfully"

    response = crud_users.get_all_users()
    assert len(response) == 1

def test_fail_delete_user():
    # Test invalid delete
    crud_users.delete_all_users()
    user_id = "672af6cd3d7885e1b7eaf6d4"

    with pytest.raises(Exception) as exc_info:
        crud_users.delete_user(user_id=user_id)
    
    assert "User not found" in str(exc_info.value)

def test_delete_all():
    # Test correct delete all
    crud_users.create_user(user_data=user)
    response = crud_users.get_all_users()

    assert len(response) == 1
    crud_users.delete_all_users()
    response = crud_users.get_all_users()

    assert len(response) == 0


def test_get_all_users():
    # Test correct retrieval of all users
    crud_users.delete_all_users()
    user_id_1 = crud_users.create_user(user_data=user)
    user_id_2 = crud_users.create_user(user_data=updated_user)

    assert PyObjectId.is_valid(user_id_1)
    assert PyObjectId.is_valid(user_id_2)

    response = crud_users.get_all_users()
    for item in response:
        assert str(item.id) in [user_id_1, user_id_2]
    
    assert len(response) == 2

def test_fail_get_all_users():
    # Test retrieval of no users
    crud_users.delete_all_users()

    response = crud_users.get_all_users()
    assert len(response) == 0

