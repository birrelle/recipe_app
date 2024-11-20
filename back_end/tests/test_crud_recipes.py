# test_crud_recipes.py
from app.crud import crud_recipes
import pytest
from flask import Flask
from config import TestingConfig
from app.utils import PyObjectId
from app.utils import enums

recipe = {
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

app = Flask(__name__)
app.config.from_object(TestingConfig)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
        
def test_create_recipe():
    # Test correct insertion
    response = crud_recipes.create_recipe(recipe=recipe)
    assert PyObjectId.is_valid(response)

def test_fail_create_recipe():
    # Test error handling for missing required fields
    with pytest.raises(ValueError) as exc_info:
        crud_recipes.create_recipe(recipe=bad_recipe)

    assert "user_id" and "field required" in str(exc_info.value)

def test_get_recipe():
    # Test correct retrieval
    crud_recipes.delete_all_recipes()
    recipe_id = crud_recipes.create_recipe(recipe=recipe)

    assert PyObjectId.is_valid(recipe_id)
    
    response = crud_recipes.get_recipe_by_id(recipe_id=recipe_id)
    assert response.title == "Pasta Primavera"
    assert response.prep_time == 20
    

def test_fail_get_recipe():
    # Test invalid retrieval
    crud_recipes.delete_all_recipes()
    recipe_id = "672af6cd3d7885e1b7eaf6d4"

    with pytest.raises(Exception) as exc_info:
        crud_recipes.get_recipe_by_id(recipe_id=recipe_id)
    
    assert "Recipe not found" in str(exc_info.value)

def test_get_recipe_by_user():
    # Test correct retrieval by user
    crud_recipes.delete_all_recipes()
    crud_recipes.create_recipe(recipe=recipe)
    crud_recipes.create_recipe(recipe=updated_recipe)

    response = crud_recipes.get_all_recipes_by_user(user_id="6738eab60f9babcf62eea6df")

    assert len(response) == 1
    assert response[0].title == "Yummy Pasta"
    assert response[0].course == ["Lunch"] 
    
def test_fail_get_recipe_by_user():
    # Test invalid retrival by user
    crud_recipes.delete_all_recipes()
    crud_recipes.create_recipe(recipe=recipe)

    response = crud_recipes.get_all_recipes_by_user(user_id="6738eab60f9babcf62eea6df")
    assert len(response) == 0

def test_update_recipe():
    # Test correct update
    crud_recipes.delete_all_recipes()
    recipe_id = crud_recipes.create_recipe(recipe=recipe)
    assert PyObjectId.is_valid(recipe_id)

    response = crud_recipes.update_recipe(recipe_id=recipe_id, updated_data=updated_recipe)
    assert response["message"] == "Recipe updated successfully"

    response = crud_recipes.get_recipe_by_id(recipe_id=recipe_id)
    assert response.title == "Yummy Pasta"
    assert response.serving_size == 8

def test_fail_update_recipe():
    # Test error handling for updating with invalid data
    crud_recipes.delete_all_recipes()
    recipe_id = crud_recipes.create_recipe(recipe=recipe)
    assert PyObjectId.is_valid(recipe_id)

    with pytest.raises(ValueError) as exc_info:
        crud_recipes.update_recipe(recipe_id=recipe_id, updated_data=bad_recipe)

    assert "user_id" and "field required" in str(exc_info.value)

def test_delete_recipe():
    # Test correct delete
    crud_recipes.delete_all_recipes()
    recipe_id = crud_recipes.create_recipe(recipe=recipe)
    crud_recipes.create_recipe(recipe=updated_recipe)
    assert PyObjectId.is_valid(recipe_id)

    response = crud_recipes.delete_recipe(recipe_id=recipe_id)
    assert response["message"] == "Recipe deleted successfully"

    response = crud_recipes.get_all_recipes()
    assert len(response) == 1

def test_fail_delete_recipe():
    # Test invalid delete
    crud_recipes.delete_all_recipes()
    recipe_id = "672af6cd3d7885e1b7eaf6d4"

    with pytest.raises(Exception) as exc_info:
        crud_recipes.delete_recipe(recipe_id=recipe_id)
    
    assert "Recipe not found" in str(exc_info.value)

def test_delete_all():
    # Test correct delete all
    crud_recipes.create_recipe(recipe=recipe)
    response = crud_recipes.get_all_recipes()

    assert len(response) == 1
    crud_recipes.delete_all_recipes()
    response = crud_recipes.get_all_recipes()

    assert len(response) == 0


def test_get_all_recipes():
    # Test correct retrieval of all recipes
    crud_recipes.delete_all_recipes()
    recipe_id_1 = crud_recipes.create_recipe(recipe=recipe)
    recipe_id_2 = crud_recipes.create_recipe(recipe=updated_recipe)

    assert PyObjectId.is_valid(recipe_id_1)
    assert PyObjectId.is_valid(recipe_id_2)

    response = crud_recipes.get_all_recipes()
    for item in response:
        assert str(item.id) in [recipe_id_1, recipe_id_2]
    
    assert len(response) == 2

def test_fail_get_all_recipes():
    # Test retrieval of no recipes
    crud_recipes.delete_all_recipes()

    response = crud_recipes.get_all_recipes()
    assert len(response) == 0

def test_get_multiple_recipes_by_id():
    # Test correct retrieval of all recipes
    crud_recipes.delete_all_recipes()
    recipe_id_1 = crud_recipes.create_recipe(recipe=recipe)
    recipe_id_2 = crud_recipes.create_recipe(recipe=updated_recipe)
    crud_recipes.create_recipe(recipe=recipe_2)

    assert PyObjectId.is_valid(recipe_id_1)
    assert PyObjectId.is_valid(recipe_id_2)

    response = crud_recipes.get_many_recipes_by_id(recipe_ids=[recipe_id_1, recipe_id_2])
    for item in response:
        assert str(item.id) in [recipe_id_1, recipe_id_2]
    
    response = sorted(response, key=lambda item: item.title)
    assert response[0].title == "Pasta Primavera"
    assert response[1].course == ["Lunch"]
    assert len(response) == 2

def test_2_get_multiple_recipes_by_id():
    # Test retrieval of recipes with bad id
    crud_recipes.delete_all_recipes()
    recipe_id = crud_recipes.create_recipe(recipe=recipe)
    crud_recipes.create_recipe(recipe=recipe_2)

    response = crud_recipes.get_many_recipes_by_id(recipe_ids=[recipe_id, "673939ecbce83aa91d4e20ab"])
    assert len(response) == 1
    assert response[0].title == "Pasta Primavera"

def test_search_recipes():
    # Test valid search
    crud_recipes.delete_all_recipes()
    crud_recipes.create_recipe(recipe=recipe)
    crud_recipes.create_recipe(recipe=recipe_2)
    crud_recipes.create_recipe(recipe=updated_recipe)

    response = crud_recipes.search_recipes(search_term="tomatoes", search_type=enums.SearchType.INGREDIENT, user_id="672af6cd3d7885e1b7eaf6d4")
    assert len(response) == 2
    response = sorted(response, key=lambda item: item.title)
    assert response[1].title == "Pizza"

    response = crud_recipes.search_recipes(search_term="pasta", search_type=enums.SearchType.RECIPE, user_id="6738eab60f9babcf62eea6df")
    assert len(response) == 1
    assert response[0].title == "Yummy Pasta"
    assert response[0].course == ["Lunch"]

def test_fail_search_recipes():
    #Test invalid search
    crud_recipes.delete_all_recipes()
    crud_recipes.create_recipe(recipe=recipe)
    crud_recipes.create_recipe(recipe=recipe_2)
    crud_recipes.create_recipe(recipe=updated_recipe)

    response = crud_recipes.search_recipes(search_term="tomatoes", search_type=enums.SearchType.INGREDIENT, user_id="6739394df0a1fa62defe9ece")
    assert len(response) == 0

    response = crud_recipes.search_recipes(search_term="tomatoes", search_type=enums.SearchType.RECIPE, user_id="6738eab60f9babcf62eea6df")
    assert len(response) == 0

    response = crud_recipes.search_recipes(search_term="Yummy Pasta", search_type=enums.SearchType.INGREDIENT, user_id="6738eab60f9babcf62eea6df")
    assert len(response) == 0
