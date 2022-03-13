from fastapi import Body, FastAPI


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {'data': 'some placeholder post'}


@app.post("/createposts")
def create_posts(payload = Body(...)):
    print(payload)
    return {"new post": f"title: {payload['title']} content: {payload['content']}"}
