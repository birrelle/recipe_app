# test_route_recipes.py
import unittest
from unittest.mock import patch
from app.utils import PyObjectId
from app.utils.enums import SearchType
from app import create_app
from app.schemas import Recipe
from flask import Flask
import pytest
from config import TestingConfig
from flask_pymongo import PyMongo
from app.routes import recipes
import json


recipe = {
    "recipe_id": "6739398dcd1f29c55bcf0e83",
    "title": "Pasta Primavera",
    "user_id": "672af6cd3d7885e1b7eaf6d4",
    "source": "Budget Bytes",
    "course": ["Dinner"],
    "ingredients": [
        {
            "order": 1,
            "quantity": "16",
            "unit": "oz",
            "name": "pasta",
            "is_optional": False,
            "section": "Pasta"
        },
        {
            "order": 2,
            "quantity": "2",
            "unit": "count",
            "name": "tomatoes",
            "is_optional": False,
            "section": "Sauce"
        },
        {
            "order": 3,
            "quantity": "4",
            "unit": "cloves",
            "name": "garlic",
            "is_optional": True,
            "section": "Sauce"
        }
    ],
    "sections": [
        {"order": 1, "name": "Pasta", "is_optional": False},
        {"order": 2, "name": "Sauce", "is_optional": False}
    ],
    "directions": [
        {"order": 1, "direction": "Boil water", "is_optional": False},
        {"order": 2, "direction": "Make pasta", "is_optional": False},
        {"order": 3, "direction": "Make sauce", "is_optional": False},
        {"order": 3, "direction": "Mix and serve warm", "is_optional": False}
    ],
    "serving_size": 4,
    "prep_time": 20,
    "cooking_time": 50,
    "total_time": 70,
    "notes": "Bake for longer at higher altitude",
    "image": "/images/picture.jpg",
    "created_at": "2024-10-18T15:30:00Z"
}
recipe_2 = {
    "recipe_id": "674624ed13f37e9e21246d55",
    "title": "Pizza",
    "user_id": "672af6cd3d7885e1b7eaf6d4",
    "source": "Budget Bytes",
    "course": ["Lunch"],
    "ingredients": [
        {
            "order": 1,
            "quantity": "16",
            "unit": "oz",
            "name": "Pizza dough",
            "is_optional": False,
            "section": "Pasta"
        },
        {
            "order": 2,
            "quantity": "2",
            "unit": "count",
            "name": "Tomatoes",
            "is_optional": False,
            "section": "Sauce"
        },
        {
            "order": 3,
            "quantity": "4",
            "unit": "blocks",
            "name": "cheese",
            "is_optional": True,
            "section": "Sauce"
        }
    ],
    "sections": [
        {"order": 1, "name": "Pizza", "is_optional": False},
        {"order": 2, "name": "Sauce", "is_optional": False}
    ],
    "directions": [
        {"order": 1, "direction": "Make dough", "is_optional": False},
        {"order": 2, "direction": "Gather ingredients", "is_optional": False},
        {"order": 3, "direction": "Make sauce", "is_optional": False},
        {"order": 3, "direction": "Mix and serve warm", "is_optional": False}
    ],
    "serving_size": 4,
    "prep_time": 20,
    "cooking_time": 50,
    "total_time": 70,
    "notes": "Bake for longer at higher altitude",
    "image": "/images/picture.jpg",
    "created_at": "2024-10-18T15:30:00Z"
}
bad_recipe = {
    "recipe_id": "6746240796be8f7e6a8ab32c",
    "title": "Pasta",
    "source": "Budget Bytes",
    "course": ["Dinner"],
    "sections": [
        {"order": 1, "name": "Pasta", "is_optional": False},
        {"order": 2, "name": "Sauce", "is_optional": False}
    ],
    "directions": [
        {"order": 1, "direction": "Boil water", "is_optional": False},
        {"order": 2, "direction": "Make pasta", "is_optional": False},
        {"order": 3, "direction": "Make sauce", "is_optional": False},
        {"order": 3, "direction": "Mix and serve warm", "is_optional": False}
    ],
    "serving_size": 4,
    "prep_time": 20,
    "cooking_time": 50,
    "total_time": 70,
    "notes": "Bake for longer at higher altitude",
    "image": "/images/picture.jpg",
    "created_at": "2024-10-18T15:30:00Z"
}
updated_recipe = {
    "recipe_id": "6739398dcd1f29c55bcf0e83",
    "title": "Yummy Pasta",
    "user_id": "6738eab60f9babcf62eea6df",
    "source": "Budget Bytes",
    "course": ["Lunch"],
    "ingredients": [
        {
            "order": 1,
            "quantity": "16",
            "unit": "oz",
            "name": "pasta",
            "is_optional": False,
            "section": "Pasta"
        },
        {
            "order": 2,
            "quantity": "2",
            "unit": "count",
            "name": "tomatoes",
            "is_optional": False,
            "section": "Sauce"
        },
        {
            "order": 3,
            "quantity": "4",
            "unit": "cloves",
            "name": "garlic",
            "is_optional": True,
            "section": "Sauce"
        }
    ],
    "sections": [
        {"order": 1, "name": "Pasta", "is_optional": False},
        {"order": 2, "name": "Sauce", "is_optional": False}
    ],
    "directions": [
        {"order": 1, "direction": "Boil water", "is_optional": False},
        {"order": 2, "direction": "Make pasta", "is_optional": False},
        {"order": 3, "direction": "Make sauce", "is_optional": False},
        {"order": 3, "direction": "Mix and serve warm", "is_optional": False}
    ],
    "serving_size": 8,
    "prep_time": 20,
    "cooking_time": 50,
    "total_time": 70,
    "notes": "Bake for longer at higher altitude",
    "image": "/images/picture.jpg",
    "created_at": "2024-10-18T15:30:00Z"
}
recipe_3 = {"recipe_id": "674623ee8e87475df81dbcf7",
    "title": "Pasta Primavera recipe",
    "user_id": "672af6cd3d7885e1b7eaf6d4"}
user = { "user_id": "672af6cd3d7885e1b7eaf6d4", "username": "username_1",
        "collection_ids": [],
        "recipe_ids": []}

def test_create_recipe_route(client):
    with patch('app.database.db.recipes_collection.insert_one') as mock:
        with patch('app.database.db.users_collection.update_one') as mock_update_user:
            with patch('app.database.db.users_collection.find_one') as mock_user:
                mock.return_value.inserted_id = PyObjectId()
                mock_user.return_value = user
                mock_update_user.return_value.matched_count = 1
                
                response = client.post('/recipes', json=recipe)
                
                # Assertions
                assert response.status_code == 200
                assert 'id' in response.json
                assert PyObjectId.is_valid(response.json['id'])


def test_get_recipe_route(client):
    with patch('app.database.db.recipes_collection.find_one') as mock:
        mock.return_value = recipe
        response = client.get('/recipes/6739398dcd1f29c55bcf0e83')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['recipe_id'] == "6739398dcd1f29c55bcf0e83"
        assert PyObjectId.is_valid(data['recipe_id'])
        assert data["title"] == "Pasta Primavera"
        assert data["user_id"] == "672af6cd3d7885e1b7eaf6d4"


def test_get_many_recipes_route(client):
    with patch('app.database.db.recipes_collection.find') as mock:
        mock.return_value = [recipe,recipe_2,recipe_3]
        recipe_ids = ['6739398dcd1f29c55bcf0e83', '674624ed13f37e9e21246d55', '674623ee8e87475df81dbcf7']

        response = client.get('/recipes/many', json=recipe_ids)

        assert response.status_code == 200

        response = json.loads(response.data)
        data = []
        for item in response:
            item = json.loads(item)
            assert item['recipe_id'] in recipe_ids
            data.append(item)
    
        data = sorted(data, key=lambda item: item['title'])
        assert data[0]['title'] == "Pasta Primavera"
        assert data[1]['course'] == None
        assert len(data) == 3


def test_get_all_recipes_for_user_route(client):
    with patch('app.database.db.recipes_collection.find') as mock:
        mock.return_value = [recipe, recipe_2]
        response = client.get('/recipes/user/672af6cd3d7885e1b7eaf6d4')

        assert response.status_code == 200

        response = json.loads(response.data)
        data = []
        for item in response:
            item = json.loads(item)
            assert item['recipe_id'] in ['6739398dcd1f29c55bcf0e83', '674624ed13f37e9e21246d55']
            data.append(item)
        
        data = sorted(data, key=lambda item: item['title'])
        assert data[0]['title'] == 'Pasta Primavera'
        assert data[1]['course'] == ['Lunch']
        assert len(data) == 2


def test_get_all_recipes_route(client):
    with patch('app.database.db.recipes_collection.find') as mock:
        mock.return_value = [recipe_2, recipe_3]
        response = client.get('/recipes/all')

        assert response.status_code == 200

        response = json.loads(response.data)
        data = []
        for item in response:
            item = json.loads(item)
            assert item['recipe_id'] in ['674624ed13f37e9e21246d55', '674623ee8e87475df81dbcf7']
            data.append(item)
        
        data = sorted(data, key=lambda item: item['title'])
        assert data[0]['title'] == 'Pasta Primavera recipe'
        assert data[0]['recipe_id'] == '674623ee8e87475df81dbcf7'
        assert data[1]['course'] == ["Lunch"]
        assert len(data) == 2


def test_search_ingredient_route(client):
    with patch('app.database.db.recipes_collection.find') as mock:
        mock.return_value = [recipe, recipe_2]
        recipe_json = {"user_id": "672af6cd3d7885e1b7eaf6d4", "search_type": SearchType.INGREDIENT, "search_term": "tomatoes"}
        recipe_json = json.loads(json.dumps(recipe_json, default=lambda x: x.value if isinstance(x, SearchType) else x))

        response = client.get('/recipes/search', json=recipe_json)

        assert response.status_code == 200

        response = json.loads(response.data)
        data = []
        for item in response:
            item = json.loads(item)
            assert item['recipe_id'] in ['6739398dcd1f29c55bcf0e83', '674624ed13f37e9e21246d55']
            data.append(item)
        
        data = sorted(data, key=lambda item: item['title'])
        assert data[0]['title'] == 'Pasta Primavera'
        assert data[0]['recipe_id'] == '6739398dcd1f29c55bcf0e83'
        assert data[1]['course'] == ['Lunch']
        assert len(data) == 2

def test_search_title_route(client):
    with patch('app.database.db.recipes_collection.find') as mock:
        mock.return_value = [recipe, recipe_3]
        recipe_json = {"user_id": "672af6cd3d7885e1b7eaf6d4", "search_type": SearchType.RECIPE, "search_term": "Pasta"}
        recipe_json = json.loads(json.dumps(recipe_json, default=lambda x: x.value if isinstance(x, SearchType) else x))
        
        response = client.get('/recipes/search', json=recipe_json)

        assert response.status_code == 200

        response = json.loads(response.data)
        data = []
        for item in response:
            item = json.loads(item)
            assert item['recipe_id'] in ['6739398dcd1f29c55bcf0e83', '674623ee8e87475df81dbcf7']
            data.append(item)
        
        data = sorted(data, key=lambda item: item['title'])
        assert data[0]['title'] == 'Pasta Primavera'
        assert data[0]['recipe_id'] == '6739398dcd1f29c55bcf0e83'
        assert len(data) == 2


def test_update_existing_recipe_route(client):
    with patch('app.database.db.recipes_collection.update_one') as mock:
        mock.return_value.matched_count = 1
        response = client.put('/recipes/6739398dcd1f29c55bcf0e83', json=updated_recipe)

        assert response.status_code == 200
        assert response.json['message'] == "Recipe updated successfully"


def test_delete_recipe_by_id_route(client):
    with patch('app.database.db.recipes_collection.delete_one') as mock:
        mock.return_value.deleted_count = 1
        response = client.delete('/recipes/6739398dcd1f29c55bcf0e83')

        assert response.status_code == 200
        assert response.json['message'] == "Recipe deleted successfully"