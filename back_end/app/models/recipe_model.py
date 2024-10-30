from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Set
from app.utils.enums import Course
from back_end.app.schemas.ingredient_schema import Ingredient
from datetime import datetime, timezone

class RecipesModel(BaseModel):
    title: str
    user: str
    source: Optional[str] = None
    course: Optional[List[Course]] = []
    ingredients: Optional[List[Ingredient]] = []
    sections: Optional[List[Dict]] = []
    directions: Optional[List[Dict]] = []
    serving_size: Optional[int] = None
    prep_time: Optional[int] = None # in minutes
    cooking_time: Optional[int] = None  # in minutes
    total_time: Optional[int] = None # in minutes
    notes: Optional[str] = None
    image: Optional[str] = None # url or file path
    created_at: datetime = datetime.now()
    
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True  
        schema_extra = {
            "example": {
                "title": "Pasta Primavera",
                "user": "user_id",
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
                    {"order": 1, "direction": "Boil water"},
                    {"order": 2, "direction": "Make pasta"},
                    {"order": 3, "direction": "Make sauce"},
                    {"order": 3, "direction": "Mix and serve warm"}
                ],
                "serving_size": 4,
                "prep_time": 20,
                "cooking_time": 50,
                "total_time": 70,
                "notes": "Bake for longer at higher altitude",
                "image": "/images/picture.jpg",
                "created_at": "2024-10-18T15:30:00Z"
            }
        }

class RecipesInDB(RecipesModel):
    id: str
