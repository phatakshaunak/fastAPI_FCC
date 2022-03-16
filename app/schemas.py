import email
from pydantic import BaseModel, EmailStr
from datetime import datetime

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

class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str
