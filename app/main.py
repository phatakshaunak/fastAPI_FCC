from re import I
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# Schema validation using Pydantic for data received from client
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
    return {"message": "Landing page of your dummy social media app"}


# Get all posts
@app.get("/posts")
def get_posts():
    return {'data': my_posts}


# Create a post, return 201 for post created
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    print(post, type(post))
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {'data': post_dict}


# Helper for getting post by id
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

    return None

#Get post by path parameter {id}
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
    return post

def find_postIndex(idx):

    for i,d in enumerate(my_posts):

        if d["id"] == idx:
            return i
    
    return None

# Delete posts
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    i = find_postIndex(id)

    if i != None:
        my_posts.pop(i)
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")

# Update posts
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    i = find_postIndex(id)

    if i != None:
        post_dict = post.dict()
        post_dict["id"] = id
        my_posts[i] = post_dict
        return {"data": post_dict}
    
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")