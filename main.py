from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# Schema validation using Pydantic for data received from front end
class Post(BaseModel):
    title: str
    content: str
    # optional as default value is set
    published: bool = True
    rating: Optional[int] = None

# Save posts (ultimately connect to a database, using a list for demonstation for now)
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "some random title", "content": "post 2's content", "id": 2} 
           ]

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {'data': my_posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {'data': post_dict}

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

    return None

#id represents a path parameter
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
    return post
