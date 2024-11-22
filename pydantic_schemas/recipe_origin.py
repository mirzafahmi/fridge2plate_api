from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
import uuid
from typing import List, Optional
from pydantic import constr

from .user import UserResponse


class RecipeOriginBase(LowercaseBaseModel):
    name: constr(strip_whitespace=True, min_length=3)
    created_by: Optional[uuid.UUID] = None

class RecipeOriginCreate(RecipeOriginBase):
    ...

class RecipeOriginUpdate(RecipeOriginBase):
    name: Optional[constr(strip_whitespace=True, min_length=3)] = None
    created_by: Optional[uuid.UUID] = None
    
class RecipeOriginCreateSeeder(RecipeOriginCreate):
    id: Optional[uuid.UUID] = None

class RecipeOrigin(LowercaseBaseModel):
    id: uuid.UUID
    name: str
    creator: UserResponse
    created_date: datetime
    updated_date: datetime

    class ConfigDict:
        from_attributes = True

class RecipeOriginResponse(LowercaseBaseModel):
    detail: str
    recipe_origins: RecipeOrigin

class RecipeOriginsResponse(LowercaseBaseModel):
    detail: str
    recipe_origins: List[RecipeOrigin]