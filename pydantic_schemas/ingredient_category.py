from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
import uuid
from typing import List, Optional
from pydantic import constr

from .user import UserResponse


class IngredientCategoryBase(LowercaseBaseModel):
    name: constr(strip_whitespace=True, min_length=3)
    created_by: Optional[uuid.UUID] = None

class IngredientCategoryCreate(IngredientCategoryBase):
    ...

class IngredientCategoryUpdate(LowercaseBaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=3)] = None
    created_by: Optional[uuid.UUID] = None

class IngredientCategoryCreateSeeder(IngredientCategoryCreate):
    id: Optional[uuid.UUID] = None
    
class IngredientCategory(LowercaseBaseModel):
    id: uuid.UUID
    name: str
    creator: UserResponse
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes=True

class IngredientCategoryResponse(LowercaseBaseModel):
    detail: str
    ingredient_category: IngredientCategory

class IngredientCategoriesResponse(LowercaseBaseModel):
    detail: str
    ingredient_categories: List[IngredientCategory]