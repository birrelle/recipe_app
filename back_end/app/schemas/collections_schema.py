from pydantic import BaseModel, Field
from typing import List, Optional, Set
from datetime import datetime, timezone
from app.schemas import PyObjectId

class CollectionsSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId)
    name: str = Field(..., min_length=1, max_length=100, description="Name of the recipe")
    recipe_ids: Optional[List[str]] = Field(None, min_length=1, description="Where the recipe came from")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), example="2024-10-18T15:30:00Z")


    class Config:
       json_encoders = {PyObjectId: str}
       schema_extra = {
            "example": {
                "name": "Favorites",
                "recipe_ids": ["id_123", "id_234", "id_345"],
                "created_at": "2024-10-18T15:30:00Z"
            }
        }