from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime


class RecipeCategoryBase(LowercaseBaseModel):
    name: str


class RecipeCategoryCreate(RecipeCategoryBase):
    ...


class RecipeCategory(RecipeCategoryBase):
    id: int
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True


class RecipeCategoryCreatedResponse(LowercaseBaseModel):
    result: str
    data: RecipeCategory