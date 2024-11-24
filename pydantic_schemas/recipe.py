from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any
from uuid import UUID
from pydantic import constr, validator, Field, root_validator
import re

from pydantic_schemas.recipe_category import RecipeCategory, RecipeCategoryLite
from pydantic_schemas.recipe_tag import RecipeTag, RecipeTagLite
from pydantic_schemas.recipe_origin import RecipeOrigin, RecipeOriginLite
from pydantic_schemas.ingredient import Ingredient
from pydantic_schemas.ingredient_recipe_association import *
from .user import UserResponse, UserResponseLite
from .instruction import InstructionCreate, Instruction, InstructionLite
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

    model_config = {
        "transform_fields": ["name", "serving", "cooking_time"]
    }

    @validator('serving')
    def validate_serving(cls, value):
        if re.match(r'^\d+$', value):
            return value
        elif re.match(r'^\d+-\d+$', value):
            return value
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
    ingredient_data: List[IngredientRecipeAssociation]  
    
    creator: Optional[UserResponse]
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

    #to sort steps list
    def model_post_init(self, __context: Any) -> None:
        self.steps = sorted(self.steps, key=lambda step: step.step_number)
        self.recipe_tags = sorted(self.recipe_tags, key=lambda recipe_tag: recipe_tag.name)
        self.ingredient_data = sorted(self.ingredient_data, key=lambda ingredient: ingredient.ingredient.name)

class RecipeLite(LowercaseBaseModel):
    id: UUID
    name: str
    serving: str
    cooking_time: str
    steps: List[InstructionLite] 
    images: List[RecipeImage] 
    recipe_category: RecipeCategoryLite
    recipe_origin: RecipeOriginLite
    recipe_tags: List[RecipeTagLite]
    ingredient_data: List[IngredientRecipeAssociationLite]  

    creator: Optional[UserResponseLite]
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

    def model_post_init(self, __context: Any) -> None:
        self.steps = sorted(self.steps, key=lambda step: step.step_number)
        self.recipe_tags = sorted(self.recipe_tags, key=lambda recipe_tag: recipe_tag.name)
        self.ingredient_data = sorted(self.ingredient_data, key=lambda ingredient: ingredient.ingredient.name)

class RecipeResponse(LowercaseBaseModel):
    detail: str
    recipe: Recipe

class RecipeLiteResponse(LowercaseBaseModel):
    detail: str
    recipe: RecipeLite

class RecipesResponse(LowercaseBaseModel):
    detail: str
    recipes: List[Recipe]

class RecipesLiteResponse(LowercaseBaseModel):
    detail: str
    recipes: List[RecipeLite]
    