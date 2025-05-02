from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

# request GET method url: "/"
# order matters for same route path

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/")
async def get_posts():
    return {"data": "This is your post"}

@app.get("/test")
async def test_posts():
    return {"data": "This is test post"}

@app.post("/create")
def create_posts(payload: dict = Body()):
    print(payload)
    return {"new_post": f"title: {payload['title']} content: {payload['content']}"}

# title str, cotent str