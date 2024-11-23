from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
import uuid
from typing import List, Optional
from pydantic import constr, Field

from .user import UserResponse


class UOMBase(LowercaseBaseModel):
    name: constr(strip_whitespace=True, min_length=3)
    unit: constr(strip_whitespace=True, min_length=1)
    weightage: float = Field(..., gt=0)
    created_by: Optional[uuid.UUID] = None

    model_config = {
        "transform_fields": ["name"]
    }
class UOMCreate(UOMBase):
    ...

class UOMUpdate(LowercaseBaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=3)] = None
    unit: Optional[constr(strip_whitespace=True, min_length=1)] = None
    weightage: Optional[float] = None
    created_by: Optional[uuid.UUID] = None

    model_config = {
        "transform_fields": ["name"]
    }

class UOMCreateSeeder(UOMCreate):
    id: Optional[uuid.UUID] = None

class UOM(LowercaseBaseModel):
    id: uuid.UUID
    name: str
    unit: str
    weightage: float
    creator: UserResponse
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

class UOMResponse(LowercaseBaseModel):
    detail: str
    uom: UOM

class UOMsResponse(LowercaseBaseModel):
    detail: str
    uoms: List[UOM]