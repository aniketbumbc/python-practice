from sqlalchemy import Column, Integer,String
from .auth_db import Base

class User(Base):
    __tablename__ = "bookusers"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True,index=True)
    email = Column(String(255), unique=True,index=True)
    hashed_password = Column(String(255), unique=True,index=True)
    role = Column(String(50), default="user")