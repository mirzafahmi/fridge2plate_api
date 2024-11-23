from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import constr

from pydantic_schemas.ingredient_category import IngredientCategory
from .user import UserResponse


class IngredientCreate(LowercaseBaseModel):
    name: constr(strip_whitespace=True, min_length=3)
    brand: constr(strip_whitespace=True, min_length=3)
    ingredient_category_id: UUID
    icon: Optional[str] = None
    created_by: Optional[UUID] = None

    model_config = {
        "transform_fields": ["name", "brand"]
    }

class IngredientCreateSeeder(IngredientCreate):
    id: Optional[UUID] = None
    
class IngredientUpdate(LowercaseBaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=3)] = None
    brand: Optional[constr(strip_whitespace=True, min_length=3)] = None
    ingredient_category_id: Optional[UUID] = None
    icon: Optional[str] = None
    created_by: Optional[UUID] = None

    model_config = {
        "transform_fields": ["name", "brand"]
    }

class Ingredient(LowercaseBaseModel):
    id: UUID
    name: str
    brand: str
    icon: Optional[str] = None
    ingredient_category: IngredientCategory
    creator: UserResponse
    created_date: datetime
    updated_date: datetime
    
    class Config:
        from_attributes = True

class IngredientResponse(LowercaseBaseModel):
    detail: str
    ingredient: Ingredient


class IngredientsResponse(LowercaseBaseModel):
    detail: str
    ingredients: List[Ingredient]

