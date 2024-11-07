from app.routes import recipes
import requests

# Define the recipe data
# payload = {
#     "username": "new_name"
# }
payload = {
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
        {"order": 1, "name": "Pasta"},
        {"order": 2, "name": "Sauce"}
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
    "image": "/images/picture.jpg"
}

# url = "http://127.0.0.1:5000/recipes/user/672af6cd3d7885e1b7eaf6d4"
url = "http://127.0.0.1:5000/users"
# url = "http://127.0.0.1:5000/recipes/671ad05c6ca9ac1b4eff9244"

# Add the recipe using the create_recipe function
# response = requests.post(url, json=payload)
response = requests.get(url)
print(response)

