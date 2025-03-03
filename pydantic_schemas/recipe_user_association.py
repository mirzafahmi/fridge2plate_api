from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional
from pydantic import constr, Field
from enum import Enum

from .user import UserResponse
#from pydantic_schemas.recipe import RecipeLite

class RecipeAction(str, Enum):
    liked = "liked"
    bookmarked = "bookmarked"
    cooked = "cooked"

class ActionSchema(LowercaseBaseModel):
    action: RecipeAction

#TODO make it use recipe response for recipeuserassoc response
class RecipeUserAssociation(LowercaseBaseModel):
    id: UUID
    user_id: UUID
    recipe_id: UUID
    cooked: bool
    cooked_date: Optional[datetime]
    bookmarked: bool
    bookmarked_date: Optional[datetime]
    liked: bool
    liked_date: Optional[datetime]

    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

class RecipeUserAssociationV2(LowercaseBaseModel):
    id: Optional[UUID] = None
    user_id: UUID
    recipe_id: UUID
    cooked: bool = False
    cooked_date: Optional[datetime] = None
    bookmarked: bool = False
    bookmarked_date: Optional[datetime] = None
    liked: bool = False
    liked_date: Optional[datetime] = None

    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class RecipeUserAssociationResponse(LowercaseBaseModel):
    detail: str
    recipe_user_association: RecipeUserAssociation

class RecipeUserAssociationsResponse(LowercaseBaseModel):
    detail: str
    recipe_user_associations: List[RecipeUserAssociation]