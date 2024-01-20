from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional
from pydantic_schemas.ingredient_category import IngredientCategory



class IngredientCreate(LowercaseBaseModel):
    name: str
    brand: str
    is_essential: bool
    ingredient_category: str


class IngredientUpdate(LowercaseBaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    is_essential: Optional[bool] = None
    ingredient_category: Optional[str] = None


class Ingredient(IngredientCreate):
    id: int
    create_date: datetime
    update_date: datetime
    ingredient_category: Optional[IngredientCategory]

    class Config:
        orm_mode = True


class IngredientCreatedResponse(LowercaseBaseModel):
    result: str
    data: Ingredient

    class Config:
        orm_mode = True

