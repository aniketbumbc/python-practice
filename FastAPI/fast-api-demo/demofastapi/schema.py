from pydantic import BaseModel

class LabBookStore(BaseModel):
    title:str
    author:str
    publish_date:str