from pydantic import BaseModel, Field
from typing import List, Optional, Set
from datetime import datetime, timezone

class UsersModel(BaseModel):
    username: str
    collection_ids: Optional[List[str]] # store the collection IDs related to the user
    recipe_ids: Optional[List[str]] # store the recipe IDs related to the user
    created_at: datetime = datetime.now()
    
    class Config:
        schema_extra = {
            "example": {
                "username": "unique_username",
                "collection_ids": ["id1", "id2","id3"],
                "recipe_ids": ["id_123", "id_234", "id_345"],
                "created_at": "2024-10-18T15:30:00Z"
            }
        }

class UsersinDB(UsersModel):
    id: str
