from pydantic import BaseModel, Field
from typing import List, Optional

class Direction(BaseModel):
    order: int = Field(..., description="Order of direction in the recipe")
    direction: str = Field(..., description="Text of the direction")
    is_optional: bool = Field(default=False, description="Flag to mark if step is optional")