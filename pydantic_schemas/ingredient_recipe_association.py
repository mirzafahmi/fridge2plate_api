from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any

from pydantic_schemas.ingredient import Ingredient
from pydantic_schemas.uom import UOM


class IngredientRecipeAssociationBase(LowercaseBaseModel):
    ingredient: str
    quantity: int
    uom: str


class IngredientRecipeAssociation(IngredientRecipeAssociationBase):
    id: int
    ingredient: Optional[Ingredient]
    uom: Optional[UOM]
    quantity: int
    
    class Config:
        orm_mode = True