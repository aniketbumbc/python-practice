from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your-256-bit-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # to hash and verify passwords create tokens for authentication
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token") # to get the token from the request


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: str = Field(min_length=3, max_length=20)
    first_name: str = Field(min_length=3, max_length=20)
    last_name: str = Field(min_length=3, max_length=20)
    role: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=20)
    age: int = Field(gt=0, lt=100)



class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int
    username: str




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):

    payload = {
        "sub": username,
        "id": user_id,
        "role": role
       }
       
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({"exp": expires})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        return {"username": username, "id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user( create_user_request: CreateUserRequest,db: Session = Depends(get_db)):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        age = create_user_request.age,
        role = create_user_request.role,
        hashed_password = pwd_context.hash(create_user_request.password),
        is_active = True,
    )
    db.add(create_user_model)
    db.commit()
    return {"message": "User created successfully"}


@router.post("/token", response_model=Token)
async def login_for_access(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
       raise HTTPException(status_code=401, detail="Could not validate credentials")

    access_token = create_access_token(user.username, user.id, user.role, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {'access_token': access_token, 'token_type': 'bearer'}
  