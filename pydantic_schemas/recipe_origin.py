from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime


class RecipeOriginBase(LowercaseBaseModel):
    name: str


class RecipeOriginCreate(RecipeOriginBase):
    ...


class RecipeOrigin(RecipeOriginBase):
    id: int
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True


class RecipeOriginCreatedResponse(LowercaseBaseModel):
    result: str
    data: RecipeOrigin