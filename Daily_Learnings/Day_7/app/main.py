from fastapi import FastAPI

import psycopg
from psycopg.rows import dict_row
import time
from .databases import engine
from . import models

from .routers import post,user


# Looks at all the classes that inherit from Base (like Post, User)
# Reads their __tablename__ and Column(...) definitions
# Creates the corresponding tables in the database, if they do not already exist.
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

@app.get("/")
def root():
    return {"message": "Hello world"}
