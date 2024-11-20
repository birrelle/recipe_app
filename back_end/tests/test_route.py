# test_routes.py
import unittest
from unittest.mock import patch
# from app.utils import PyObjectId
from app import create_app
from app.schemas import Recipe
from flask import Flask
import pytest
from config import TestingConfig

app = Flask(__name__)
app.config.from_object(TestingConfig)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

#     def test_home_route(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Welcome', response.get_data(as_text=True))

#     def test_recipes_route(self):
#         response = self.client.get('/recipes')
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(isinstance(response.json, list))

#     def test_invalid_route(self):
#         response = self.client.get('/nonexistent')
#         self.assertEqual(response.status_code, 404)

#     def test_recipe_detail_route(self):
#         # Mock a valid recipe ID
#         valid_id = str(PyObjectId())
#         response = self.client.get(f'/recipes/{valid_id}')
#         self.assertEqual(response.status_code, 404)  # Should be 404 if not found

    # @patch('app.routes.Recipe.create')
    # def test_create_recipe_route(self, mock_create):
    #     mock_create.return_value = {'_id': PyObjectId()}
    #     data = {
    #         'title': 'Test Recipe',
    #         'ingredients': ['ingredient1', 'ingredient2'],
    #         'instructions': ['step1', 'step2']
    #     }
    #     response = self.client.post('/recipes', json=data, headers=self.headers)
    #     self.assertEqual(response.status_code, 201)

    # def test_create_recipe_invalid_data(self):
    #     data = {'title': 'Test Recipe'}  # Missing required fields
    #     response = self.client.post('/recipes', json=data, headers=self.headers)
    #     self.assertEqual(response.status_code, 400)