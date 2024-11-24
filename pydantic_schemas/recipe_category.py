from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
import uuid
from typing import List, Optional
from pydantic import constr

from .user import UserResponse


class RecipeCategoryBase(LowercaseBaseModel):
    name: constr(strip_whitespace=True, min_length=3)
    created_by: Optional[uuid.UUID] = None

    model_config = {
        "transform_fields": ["name"]
    }

class RecipeCategoryCreate(RecipeCategoryBase):
    ...

class RecipeCategoryUpdate(LowercaseBaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=3)] = None
    created_by: Optional[uuid.UUID] = None

    model_config = {
        "transform_fields": ["name"]
    }

class RecipeCategoryCreateSeeder(RecipeCategoryCreate):
    id: Optional[uuid.UUID] = None

class RecipeCategory(LowercaseBaseModel):
    id: uuid.UUID
    name: str
    creator: UserResponse
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

class RecipeCategoryLite(LowercaseBaseModel):
    name: str

    class Config:
        from_attributes = True

class RecipeCategoryResponse(LowercaseBaseModel):
    detail: str
    recipe_category: RecipeCategory

class RecipeCategoriesResponse(LowercaseBaseModel):
    detail: str
    recipe_categories: List[RecipeCategory]