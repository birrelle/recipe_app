from pydantic import BaseModel, Field
from typing import List, Optional

class Section(BaseModel):
    order: int = Field(..., description="Order of section in the recipe")
    name: str = Field(..., description="Name of the section")
    is_optional: bool = Field(default=False, description="Flag to mark if step is optional")

    class Config:
       schema_extra = {
            "example": {
                "order": 1,
                "name": "Pasta",
                "is_optional": False
            }
        }