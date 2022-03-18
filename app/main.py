from fastapi import FastAPI
import psycopg2, os
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import posts, users, auth

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

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
    return {"message": "Landing page of a dummy social media app"}






    