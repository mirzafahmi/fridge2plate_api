from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr, validator
import uuid

from .lowercase_base_model import LowercaseBaseModel


class UserCreate(LowercaseBaseModel):
    username: constr(strip_whitespace=True, min_length=5)
    email: EmailStr
    password: constr(strip_whitespace=True, min_length=5)

    @validator("username")
    def normalize_username(cls, value):
        # Convert to lowercase and remove spaces
        return value.lower().replace(" ", "")

class UserCreateSeeder(UserCreate):
    id: Optional[uuid.UUID] = None

class UserUpdate(LowercaseBaseModel):
    username: Optional[constr(strip_whitespace=True, min_length=5)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(strip_whitespace=True, min_length=5)] = None

class UserResponse(LowercaseBaseModel):
    id: uuid.UUID
    username: str
    email: str
    created_date: datetime
    updated_date: datetime

    class ConfigDict:
        from_attributes = True

class UserMessageResponse(LowercaseBaseModel):
    message: str
    user: UserResponse

class UsersMessageResponse(LowercaseBaseModel):
    message: str
    users: List[UserResponse]

class UserLogin(LowercaseBaseModel):
    email: EmailStr
    password: constr(strip_whitespace=True, min_length=5)

class AuthResponse(LowercaseBaseModel):
    message: str
    token_type: str
    access_token: str