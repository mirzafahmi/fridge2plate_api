from datetime import timedelta, datetime
from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends
from jose import jwt, JWTError
from fastapi import HTTPException, status

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional
from dotenv import load_dotenv
import os
import base64
from uuid import UUID

from db.models.user import User
from pydantic_schemas.user import UserCreate, UserUpdate, UserLogin

load_dotenv()


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
JWT_ALGORITHM = "RS256"
JWT_TOKEN_EXPIRE_MINUTES = 30

PRIVATE_KEY = base64.b64decode(os.getenv("PRIVATE_KEY")).decode("utf-8")
PUBLIC_KEY = base64.b64decode(os.getenv("PUBLIC_KEY")).decode("utf-8")

oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

def get_user(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: str):
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

def post_user(db: Session, user: UserCreate):
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

def authenticate_user(db: Session, user: UserLogin):
    user_db = get_user_by_email(db, user.username)

    if not user_db:
        return False
    
    if not bcrypt_context.verify(user.password, user_db.password):
        return False
    
    return user_db

def create_jwt_token(data: dict, expires_delta: timedelta = None):
    to_encode = {
        key: str(value) if isinstance(value, UUID) else value
        for key, value in data.items()
    }

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=JWT_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, PRIVATE_KEY, algorithm=JWT_ALGORITHM)

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[JWT_ALGORITHM])
        if "sub" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token payload missing 'sub' claim"
            )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token has expired"
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )

def get_current_user(token: str = Depends(oauth_bearer)):
    return decode_jwt_token(token)