from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any, Text, Union
from uuid import UUID 
from pydantic import HttpUrl, validator


class RecipeImageBase(LowercaseBaseModel):
    image: Union[str, List[Union[HttpUrl, str]]]

    model_config = {
        "transform_fields": []
    }

    @validator("image")
    def validate_image(cls, value):
        if value is None:
            return value

        if isinstance(value, str):
            if not value.strip():
                raise ValueError("Image must not be an empty string.")
            if len(value) < 1:
                raise ValueError("Image must be at least 1 character long.")

        elif isinstance(value, list):
            for item in value:
                if not isinstance(item, (str, HttpUrl)):
                    raise ValueError("Each item in the image list must be a valid string or URL.")
                if isinstance(item, str) and not item.strip():
                    raise ValueError("Each image in the list must not be an empty string.")
                if isinstance(item, str) and len(item) < 1:
                    raise ValueError("Each image in the list must be at least 1 character long.")

        else:
            raise ValueError("Image must be either a string or a list of strings/URLs.")

        return value

class RecipeImageCreate(RecipeImageBase):
    image: List[Union[HttpUrl, str]]
    recipe_id: UUID

class RecipeImageCreateSeeder(RecipeImageCreate):
    id: Optional[UUID] = None

class RecipeImage(LowercaseBaseModel):
    id: UUID
    image: str
    recipe_id: UUID

    class Config:
        from_attributes = True

class RecipeImageUpdate(RecipeImageBase):
    image: Optional[Union[HttpUrl, str]] = None
    recipe_id: Optional[UUID] = None

class RecipeImageResponse(LowercaseBaseModel):
    detail: str
    recipe_image: RecipeImage

class RecipeImagesResponse(LowercaseBaseModel):
    detail: str
    recipe_images: List[RecipeImage]

    def model_post_init(self, __context: Any) -> None:
            self.recipe_images = sorted(
                self.recipe_images, 
                key=lambda img: (img.recipe_id, img.image)
            )

class RecipeImagesByRecipe(RecipeImagesResponse):
    recipe_id: UUID
    recipe_images: List[RecipeImage]