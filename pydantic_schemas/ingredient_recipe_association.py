from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any
import uuid 

from pydantic_schemas.ingredient import Ingredient
from pydantic_schemas.uom import UOM


class IngredientRecipeAssociationBase(LowercaseBaseModel):
    ingredient_id: uuid.UUID
    quantity: float
    uom_id: uuid.UUID
    is_essential: bool

class IngredientRecipeAssociationCreateSeeder(IngredientRecipeAssociationBase):
    id: Optional[uuid.UUID] = None

class IngredientRecipeAssociation(LowercaseBaseModel):
    id: uuid.UUID
    ingredient: Ingredient
    quantity: float
    uom: UOM
    is_essential: bool
    
    class ConfigDict:
        from_attributes = True