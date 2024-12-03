# test_route_users.py
import unittest
from unittest.mock import patch
from app.utils import PyObjectId
from app.utils.enums import SearchType
from app import create_app
from app.schemas import User
from flask import Flask
import pytest
from config import TestingConfig
from flask_pymongo import PyMongo
from app.routes import users
import json

user = { "user_id": "674623ee8e87475df81dbcf7", "username": "username_1",
        "collection_ids": ["673939ecbce83aa91d4e20aa"],
        "recipe_ids": ["673939cf5a425b66cc8c3dd2", "672af6cd3d7885e1b7eaf6d4"]}
user_2 = {"user_id": "6746240796be8f7e6a8ab32c", "username": "username_2",
        "recipe_ids": ["672af6cd3d7885e1b7eaf6d4"]}
user_3 = {"user_id": "674624ed13f37e9e21246d55", "username": "zzz", "recipe_ids": ["673939cf5a425b66cc8c3dd2", "672af6cd3d7885e1b7eaf6d4", "673939ba7cb7a2ab4a91f6fa"]}
updated_user = {"user_id": "674623ee8e87475df81dbcf7", "username": "new_username",
                "collection_ids": [],
                "recipe_ids": ["673939cf5a425b66cc8c3dd2", "672af6cd3d7885e1b7eaf6d4", "673939ba7cb7a2ab4a91f6fa"]}


def test_create_user_route(client):
    with patch('app.database.db.users_collection.insert_one') as mock:
        mock.return_value.inserted_id = PyObjectId()
        response = client.post('/users', json=user)
        
        # Assertions
        assert response.status_code == 200
        assert 'id' in response.json
        assert PyObjectId.is_valid(response.json['id'])


def test_get_user_route(client):
    with patch('app.database.db.users_collection.find_one') as mock:
        mock.return_value = user
        response = client.get('/users/674623ee8e87475df81dbcf7')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user_id'] == "674623ee8e87475df81dbcf7"
        assert PyObjectId.is_valid(data['user_id'])
        assert data["username"] == "username_1"


def test_get_all_users_route(client):
    with patch('app.database.db.users_collection.find') as mock:
        mock.return_value = [user_2, user_3]
        response = client.get('/users/all')

        assert response.status_code == 200

        response = json.loads(response.data)
        data = []
        for item in response:
            item = json.loads(item)
            assert item['user_id'] in ['6746240796be8f7e6a8ab32c', '674624ed13f37e9e21246d55']
            data.append(item)
        
        data = sorted(data, key=lambda item: item['username'])
        assert data[0]['username'] == 'username_2'
        assert data[1]['recipe_ids'] == ["673939cf5a425b66cc8c3dd2", "672af6cd3d7885e1b7eaf6d4", "673939ba7cb7a2ab4a91f6fa"]
        assert len(data) == 2


def test_update_existing_user_route(client):
    with patch('app.database.db.users_collection.update_one') as mock:
        mock.return_value.matched_count = 1
        response = client.put('/users/6739398dcd1f29c55bcf0e83', json=updated_user)

        assert response.status_code == 200
        assert response.json['message'] == "User updated successfully"


def test_delete_user_by_id_route(client):
    with patch('app.database.db.users_collection.delete_one') as mock:
        mock.return_value.deleted_count = 1
        response = client.delete('/users/6739398dcd1f29c55bcf0e83')

        assert response.status_code == 200
        assert response.json['message'] == "User deleted successfully"