from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional
from pydantic_schemas.ingredient_category import IngredientCategory
import uuid


class IngredientCreate(LowercaseBaseModel):
    name: str
    brand: str
    ingredient_category_id: str
    icon: Optional[str] = None

class IngredientCreateSeeder(IngredientCreate):
    id: Optional[uuid.UUID] = None
    
class IngredientUpdate(LowercaseBaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    ingredient_category_id: Optional[str] = None
    icon: Optional[str] = None

class Ingredient(IngredientCreate):
    id: uuid.UUID
    created_date: datetime
    updated_date: datetime
    ingredient_category_id: Optional[IngredientCategory]

    class ConfigDict:
        from_attributes = True

class IngredientCreatedResponse(LowercaseBaseModel):
    result: str
    data: Ingredient

    class ConfigDict:
        from_attributes = True

