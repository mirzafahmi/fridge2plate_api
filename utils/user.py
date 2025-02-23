from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, WebSocket
from jose import jwt, JWTError
from fastapi import HTTPException, status

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional
import base64
from uuid import UUID

from db.models.user import User
from pydantic_schemas.user import UserCreate, UserUpdate, UserLogin


def get_user(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, user_username: str):
    return db.query(User).filter(func.lower(User.username) == user_username).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.email == user_email).first()

def check_valid_user(db: Session, data):
    if data.dict().get('created_by') is not None:
        if not get_user_by_id(db, data.created_by):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Id {data.created_by} as User is not found"
            )

def check_creator(db: Session, current_user: dict, data):
    user_id = current_user.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user data: 'sub' not found."
        )

    if user_id != data.created_by:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail=f"Id {user_id} as User is not an creator"
            )

def post_user(db: Session, user: UserCreate):
    from utils.auth import bcrypt_context
    
    if user.dict().get('id') is not None:
        db_user = User(
            id=user.id,
            username=user.username,
            email=user.email,
            password=bcrypt_context.hash(user.password)
        )
    else: 
        db_user = User(
            username=user.username,
            email=user.email,
            password=bcrypt_context.hash(user.password)
        )

    db.add(db_user)
    db.commit()

    db.refresh(db_user)

    return db_user

def put_user(db: Session, user: User, user_update: UserUpdate):
    #TODO! check duplicate
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.password is not None:
        user.password = bcrypt_context.hash(user_update.password)
    
    db.commit()

    return user
