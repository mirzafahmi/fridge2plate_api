from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from db.db_setup import get_db
from pydantic_schemas.user import UserResponse, UserMessageResponse, UsersMessageResponse, UserUpdate, UserFollowerListResponse, UserFollowingListResponse
from pydantic_schemas.recipe_user_association import RecipeUserAssociationResponse, RecipeUserAssociationsResponse
from db.models.user import User
from utils.user import get_user, get_user_by_id, get_user_by_email, get_user_by_username, put_user
from utils.auth import get_current_user
from utils.recipe_user_association import get_cooked_recipes, get_bookmarked_recipes, get_liked_recipes, get_user_interactions, get_users_interactions
from utils.follower import * 

from datetime import timedelta, datetime
from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(
    prefix='/users',
    tags=["User Details"]
)

@router.get("/", response_model=UsersMessageResponse)
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

@router.get("/by_email/{email}", response_model=UserMessageResponse)
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

@router.get("/{user_id}", response_model=UserMessageResponse)
async def retrieve_user_by_id(user_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    print(f"Searching for user with ID: {user_id}")
    user_db = get_user_by_id(db, user_id)
    print(f"Found user: {user_db}")
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
            "detail": f"ID {user_id} of user data retrieved successfully", 
            "user": user_db
        }

@router.get("/{user_id}/cooked", status_code=status.HTTP_200_OK, response_model=RecipeUserAssociationsResponse)
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

@router.get("/{user_id}/bookmarked", status_code=status.HTTP_200_OK, response_model=RecipeUserAssociationsResponse)
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

@router.get("/{user_id}/liked", status_code=status.HTTP_200_OK, response_model=RecipeUserAssociationsResponse)
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

@router.post("/follow/{following_id}")
def follow_unfollow_user(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), following_id: UUID):
    user_id = UUID(current_user['sub'])

    return {"detail": f"ID {user_id} of user {toggle_follow(db, user_id, following_id)} ID {following_id}"}

@router.get("/followers/", status_code=status.HTTP_200_OK, response_model=UserFollowerListResponse)
@router.get("/followers/{user_id}", status_code=status.HTTP_200_OK, response_model=UserFollowerListResponse)
def list_followers(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), user_id: UUID = None, limit: int = 10, offset: int = 0):
    target_user_id = user_id if user_id else UUID(current_user['sub'])
    followers = get_followers(db, target_user_id, limit, offset)
    total_count = get_followers_count(db, target_user_id)
    
    result = [
        UserResponse(**user.__dict__, is_following=is_following)
        for user, is_following in followers
    ]

    return {"total_count": total_count, "followers": result}

@router.get("/followings/", status_code=status.HTTP_200_OK, response_model=UserFollowingListResponse)
@router.get("/followings/{user_id}", status_code=status.HTTP_200_OK, response_model=UserFollowingListResponse)
def list_following(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), user_id: UUID = None, limit: int = 10, offset: int = 0):
    target_user_id = user_id if user_id else UUID(current_user['sub'])
    followings = get_following(db, target_user_id, limit, offset)
    total_count = get_following_count(db, target_user_id)

    result = [
        UserResponse(**user.__dict__, is_following=is_following)
        for user, is_following in followings
    ]

    return {"total_count": total_count, "followings": result}
