from pydantic import BaseModel

class PostCreate(BaseModel):
    title : str
    content : str
    author : str
    published : bool
    likes : int

class PostResponse(BaseModel):
    title : str
    content : str
    author : str
    published : bool
    likes : int