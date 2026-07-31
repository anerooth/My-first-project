from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
app = FastAPI()

class post(BaseModel):
    name: str = "Anerooth"
    role: str
    age: Optional[int] = None
while True:
    try:
        conn = psycopg.connect(dbname='My first database',user='postgres',password="LOVE")
        cursor = conn.cursor()
        print("database connetion sucessfull")
        break
    except Exception as error:
        print("connection to database failed!")
        print(f"Error: {error}")
        time.sleep(2)

my_posts = [{"name":"content of post 1","id":0},{"name":"content of post 2","id":1}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index(id):
    for i,p in enumerate(my_posts):
        if (id == p['id']):
            return i

@app.get("/")
def read_root():
    return {"Hello":"world"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return{"data":posts}

# @app.get("/posts")
# def get_posts():
#     return {"here are your posts"}

@app.get("/songs")
def fav_song():
    return{"My fav song is ranjha"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(load:post):
    my_posts.append(load.model_dump)
    temp = load.dict()
    temp['id'] = randrange(0,1000)
    my_posts.append(temp)
    return{"message":temp}

@app.get("/posts/{id}")
def get_post(id: int,response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your post with {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{f"your post with id {id} was not fucking found"}
    return{"data":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your post with id:{id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id :int,Post : post):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your post with id:{id} was not found")
    post_dict = Post.dict()
    post_dict['id'] = index
    my_posts[index] = post_dict
    return{"data":post_dict}



