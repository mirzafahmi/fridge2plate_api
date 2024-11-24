from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any
import uuid 

from pydantic_schemas.ingredient import Ingredient, IngredientLite
from pydantic_schemas.uom import UOM, UOMLite


class IngredientRecipeAssociationBase(LowercaseBaseModel):
    ingredient_id: uuid.UUID
    quantity: float
    uom_id: uuid.UUID
    is_essential: bool

class IngredientRecipeAssociationCreateSeeder(IngredientRecipeAssociationBase):
    id: Optional[uuid.UUID] = None

class IngredientRecipeAssociation(LowercaseBaseModel):
    id: uuid.UUID
    recipe_id: uuid.UUID
    ingredient: Ingredient
    quantity: float
    uom: UOM
    is_essential: bool

    created_date: datetime
    updated_date: datetime
    
    class Config:
        from_attributes = True

class IngredientRecipeAssociationLite(LowercaseBaseModel):
    recipe_id: uuid.UUID
    ingredient: IngredientLite
    quantity: float
    uom: UOMLite
    is_essential: bool
    
    class Config:
        from_attributes = True

class IngredientRecipeAssociationResponse(LowercaseBaseModel):
    detail: str
    ingredient_recipe_association: IngredientRecipeAssociation

class IngredientRecipeAssociationsResponse(LowercaseBaseModel):
    detail: str
    ingredient_recipe_associations: List[IngredientRecipeAssociation]

class IngredientRecipeAssociationResponseLite(LowercaseBaseModel):
    detail: str
    ingredient_recipe_association: IngredientRecipeAssociationLite

class IngredientRecipeAssociationsResponseLite(LowercaseBaseModel):
    detail: str
    ingredient_recipe_associations: List[IngredientRecipeAssociationLite]