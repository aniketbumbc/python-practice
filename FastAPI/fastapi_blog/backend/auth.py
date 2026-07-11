from datetime import UTC, datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from config import settings
from typing import Annotated
from fastapi import Depends,HTTPException,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import models
from config import settings
from database import get_db
import hashlib
import secrets

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_pass:str, hash_pass:str) -> bool:
    return pwd_context.verify(plain_pass,hash_pass)


def create_access_token(data:dict, expires_delta:timedelta | None)-> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_mins)

    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm
    )
    return encode_jwt


def verify_access_token(token:str) -> str | None: 

    try:
        payload = jwt.decode(token, settings.secret_key.get_secret_value(),algorithms=[settings.algorithm],options={"require":["exp","sub"]})
    except jwt.InvalidTokenError:
        return None
    else:
        return payload


async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)], db:Annotated[AsyncSession,Depends(get_db)]) -> models.User:
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    userName = payload.get('sub')
    userId = payload.get('id')
    if not userName or not userId:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await db.get(models.User, int(userId))  # faster, uses primary key lookup
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

CurrentUser = Annotated[models.User, Depends(get_current_user)]

def generate_rest_token() ->str:
    return secrets.token_urlsafe(32)

def hash_reset_token(token:str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()