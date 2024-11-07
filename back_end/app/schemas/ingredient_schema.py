from pydantic import BaseModel, Field
from typing import List, Optional

class Ingredient(BaseModel):
    order: int = Field(..., description="Order of ingredients in the recipe")
    quantity: str = Field(..., description="Amount of the ingredient, convert to num in edit mode or when doubling")
    unit: Optional[str] = Field(None, description="Unit of the ingredient")
    name: str = Field(..., min_length=1, description="Name of the ingredient")
    is_optional: bool = Field(default=False, description="Flag to mark if ingredient is optional")
    section: Optional[str] = Field(None, min_length=1, description="The section to which the ingredient belongs")

    class Config:
       schema_extra = {
            "example": {
                "order": 1,
                "quantity": "1 1/2",
                "unit": "cups",
                "name": "sauce",
                "is_optional": False,
                "section": "Sauce"
            }
        }