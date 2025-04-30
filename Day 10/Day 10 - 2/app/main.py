from fastapi import FastAPI

import psycopg
from psycopg.rows import dict_row
import time
from .databases import engine
from . import models

from .routers import post,user,auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg.connect(host='localhost',dbname='fastapiDB',user='postgres',password='root',row_factory=dict_row)
        print(conn)
        cursor= conn.cursor()
        print(cursor)
        print("DB connection was sucessfull")
        break
    except Exception as error:
        print("Connection to DB failed")
        print("Error:",error)
        time.sleep(5) 


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello world"}
