from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Set
from app.utils.enums import Course
from app.schemas.ingredient_schema import Ingredient
from app.schemas.direction_schema import Direction
from app.schemas.section_schema import Section
from datetime import datetime, timezone
from app.schemas import PyObjectId

# Define the Recipe schema using Pydantic
class RecipesSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId)
    title: str = Field(..., min_length=1, max_length=100, description="Name of the recipe")
    user_id: PyObjectId
    source: Optional[str] = Field(None, min_length=1, description="Where the recipe came from")
    course: Optional[List[Course]] 
    ingredients: Optional[List[Ingredient]] 
    sections: Optional[List[Section]] 
    directions: Optional[List[Direction]] 
    serving_size: Optional[int] = Field(None, gt=0, description="Number of servings")
    prep_time: Optional[int] = Field(None, gt=0, description="Prep time in minutes")
    cooking_time: Optional[int] = Field(None, description="Cooking time in minutes")
    total_time: Optional[int] = Field(None, gt=0, description="Total time in minutes")
    notes: Optional[str] = Field(None, description="Any additional notes related to the recipe")
    image: Optional[str] = Field(None, description="Image location path")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), example="2024-10-18T15:30:00Z")


    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True  
        json_encoders = {PyObjectId: str}
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