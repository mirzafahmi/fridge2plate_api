from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import constr

from pydantic_schemas.ingredient_category import IngredientCategory, IngredientCategoryLite
from .user import UserResponse


class IngredientCreate(LowercaseBaseModel):
    name: constr(strip_whitespace=True, min_length=3)
    brand: constr(strip_whitespace=True, min_length=3)
    ingredient_category_id: UUID
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
    created_by: Optional[UUID] = None

    model_config = {
        "transform_fields": ["name", "brand"]
    }

class Ingredient(LowercaseBaseModel):
    id: UUID
    name: str
    brand: str
    ingredient_category: IngredientCategory
    creator: UserResponse
    created_date: datetime
    updated_date: datetime
    
    class Config:
        from_attributes = True

class IngredientLite(LowercaseBaseModel):
    name: str
    brand: str
    ingredient_category: IngredientCategoryLite
    
    class Config:
        from_attributes = True

class IngredientResponse(LowercaseBaseModel):
    detail: str
    ingredient: Ingredient


class IngredientsResponse(LowercaseBaseModel):
    detail: str
    ingredients: List[Ingredient]

