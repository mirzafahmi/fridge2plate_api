from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any, Union
from uuid import UUID
from pydantic import constr, validator, Field, root_validator, HttpUrl
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
    name: constr(strip_whitespace=True, min_length=3)
    serving: constr(strip_whitespace=True, min_length=1)
    cooking_time: constr(strip_whitespace=True, min_length=1)
    recipe_category_id: UUID
    recipe_origin_id: UUID
    recipe_tags: List[UUID]
    ingredients: List[IngredientRecipeAssociationBase]
    steps: List[InstructionCreate]
    images: Optional[List[Union[HttpUrl, str]]] = None #TODO! convert images as list of str not as list of recipeimage obj
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
    
    @validator('cooking_time')
    def validate_cooking_time(cls, value):
        if re.match(r'^\d+\s+(minute|hour)s?$', value.strip(), re.IGNORECASE):
            return value
        raise ValueError('Cooking time must be in the format "X minute(s)" or "X hour(s)", where X is a number and "minute(s)" or "hour(s)" is the unit.')

    @validator('recipe_tags')
    def validate_recipe_tags(cls, value):
        if len(value) < 1:
            raise ValueError('At least one recipe tag (UUID) is required.')
        return value
    
    @validator("steps")
    def validate_steps(cls, steps):
        if not steps:
            raise ValueError("Steps cannot be an empty list.")
        
        step_numbers = sorted([step.step_number for step in steps])
        expected_sequence = list(range(1, len(step_numbers) + 1))
        if step_numbers != expected_sequence:
            raise ValueError(
                f"step_number values must start at 1 and be consecutive without gaps. "
                f"Provided: {step_numbers}, Expected: {expected_sequence}"
            )
        return steps

class RecipeCreate(RecipeBase):
    ...

class RecipeCreateSeeder(RecipeCreate):
    id: Optional[UUID] = None

class RecipeUpdate(RecipeBase):
    name: Optional[constr(strip_whitespace=True, min_length=3)] = None
    serving: Optional[constr(strip_whitespace=True, min_length=1)] = None
    cooking_time: Optional[constr(strip_whitespace=True, min_length=1)] = None
    recipe_category_id: Optional[UUID] = None
    recipe_origin_id: Optional[UUID] = None
    recipe_tags: Optional[List[UUID]] = None
    ingredients: Optional[List[IngredientRecipeAssociationBase]] = None
    created_by: Optional[UUID] = None
    steps: Optional[List[InstructionCreate]] = None
    images: Optional[List[Union[HttpUrl, str]]] = None

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
        self.images = sorted(self.images, key=lambda image: image.image)

class RecipeLite(Recipe):
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
    