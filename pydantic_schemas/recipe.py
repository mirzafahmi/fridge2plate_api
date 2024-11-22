from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any
import uuid

from pydantic_schemas.recipe_category import RecipeCategory
from pydantic_schemas.recipe_tag import RecipeTag
from pydantic_schemas.recipe_origin import RecipeOrigin
from pydantic_schemas.ingredient import Ingredient
from pydantic_schemas.ingredient_recipe_association import *



class RecipeUpdate(LowercaseBaseModel):
    name: Optional[str] = None
    serving: Optional[int] = None
    cooking_time: Optional[str] = None
    author: Optional[str] = None
    instructions: Optional[str] = None
    recipe_category_id: Optional[int] = None
    recipe_tag_id: Optional[int] = None
    recipe_origin_id: Optional[int] = None
    ingredients: Optional[List[IngredientRecipeAssociationBase]]

class RecipeBase(LowercaseBaseModel):
    ...

class RecipeCreate(LowercaseBaseModel):
    name: str
    serving: int
    cooking_time: str
    author: str
    instructions: str
    recipe_category: str
    recipe_tag: str
    recipe_origin: str
    ingredients: List[IngredientRecipeAssociationBase]

class RecipeCreateSeeder(RecipeCreate):
    id: Optional[uuid.UUID] = None

class Recipe(LowercaseBaseModel):
    id: uuid.UUID
    name: str
    serving: int
    cooking_time: str
    author: str
    instructions: str
    recipe_category: Optional[RecipeCategory]
    recipe_tag: Optional[RecipeTag]
    recipe_origin: Optional[RecipeOrigin]
    ingredients_recipe_associations: List[IngredientRecipeAssociation]

    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True


class RecipeCreatedResponse(LowercaseBaseModel):
    result: str
    data: Recipe