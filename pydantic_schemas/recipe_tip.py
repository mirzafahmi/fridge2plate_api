from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any, Text, Union
from uuid import UUID
from pydantic import validator, constr


class RecipeTipBase(LowercaseBaseModel):
    description: List[str]

    model_config = {
        "transform_fields": ["description"]
    }

    @validator("description")
    def validate_description(cls, value):
        if value is None:
            return ValueError("Recipe Tip Descriptions cannot be null.")
        if not isinstance(value, list):
            raise ValueError("Recipe Tip Descriptions must be a list of strings.")
        lowercased_tips = []
        for tip in value:
            if not isinstance(tip, str) or not tip.strip():
                raise ValueError("Each Recipe Tip Description must be a non-empty string.")
            if len(tip) < 3:
                raise ValueError("String should have at least 3 characters")
            lowercased_tips.append(tip.lower())
        return lowercased_tips

class RecipeTipCreate(RecipeTipBase):
    recipe_id: UUID

class RecipeTipCreateSeeder(RecipeTipCreate):
    id: Optional[UUID] = None

class RecipeTipUpdate(LowercaseBaseModel):
    description: constr(strip_whitespace=True, min_length=3)

    model_config = {
        "transform_fields": ["description"]
    }

class RecipeTip(LowercaseBaseModel):
    id: UUID
    description: Text
    recipe_id: UUID

    class Config:
        from_attributes = True

class RecipeTipLite(LowercaseBaseModel):
    description: Text
    recipe_id: UUID

    class Config:
        from_attributes = True

class RecipeTipsByRecipe(LowercaseBaseModel):
    recipe_id: UUID
    recipe_tips: List[RecipeTip]

    def model_post_init(self, __context: Any) -> None:
        self.tips = sorted(
            self.tips, 
            key=lambda tip: (tip.recipe_id, tip.description)
        )

class RecipeTipResponse(LowercaseBaseModel):
    detail: str
    recipe_tip: RecipeTip

class RecipeTipsResponse(LowercaseBaseModel):
    detail: str
    recipe_tips: List[RecipeTip]
