from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

# # Schema validation using Pydantic for data received from client
# class Post(BaseModel):
#     title: str
#     content: str
#     # optional as default value is set
#     published: bool = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


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
    user_id: int
    post_owner: UserOut

    # Add this class for Pydantic to read despite the response not being a python dictionary
    # The response in this case that is to be validated is a SQLAlchemy based class
    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id: int
    drc: int
