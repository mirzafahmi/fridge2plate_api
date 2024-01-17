from pydantic import BaseModel
from typing import Any

class LowercaseBaseModel(BaseModel):
    class Config:
        # This config setting makes Pydantic case-insensitive
        case_sensitive = False

    def __init__(self, **data: Any) -> None:
        # Convert all keys in data to lowercase
        data_lower = {key.lower(): value for key, value in data.items()}
        super().__init__(**data_lower)

