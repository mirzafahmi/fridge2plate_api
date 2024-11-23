from pydantic import BaseModel, Field, field_validator
from typing import Any

class LowercaseBaseModel(BaseModel):
    class Config:
        transform_fields = set() 

    @field_validator("*", mode="before")
    def convert_to_lowercase(cls, value, info):
        transform_fields = cls.model_config.get("transform_fields", [])

        if isinstance(value, str) and info.field_name in transform_fields:
            return value.lower()
        return value

