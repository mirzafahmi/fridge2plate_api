from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional

class IngredientCaegoryBase(LowercaseBaseModel):
    ingredient_category: str

class IngredientBase(LowercaseBaseModel):
    name: str
    brand: str
    is_essential: bool
    ingredient_category_id: int
    ingredients: Optional[List[IngredientCaegoryBase]]


class IngredientCreate(IngredientBase):
    ...


class Ingredient(IngredientBase):
    id: int
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True


class IngredientCreatedResponse(LowercaseBaseModel):
    result: str
    data: Ingredient