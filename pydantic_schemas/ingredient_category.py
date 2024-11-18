from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
import uuid
from typing import Optional


class IngredientCategoryBase(LowercaseBaseModel):
    name: str

class IngredientCategoryCreate(IngredientCategoryBase):
    ...

class IngredientCategoryCreateSeeder(IngredientCategoryCreate):
    id: Optional[uuid.UUID] = None
    
class IngredientCategory(IngredientCategoryBase):
    id: uuid.UUID
    created_date: datetime
    updated_date: datetime

    class ConfigDict:
        from_attributes = True

class IngredientCategoryCreatedResponse(LowercaseBaseModel):
    result: str
    data: IngredientCategory