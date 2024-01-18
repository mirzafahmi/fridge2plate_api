from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime


class RecipeBase(LowercaseBaseModel):
    name: str
    serving: int
    cooking_time: str
    author: str
    instuctions: str
    recipe_category_id: int
    recipe_tag_id: int
    recipe_origin_id: int
    Recipes: List[int]


class RecipeCreate(RecipeBase):
    ...


class Recipe(RecipeBase):
    id: int
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True


class RecipeCreatedResponse(LowercaseBaseModel):
    result: str
    data: Recipe