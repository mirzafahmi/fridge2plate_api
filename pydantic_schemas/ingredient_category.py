from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime


class IngredientCategoryBase(LowercaseBaseModel):
    name: str

class IngredientCategoryCreate(IngredientCategoryBase):
    ...

class IngredientCategory(IngredientCategoryBase):
    id: int
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True

class IngredientCategoryCreatedResponse(LowercaseBaseModel):
    result: str
    data: IngredientCategory