from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime


class UOMBase(LowercaseBaseModel):
    name: str
    unit: str
    weightage: float


class UOMCreate(UOMBase):
    ...

class UOM(UOMBase):
    id: int
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True

class UOMCreatedResponse(LowercaseBaseModel):
    result: str
    data: UOM