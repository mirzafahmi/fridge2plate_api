from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime


class RecipeTagBase(LowercaseBaseModel):
    name: str


class RecipeTagCreate(RecipeTagBase):
    ...


class RecipeTag(RecipeTagBase):
    id: int
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True


class RecipeTagCreatedResponse(LowercaseBaseModel):
    result: str
    data: RecipeTag