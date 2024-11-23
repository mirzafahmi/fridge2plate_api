from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any
from uuid import UUID
from pydantic import constr, validator
import re

from pydantic_schemas.recipe_category import RecipeCategory
from pydantic_schemas.recipe_tag import RecipeTag
from pydantic_schemas.recipe_origin import RecipeOrigin
from pydantic_schemas.ingredient import Ingredient
from pydantic_schemas.ingredient_recipe_association import *
from .user import UserResponse
from .instruction import InstructionCreate, Instruction
from .recipe_image import RecipeImageCreate, RecipeImage


class RecipeBase(LowercaseBaseModel):
    name: str
    serving: str
    cooking_time: str
    recipe_category_id: UUID
    recipe_origin_id: UUID
    recipe_tags: List[UUID]
    ingredients: List[IngredientRecipeAssociationBase]
    steps: List[InstructionCreate]
    images: Optional[List[RecipeImageCreate]] = None
    created_by: Optional[UUID] = None

    @validator('serving')
    def validate_serving(cls, value):
        # Check if the value is a number
        if re.match(r'^\d+$', value):
            return value
        # Check if the value is a range in the form 'number-number'
        elif re.match(r'^\d+-\d+$', value):
            return value
        # Raise an error if neither a single number nor a valid range
        raise ValueError('Serving must be a number or a valid range (e.g., "1-3")')

class RecipeCreate(RecipeBase):
    ...

class RecipeCreateSeeder(RecipeCreate):
    id: Optional[UUID] = None

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

class Recipe(LowercaseBaseModel):
    id: UUID
    name: str
    serving: str
    cooking_time: str
    steps: List[Instruction] 
    images: List[RecipeImage] 
    recipe_category: RecipeCategory
    recipe_origin: RecipeOrigin
    recipe_tags: List[RecipeTag]
    ingredients: List[Ingredient]
    
    creator: UserResponse
    created_date: datetime
    updated_date: datetime
    class Config:
        from_attributes = True


class RecipeResponse(LowercaseBaseModel):
    detail: str
    recipe: Recipe

class RecipesResponse(LowercaseBaseModel):
    detail: str
    recipes: List[Recipe]