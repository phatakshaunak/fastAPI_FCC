from re import I
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2, os
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, Base, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# models.Base.metadata.create_all(bind = engine)

# Schema validation using Pydantic for data received from client
class Post(BaseModel):
    title: str
    content: str
    # optional as default value is set
    published: bool = True

pg_password = os.environ["pg_password"]

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', 
                                password = pg_password, cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as error:
        print("Connecting to database failed with the message \n", error)
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "Landing page of your dummy social media app"}

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Posts).all()
    return {"data": posts}


# Get all posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute('''select * from public.posts''')
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Posts).all()
    return {'data': posts}


# Create a post, return 201 for post created
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):

    # %s avoids SQL injection, prevents filter variables being treated as valid sql commands
    cursor.execute('''INSERT INTO public.posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', 
                  (post.title, post.content, post.published))
    
    # Saves changes to the db
    conn.commit()
    return {'data': cursor.fetchone()}


#Get post by path parameter {id}
@app.get("/posts/{id}")
def get_post(id: int):

    cursor.execute('''SELECT * from public.posts p where p.id = %s''', (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")
    
    return {"post_detail": post}
    

# Delete posts
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute('''DELETE FROM public.posts p where p.id = %s RETURNING *''',str(id))

    deleted = cursor.fetchone()

    conn.commit()
    
    if deleted:
        return {"deleted post": deleted}
    
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")

# Update posts
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', 
                   (post.title, post.content, post.published, str(id)))
    
    updated = cursor.fetchone()

    conn.commit()

    if updated:
        return {"updated message": updated}

    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")