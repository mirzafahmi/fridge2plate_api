from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any
from uuid import UUID

from pydantic_schemas.recipe_tag import RecipeTagLite

class RecipeTagRecipeAssociationBase(LowercaseBaseModel):
    recipe_tag_id: UUID

class RecipeTagRecipeAssociationCreate(RecipeTagRecipeAssociationBase):
    recipe_id: UUID

class RecipeTagRecipeAssociationUpdate(RecipeTagRecipeAssociationBase):
    recipe_tag_id: Optional[UUID] = None

class RecipeTagRecipeAssociationLite(LowercaseBaseModel):
    recipe_id: UUID
    recipe_tag: RecipeTagLite    

class RecipeTagRecipeAssociation(LowercaseBaseModel):
    id: UUID
    recipe_id: UUID
    recipe_tag: RecipeTagLite 

class RecipeTagRecipeAssociationResponse(LowercaseBaseModel):
    detail: str
    recipe_tag_recipe_association: RecipeTagRecipeAssociation
    
class RecipeTagRecipeAssociationsResponse(LowercaseBaseModel):
    detail: str
    recipe_tag_recipe_associations: List[RecipeTagRecipeAssociation]

    def model_post_init(self, __context: Any) -> None:
        self.recipe_tag_recipe_associations = sorted(
            self.recipe_tag_recipe_associations, 
            key=lambda assoc: (assoc.recipe_id, assoc.recipe_tag.name)
        )

class RecipeTagRecipeAssociationsLiteResponse(RecipeTagRecipeAssociationsResponse):
    detail: str
    recipe_tag_recipe_associations: List[RecipeTagRecipeAssociationLite]
