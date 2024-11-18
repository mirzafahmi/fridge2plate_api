from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
import uuid
from typing import Optional


class RecipeOriginBase(LowercaseBaseModel):
    name: str


class RecipeOriginCreate(RecipeOriginBase):
    ...

class RecipeOriginCreateSeeder(RecipeOriginCreate):
    id: Optional[uuid.UUID] = None

class RecipeOrigin(RecipeOriginBase):
    id: uuid.UUID
    created_date: datetime
    updated_date: datetime

    class ConfigDict:
        from_attributes = True


class RecipeOriginCreatedResponse(LowercaseBaseModel):
    result: str
    data: RecipeOrigin