from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from db.db_setup import get_db
from pydantic_schemas.user import UserResponse, UserMessageResponse, UsersMessageResponse, UserCreate, UserUpdate, UserLogin, AuthResponse
from db.models.user import User
from utils.user import get_user, get_user_by_id, get_user_by_email, get_user_by_username, get_current_user, post_user, put_user, authenticate_user, create_jwt_token, decode_jwt_token

from datetime import timedelta, datetime
from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    prefix='/auth',
    tags=["User Authetication"]
)

oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserMessageResponse)
async def add_user(*, db: Session = Depends(get_db), user: UserCreate):

    user_by_email = get_user_by_email(db, user.email)

    if user_by_email:
        raise HTTPException(
            status_code=400, 
            detail=f"{user.email} is already registered"
        )

    user_by_username = get_user_by_username(db, user.username)

    if user_by_username:
        raise HTTPException(
            status_code=400, 
            detail=f"{user.username} is already registered"
        )
    
    user_create = post_user(db, user)

    return {
        "detail": "User created successfully", 
        "user": UserResponse(
            id=user_create.id, 
            username=user_create.username, 
            email=user_create.email, 
            created_date=user_create.created_date, 
            updated_date=user_create.updated_date
        )
    }

@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthResponse)
async def auth_user(*, db: Session = Depends(get_db), user: OAuth2PasswordRequestForm = Depends()):

    user_login = authenticate_user(db, user)

    if not user_login:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    jwt_token = create_jwt_token(data={"sub": user_login.id, "email": user_login.email})

    return {
        "detail": "Login successful", 
        "token_type": "bearer", 
        "access_token": jwt_token
    }

@router.get("/validate", response_model=UserMessageResponse)
async def retrieve_current_user(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):

    user = get_user_by_id(db, UUID(current_user["sub"]))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found"
        )
    return {
        "detail": "User data retrieved successfully", 
        "user": UserResponse(
            id=user.id, 
            username=user.username, 
            email=user.email, 
            created_date=user.created_date, 
            updated_date=user.updated_date
        )
    }

@router.patch("/profile/update", response_model=UserMessageResponse)
async def update_profile(user_update: UserUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):

    user = get_user_by_id(db, payload["sub"])

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found"
        )

    updated_user = put_user(db, user, user_update)

    return {
        "detail": "User updated successfully", 
        "user": UserResponse(
            id=user_create.id, 
            username=user_create.username, 
            email=user_create.email, 
            created_date=user_create.created_date, 
            updated_date=user_create.updated_date
        )
    }

@router.get("/users/{email}", response_model=UserMessageResponse)
async def retrieve_user_by_email(email: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
            "detail": f"{email} user data retrieved successfully", 
            "user": UserResponse(
                id=user.id, 
                username=user.username, 
                email=user.email, 
                created_date=user.created_date, 
                updated_date=user.updated_date
            )
        }

@router.get("/users", response_model=UsersMessageResponse)
async def retrieve_user(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    users = get_user(db)

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users list are empty")

    return {
            "detail": f"Users data retrieved successfully", 
            "users": [
                UserResponse(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    created_date=user.created_date,
                    updated_date=user.updated_date
                ) for user in users
            ]
        }
