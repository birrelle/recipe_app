# test_route_collections.py
import unittest
from unittest.mock import patch
from app.utils import PyObjectId
from app.utils.enums import SearchType
from app import create_app
from app.schemas import Collection
from flask import Flask
import pytest
from config import TestingConfig
from flask_pymongo import PyMongo
from app.routes import collections
import json

collection = {"collection_id": "674623ee8e87475df81dbcf7", "name": "Favorites",
                "user_id": "672af6cd3d7885e1b7eaf6d4",
                "recipe_ids": ["673939ecbce83aa91d4e20aa", "673939e155abdf31fbf15fef", "673939e155abdf31fbf15ff0"]}
collection_2 = {"collection_id": "6746240796be8f7e6a8ab32c", "name": "Thanksgiving",
                "user_id": "672af6cd3d7885e1b7eaf6d4",
                "recipe_ids": ["673939cf5a425b66cc8c3dd2", "672af6cd3d7885e1b7eaf6d4", "673939ba7cb7a2ab4a91f6fa"]}
collection_3 = {"collection_id": "674624ed13f37e9e21246d55", "name": "Fav dinners", "user_id": "673939ecbce83aa91d4e20ab",
                "recipe_ids": ["673939cf5a425b66cc8c3dd2", "672af6cd3d7885e1b7eaf6d4", "673939ba7cb7a2ab4a91f6fa"]}
updated_collection = {"collection_id": "674623ee8e87475df81dbcf7", "name": "Favorite Desserts",
                "user_id": "673939ecbce83aa91d4e20ab",
                "recipe_ids": ["673939ecbce83aa91d4e20aa", "673939e155abdf31fbf15fef", "673939e155abdf31fbf15ff0"]}
user = { "user_id": "672af6cd3d7885e1b7eaf6d4", "username": "username_1",
        "collection_ids": [],
        "recipe_ids": []}

def test_create_collection_route(client):
    with patch('app.database.db.collections_collection.insert_one') as mock:
        with patch('app.database.db.users_collection.update_one') as mock_update_user:
            with patch('app.database.db.users_collection.find_one') as mock_user:
                mock.return_value.inserted_id = PyObjectId()
                mock_user.return_value = user
                mock_update_user.return_value.matched_count = 1
                
                response = client.post('/collections', json=collection)
                
                # Assertions
                assert response.status_code == 200
                assert 'id' in response.json
                assert PyObjectId.is_valid(response.json['id'])


def test_get_collection_route(client):
    with patch('app.database.db.collections_collection.find_one') as mock:
        mock.return_value = collection
        response = client.get('/collections/674623ee8e87475df81dbcf7')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['collection_id'] == "674623ee8e87475df81dbcf7"
        assert PyObjectId.is_valid(data['collection_id'])
        assert data["name"] == "Favorites"
        assert data["user_id"] == "672af6cd3d7885e1b7eaf6d4"


def test_get_all_collections_for_user_route(client):
    with patch('app.database.db.collections_collection.find') as mock:
        mock.return_value = [collection, collection_3]
        response = client.get('/collections/user/673939ecbce83aa91d4e20ab')

        assert response.status_code == 200

        response = json.loads(response.data)
        data = []
        for item in response:
            item = json.loads(item)
            assert item['collection_id'] in ['674623ee8e87475df81dbcf7', '674624ed13f37e9e21246d55']
            data.append(item)
        
        data = sorted(data, key=lambda item: item['name'])
        assert data[0]['name'] == 'Fav dinners'
        assert data[1]['recipe_ids'] == ["673939ecbce83aa91d4e20aa", "673939e155abdf31fbf15fef", "673939e155abdf31fbf15ff0"]
        assert len(data) == 2


def test_get_all_collections_route(client):
    with patch('app.database.db.collections_collection.find') as mock:
        mock.return_value = [collection_2, collection_3]
        response = client.get('/collections/all')

        assert response.status_code == 200

        response = json.loads(response.data)
        data = []
        for item in response:
            item = json.loads(item)
            assert item['collection_id'] in ['6746240796be8f7e6a8ab32c', '674624ed13f37e9e21246d55']
            data.append(item)
        
        data = sorted(data, key=lambda item: item['name'])
        assert data[0]['name'] == 'Fav dinners'
        assert data[0]['collection_id'] == '674624ed13f37e9e21246d55'
        assert data[1]['recipe_ids'] == ["673939cf5a425b66cc8c3dd2", "672af6cd3d7885e1b7eaf6d4", "673939ba7cb7a2ab4a91f6fa"]
        assert len(data) == 2


def test_add_collections_to_collection_route(client):
    with patch('app.database.db.collections_collection.update_one') as mock:
        mock.return_value.matched_count = 1
        response = client.put('/collections/6739398dcd1f29c55bcf0e83', json=updated_collection)

        assert response.status_code == 200
        assert response.json['message'] == "Collection updated successfully"


def test_update_existing_collections_route(client):
    with patch('app.database.db.collections_collection.update_one') as mock:
        mock.return_value.matched_count = 1
        response = client.put('/collections/6739398dcd1f29c55bcf0e83', json=updated_collection)

        assert response.status_code == 200
        assert response.json['message'] == "Collection updated successfully"


def test_delete_collection_by_id_route(client):
    with patch('app.database.db.collections_collection.delete_one') as mock:
        mock.return_value.deleted_count = 1
        response = client.delete('/collections/6739398dcd1f29c55bcf0e83')

        assert response.status_code == 200
        assert response.json['message'] == "Collection deleted successfully"