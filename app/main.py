from re import I
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
import psycopg2, os
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind = engine)



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


# Get all posts
@app.get("/posts", response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute('''select * from public.posts''')
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Posts).all()
    
    return posts


# Create a post, return 201 for post created
@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

    # %s avoids SQL injection, prevents filter variables being treated as valid sql commands
    # cursor.execute('''INSERT INTO public.posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', 
                #   (post.title, post.content, post.published))
    
    # Saves changes to the db
    # conn.commit()
    # new_post = models.Posts(title = post.title, content = post.content, published = post.published)
    
    new_post = models.Posts(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#Get post by path parameter {id}
@app.get("/posts/{id}", response_model = schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute('''SELECT * from public.posts p where p.id = %s''', (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")
    
    return post
    

# Delete posts
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute('''DELETE FROM public.posts p where p.id = %s RETURNING *''',str(id))

    # deleted = cursor.fetchone()

    # conn.commit()
    delete_query = db.query(models.Posts).filter(models.Posts.id == id)

    if delete_query.first():
        delete_query.delete(synchronize_session = False)
        db.commit()
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")

# Update posts
@app.put("/posts/{id}", response_model = schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', 
    #                (post.title, post.content, post.published, str(id)))
    
    # updated = cursor.fetchone()

    # conn.commit()

    update_query = db.query(models.Posts).filter(models.Posts.id == id)

    if update_query.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")
    
    update_query.update(post.dict(), synchronize_session = False)

    db.commit()

    return update_query.first()


@app.post("/users", status_code = status.HTTP_201_CREATED)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


    