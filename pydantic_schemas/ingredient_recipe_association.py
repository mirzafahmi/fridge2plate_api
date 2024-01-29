from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any

from pydantic_schemas.ingredient import Ingredient
from pydantic_schemas.uom import UOM


class IngredientRecipeAssociationBase(LowercaseBaseModel):
    ingredient: str
    quantity: int
    uom: str


class IngredientRecipeAssociation(LowercaseBaseModel):
    id: int
    ingredient: Ingredient
    uom: UOM
    quantity: int
    
    class Config:
        orm_mode = True