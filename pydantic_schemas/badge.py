from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
import uuid
from typing import List, Optional, Union
from pydantic import constr, HttpUrl, validator, Field
import os
from dotenv import load_dotenv

from .user import UserResponse


load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")

class BadgeBase(LowercaseBaseModel):
    name: constr(strip_whitespace=True, min_length=3)
    description: Optional[constr(strip_whitespace=True, min_length=3)] = Field(default="")
    image: constr(strip_whitespace=True, min_length=3)
    created_by: Optional[uuid.UUID] = uuid.UUID(ADMIN_ID)

    model_config = {
        "transform_fields": ["name", "description", "image"]
    }


class BadgeCreate(BadgeBase):
    ...

class BadgeUpdate(BadgeBase):
    name: Optional[constr(strip_whitespace=True, min_length=3)] = None
    description: Optional[constr(strip_whitespace=True, min_length=3)] = None
    image: Optional[constr(strip_whitespace=True, min_length=3)] = None
    created_by: Optional[uuid.UUID] = None

class BadgeCreateSeeder(BadgeCreate):
    id: Optional[uuid.UUID] = None

class Badge(LowercaseBaseModel):
    id: uuid.UUID
    name: str
    description: str
    image: str
    creator: UserResponse
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes=True

class BadgeLite(LowercaseBaseModel):
    name: str
    description: str
    image: str

    class Config:
        from_attributes=True

class BadgeResponse(LowercaseBaseModel):
    detail: str
    badge: Badge

class BadgesResponse(LowercaseBaseModel):
    detail: str
    badges: List[Badge]