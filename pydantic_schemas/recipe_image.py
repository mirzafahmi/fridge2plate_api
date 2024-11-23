from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any, Text
from uuid import UUID 


class RecipeImageBase(LowercaseBaseModel):
    image: str

    model_config = {
        "transform_fields": []
    }

class RecipeImageCreate(RecipeImageBase):
    ...

class RecipeImageCreateSeeder(RecipeImageCreate):
    id: Optional[UUID] = None

class RecipeImage(LowercaseBaseModel):
    id: UUID
    image: str

    class Config:
        orm_mode = True

class RecipeImageUpdate(RecipeImageBase):
    ...

class RecipeImagesByRecipe(LowercaseBaseModel):
    recipe_id: UUID
    RecipeImages: List[RecipeImage]