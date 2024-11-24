from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any
from uuid import UUID

from pydantic_schemas.recipe_tag import RecipeTagLite


class RecipeTagRecipeAssociationLite(LowercaseBaseModel):
    recipe_id: UUID
    recipe_tag: RecipeTagLite    

class RecipeTagRecipeAssociation(RecipeTagRecipeAssociationLite):
    id: UUID

class RecipeTagRecipeAssociationsResponse(LowercaseBaseModel):
    detail: str
    recipe_tag_recipe_associations: List[RecipeTagRecipeAssociation]

class RecipeTagRecipeAssociationsListResponse(LowercaseBaseModel):
    detail: str
    recipe_tag_recipe_associations: List[RecipeTagRecipeAssociation]

class RecipeTagRecipeAssociationsLiteResponse(LowercaseBaseModel):
    detail: str
    recipe_tag_recipe_associations: List[RecipeTagRecipeAssociationLite]

class RecipeTagRecipeAssociationsListLiteResponse(LowercaseBaseModel):
    detail: str
    recipe_tag_recipe_associations: List[RecipeTagRecipeAssociationLite]