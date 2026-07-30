from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app =  FastAPI()

class Bookmark(BaseModel):
    def __init__(self):
        self.bookmarks[]

    title : str
    url : str 
    category : Optional[str] = "general"
    is_favorite : Optional[bool] = False

bookmarks = [
                {title:"WOZ",url:"idk",category:"fantasy",is_favourite:True}
            ]

@app.get("/")
def welcome():
    return("wlecome to bookmarks")

@app.get("/bookmarks")
def get_bookmarks():
    return{"data":bookmarks}

