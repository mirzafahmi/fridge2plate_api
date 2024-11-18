from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
import uuid
from typing import Optional


class UOMBase(LowercaseBaseModel):
    name: str
    unit: str
    weightage: float


class UOMCreate(UOMBase):
    ...

class UOMCreateSeeder(UOMCreate):
    id: Optional[uuid.UUID] = None

class UOM(UOMBase):
    id: uuid.UUID
    created_date: datetime
    updated_date: datetime

    class ConfigDict:
        from_attributes = True

class UOMCreatedResponse(LowercaseBaseModel):
    result: str
    data: UOM