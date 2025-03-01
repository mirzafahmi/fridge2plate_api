from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from uuid import UUID

from db.db_setup import get_db
from utils.user import get_user_by_email, get_user_by_username, post_user, get_user_by_id
from utils.follower import get_follow_counts, get_follow_stats
from utils.auth import authenticate_user, create_jwt_token, get_current_user
from utils.recipe_user_association import get_user_interactions
from pydantic_schemas.user import UserMessageResponse, UserCreate, AuthResponse


router = APIRouter(
    prefix='/auth',
    tags=["User Authetication"]
)

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

    user_follow_counts = get_follow_counts(db, [user_id])
    count = user_follow_counts.get(user_id, {})
    user_db.followers_count = count.get("followers_count", 0)
    user_db.followings_count = count.get("followings_count", 0)

    return {
        "detail": "User data retrieved successfully", 
        "user": user_db
    }