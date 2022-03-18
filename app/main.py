from fastapi import FastAPI
import os
from . import models
from .database import engine
from .routers import posts, users, auth

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

models.Base.metadata.create_all(bind = engine)


@app.get("/")
def root():
    return {"message": "Landing end point for a dummy social media app"}