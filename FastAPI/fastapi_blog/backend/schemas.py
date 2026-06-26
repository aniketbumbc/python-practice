from pydantic import BaseModel, ConfigDict,EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username:str = Field(min_length=1, max_length=50)
    email:EmailStr = Field(max_length=50)


class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True) #Pydantic to read data from ORM model attributes (like SQLAlchemy objects) instead of only from dicts.

    id:int
    image_file: str | None
    image_path: str



class PostBase(BaseModel):
    title:str = Field(min_length=1, max_length=100)
    content:str = Field(min_length=30,example="FastAPI is a modern web framework for building APIs with Python."
)
    topic:str =  Field(min_length=5, max_length=50)


class PostCreate(PostBase):
    user_id: int #temporary



class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True) #Pydantic to read data from ORM model attributes (like SQLAlchemy objects) instead of only from dicts.

    id: int
    user_id: int
    date_posted: datetime
    author: UserResponse


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    content: Optional[str] = Field(None, min_length=10)
    topic: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    image_file: Optional[str] = None