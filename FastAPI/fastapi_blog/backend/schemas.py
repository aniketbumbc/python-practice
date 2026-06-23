from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):
    title:str = Field(min_length=1, max_length=100)
    content:str = Field(min_length=30,example="FastAPI is a modern web framework for building APIs with Python."
)
    author:str = Field(min_length=1, max_length=50)
    topic:str =  Field(min_length=5, max_length=50)


class PostCreate(PostBase):
    pass



class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True) #Pydantic to read data from ORM model attributes (like SQLAlchemy objects) instead of only from dicts.

    id: int
    date_posted: str