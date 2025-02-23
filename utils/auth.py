from dotenv import load_dotenv
import os
import base64
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, WebSocket, HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from uuid import UUID

from pydantic_schemas.user import UserLogin
from utils.user import get_user_by_email

load_dotenv()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
JWT_ALGORITHM = "RS256"
JWT_TOKEN_EXPIRE_MINUTES = 30

PRIVATE_KEY = base64.b64decode(os.getenv("PRIVATE_KEY")).decode("utf-8")
PUBLIC_KEY = base64.b64decode(os.getenv("PUBLIC_KEY")).decode("utf-8")

oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

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

async def get_token_from_ws(websocket: WebSocket):
    token = websocket.headers.get("Authorization")

    if token:
        return token.split(" ")[1] if " " in token else token
    return None

def authenticate_user(db: Session, user: UserLogin):
    user_db = get_user_by_email(db, user.username)

    if not user_db:
        return False
    
    if not bcrypt_context.verify(user.password, user_db.password):
        return False
    
    return user_db