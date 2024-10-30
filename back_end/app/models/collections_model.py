from pydantic import BaseModel, Field
from typing import List, Optional, Set
from datetime import datetime, timezone

class CollectionsModel(BaseModel):
    name: str
    recipe_ids: Optional[List[str]] # store the recipe IDs in the collection
    created_at: datetime = datetime.now()
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Favorites",
                "recipe_ids": ["id_123", "id_234", "id_345"],
                "created_at": "2024-10-18T15:30:00Z"
            }
        }

class CollectionsInDB(CollectionsModel):
    id: str
