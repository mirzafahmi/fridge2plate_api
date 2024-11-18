from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
import uuid
from typing import Optional


class RecipeTagBase(LowercaseBaseModel):
    name: str


class RecipeTagCreate(RecipeTagBase):
    ...

class RecipeTagCreateSeeder(RecipeTagCreate):
    id: Optional[uuid.UUID] = None

class RecipeTag(RecipeTagBase):
    id: uuid.UUID
    created_date: datetime
    updated_date: datetime

    class ConfigDict:
        from_attributes = True


class RecipeTagCreatedResponse(LowercaseBaseModel):
    result: str
    data: RecipeTag