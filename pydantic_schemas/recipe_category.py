from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
import uuid
from typing import Optional


class RecipeCategoryBase(LowercaseBaseModel):
    name: str


class RecipeCategoryCreate(RecipeCategoryBase):
    ...

class RecipeCategoryCreateSeeder(RecipeCategoryCreate):
    id: Optional[uuid.UUID] = None

class RecipeCategory(RecipeCategoryBase):
    id: uuid.UUID
    created_date: datetime
    updated_date: datetime

    class ConfigDict:
        from_attributes = True


class RecipeCategoryCreatedResponse(LowercaseBaseModel):
    result: str
    data: RecipeCategory