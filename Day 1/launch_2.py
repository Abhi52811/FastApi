from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.post("/create")
async def create_posts(new_post: Post):
    print(new_post)
    print(new_post.title)
    print(new_post.content)
    # Pydantic model has a method called dot dict
    print(new_post.dict())
    return {"data": new_post}

# title str, cotent str