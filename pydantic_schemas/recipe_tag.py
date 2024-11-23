from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
import uuid
from typing import List, Optional
from pydantic import constr

from .user import UserResponse


class RecipeTagBase(LowercaseBaseModel):
    name: constr(strip_whitespace=True, min_length=3)
    created_by: Optional[uuid.UUID] = None

    model_config = {
        "transform_fields": ["name"]
    }

class RecipeTagCreate(RecipeTagBase):
    ...

class RecipeTagUpdate(LowercaseBaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=3)] = None
    created_by: Optional[uuid.UUID] = None

    model_config = {
        "transform_fields": ["name"]
    }

class RecipeTagCreateSeeder(RecipeTagCreate):
    id: Optional[uuid.UUID] = None

class RecipeTag(LowercaseBaseModel):
    id: uuid.UUID
    name: str
    creator: UserResponse
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

class RecipeTagResponse(LowercaseBaseModel):
    detail: str
    recipe_tag: RecipeTag

class RecipeTagsResponse(LowercaseBaseModel):
    detail: str
    recipe_tags: List[RecipeTag]