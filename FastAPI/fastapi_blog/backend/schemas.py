from pydantic import BaseModel, ConfigDict,EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username:str = Field(min_length=1, max_length=50)
    email:EmailStr = Field(max_length=50)


class UserCreate(UserBase):
    password: str = Field(min_length=5)

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True) #Pydantic to read data from ORM model attributes (like SQLAlchemy objects) instead of only from dicts.

    id: int
    username: str
    image_file: str | None
    image_path: str

class UserPrivate(UserPublic):
    email:EmailStr



class PostBase(BaseModel):
    title:str = Field(min_length=1, max_length=100)
    content:str = Field(min_length=30,example="FastAPI is a modern web framework for building APIs with Python."
)
    topic:str =  Field(min_length=5, max_length=50)


class PostCreate(PostBase):
    pass



class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True) #Pydantic to read data from ORM model attributes (like SQLAlchemy objects) instead of only from dicts.

    id: int
    user_id: int
    date_posted: datetime
    author: UserPublic


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    content: Optional[str] = Field(None, min_length=10)
    topic: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None

class Token(BaseModel):
    access_token: str
    token_type: str


class PaginatedPostResponse(BaseModel):
    posts: list[PostResponse]
    total:int
    skip:int
    limit:int
    has_more:bool


class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(max_length=120)


class ResetPasswordRequest(BaseModel):
    token: str
    new_password:str = Field(min_length=5)


class ChangePasswordRequest(BaseModel):
    current_password:str
    new_password: str = Field(min_length=5)