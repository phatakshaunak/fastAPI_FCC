from pydantic import BaseModel

from app.database import Base

# # Schema validation using Pydantic for data received from client
# class Post(BaseModel):
#     title: str
#     content: str
#     # optional as default value is set
#     published: bool = True

class PostBase(BaseModel):
    title: str
    content: str
    # optional as default value is set
    published: bool = True

class PostCreate(PostBase):
    pass
