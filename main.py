from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {'data': 'some placeholder post'}

# Schema that front end should ensure being sent
class Post(BaseModel):
    title: str
    content: str
    # optional as default value is set
    published: bool = True
    rating: Optional[int] = None


@app.post("/createposts")
def create_posts(post: Post):
    to_return  = post.dict()
    print(post, type(post))
    print(to_return ,type(to_return))

    return to_return
    # print(payload)
    # return {"new post": f"title: {payload['title']} content: {payload['content']}"}
