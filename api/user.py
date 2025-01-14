from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from db.db_setup import get_db
from pydantic_schemas.user import UserResponse, UserMessageResponse, UsersMessageResponse, UserCreate, UserUpdate, UserLogin, AuthResponse
from pydantic_schemas.recipe_user_association import RecipeUserAssociationResponse, RecipeUserAssociationsResponse
from db.models.user import User
from utils.user import get_user, get_user_by_id, get_user_by_email, get_user_by_username, get_current_user, post_user, put_user, authenticate_user, create_jwt_token, decode_jwt_token
from utils.recipe_user_association import get_cooked_recipes, get_bookmarked_recipes, get_liked_recipes, get_user_interactions, get_users_interactions

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

    user_interaction = get_user_interactions(db, user_create.id)
    user_create.cooked_count = user_interaction.get("cooked_count", 0)
    user_create.bookmarked_count = user_interaction.get("bookmarked_count", 0)
    user_create.liked_count = user_interaction.get("liked_count", 0)
    
    return {
        "detail": "User created successfully", 
        "user": user_create
    }

@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthResponse)
async def auth_user(*, db: Session = Depends(get_db), user: OAuth2PasswordRequestForm = Depends()):

    user_login = authenticate_user(db, user)

    if not user_login:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )

    jwt_token = create_jwt_token(data={"sub": user_login.id, "email": user_login.email})

    return {
        "detail": "Login successful", 
        "token_type": "bearer", 
        "access_token": jwt_token
    }

@router.get("/validate", response_model=UserMessageResponse)
async def retrieve_current_user(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = UUID(current_user["sub"])
    user_db = get_user_by_id(db, user_id)

    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found"
        )

    user_interaction = get_user_interactions(db, user_id)
    user_db.cooked_count = user_interaction.get("cooked_count", 0)
    user_db.bookmarked_count = user_interaction.get("bookmarked_count", 0)
    user_db.liked_count = user_interaction.get("liked_count", 0)

    return {
        "detail": "User data retrieved successfully", 
        "user": user_db
    }

@router.patch("/profile/update", response_model=UserMessageResponse)
async def update_profile(user_update: UserUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = UUID(current_user["sub"])
    user_db = get_user_by_id(db, user_id)

    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found"
        )# why tf 401 instead of 404

    updated_user = put_user(db, user, user_update)

    user_interaction = get_user_interactions(db, user_id)
    updated_user.cooked_count = user_interaction.get("cooked_count", 0)
    updated_user.bookmarked_count = user_interaction.get("bookmarked_count", 0)
    updated_user.liked_count = user_interaction.get("liked_count", 0)

    return {
        "detail": "User updated successfully", 
        "user": updated_user
    }

@router.get("/users/{email}", response_model=UserMessageResponse)
async def retrieve_user_by_email(email: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_db = get_user_by_email(db, email)

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    user_interaction = get_user_interactions(db, user_db.id)
    user_db.cooked_count = user_interaction.get("cooked_count", 0)
    user_db.bookmarked_count = user_interaction.get("bookmarked_count", 0)
    user_db.liked_count = user_interaction.get("liked_count", 0)

    return {
            "detail": f"{email} user data retrieved successfully", 
            "user": user_db
        }

@router.get("/users/{user_id}/cooked", status_code=status.HTTP_200_OK, response_model=RecipeUserAssociationsResponse)
async def retrieve_cooked_recipe(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), user_id: UUID):
    db_user = get_user_by_id(db, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {user_id} as User is not found"
        )

    recipe_user_assocs = get_cooked_recipes(db, user_id)

    if not recipe_user_assocs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Cooked recipe list for ID {user_id} of User is empty"
        )

    return {
        "detail": f"ID {user_id} as User's cooked Recipe list is retrieved successfully",
        "recipe_user_associations": recipe_user_assocs
    }

@router.get("/users/{user_id}/bookmarked", status_code=status.HTTP_200_OK, response_model=RecipeUserAssociationsResponse)
async def retrieve_bookmarked_recipe(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), user_id: UUID):
    db_user = get_user_by_id(db, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {user_id} as User is not found"
        )

    recipe_user_assocs = get_bookmarked_recipes(db, user_id)

    if not recipe_user_assocs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Bookmarked recipe list for ID {user_id} of User is empty"
        )

    return {
        "detail": f"ID {user_id} as User's bookmarked Recipe list is retrieved successfully",
        "recipe_user_associations": recipe_user_assocs
    }

@router.get("/users/{user_id}/liked", status_code=status.HTTP_200_OK, response_model=RecipeUserAssociationsResponse)
async def retrieve_liked_recipe(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), user_id: UUID):
    db_user = get_user_by_id(db, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {user_id} as User is not found"
        )

    recipe_user_assocs = get_liked_recipes(db, user_id)

    if not recipe_user_assocs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Liked recipe list for ID {user_id} of User is empty"
        )

    return {
        "detail": f"ID {user_id} as User's liked Recipe list is retrieved successfully",
        "recipe_user_associations": recipe_user_assocs
    }

@router.get("/users", response_model=UsersMessageResponse)
async def retrieve_user(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    users_db = get_user(db)

    if not users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Users list are empty"
        )

    user_ids = [user.id for user in users_db]

    users_interactions = get_users_interactions(db, user_ids)
    
    for user_db in users_db:
        counts = users_interactions.get(user_db.id, {})
        user_db.cooked_count = counts.get("cooked_count", 0)
        user_db.bookmarked_count = counts.get("bookmarked_count", 0)
        user_db.liked_count = counts.get("liked_count", 0)

    return {
            "detail": f"Users data retrieved successfully", 
            "users": users_db
        }
