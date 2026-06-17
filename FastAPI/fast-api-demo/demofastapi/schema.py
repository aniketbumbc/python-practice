from pydantic import BaseModel
from typing import Optional


class LabBookStore(BaseModel):
    title:str
    author:str
    publish_date:str


class UpdateLabBookStore(BaseModel):
    title:str
    author:str
    publish_date:str

class PatchLabBookStore(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publish_date: Optional[str] = None
