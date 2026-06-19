from pydantic import BaseModel,EmailStr
from typing import Optional

# create user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


# schema user login
class UserLogin(BaseModel):
    username: str
    password: str
