from pydantic import BaseModel, Field
from typing import List, Set, Optional
from datetime import datetime, timezone
from app.schemas import PyObjectId

class UserSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId)
    username: str = Field(..., min_length=1, max_length=100, description="User's username")
    collection_ids: Optional[List[str]] = Field(None, description="store the collection IDs related to the user")
    recipe_ids: Optional[List[str]] = Field(None, description="Store the recipe IDs related to the user")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), example="2024-10-18T15:30:00Z")

    class Config:
        json_encoders = {PyObjectId: str}
        schema_extra = {
            "example": {
                "username": "unique_username",
                "collection_ids": ["id1", "id2","id3"],
                "recipe_ids": ["id_123", "id_234", "id_345"],
                "created_at": "2024-10-18T15:30:00Z"
            }
        }