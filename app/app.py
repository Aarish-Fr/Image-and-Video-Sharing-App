from fastapi import FastAPI
from fastapi import HTTPException
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

#initializing the fastApi app
app = FastAPI(lifespan=lifespan)

text_posts = {
    1: {
        "title": "Understanding Python's __name__ Variable",
        "content": "Today I learned how to prevent my FastAPI server from auto-starting when imported!",
        "author": "BackendBeginner99",
        "published": True,
        "likes": 42
    },
    2: {
        "title": "My first SQLAlchemy model",
        "content": "Still working on the draft for this one, database tables are tricky...",
        "author": "BackendBeginner99",
        "published": False,
        "likes": 0
    },
    3: {
        "title": "Uploading Images in FastAPI",
        "content": "Just figured out how to use UploadFile to handle image uploads. It is surprisingly clean.",
        "author": "MediaAppDev",
        "published": True,
        "likes": 156
    },
    4: {
        "title": "Stuck on Path Parameters",
        "content": "Trying to build a route to get a specific post by ID. Keep getting a 404 error.",
        "author": "CodeNewbie",
        "published": True,
        "likes": 3
    },
    5: {
        "title": "Handling Video Files",
        "content": "Videos are massive. I need to figure out how to stream them in chunks instead of loading the whole file into server memory.",
        "author": "MediaAppDev",
        "published": False,
        "likes": 0
    },
    6: {
        "title": "PostgreSQL vs SQLite for development",
        "content": "Is it okay to use SQLite while building my app locally before switching to Postgres?",
        "author": "BackendBeginner99",
        "published": True,
        "likes": 12
    },
    7: {
        "title": "Pydantic models are a lifesaver",
        "content": "Data validation used to be a nightmare in other languages. Pydantic makes making sure a user submits a valid email address so easy.",
        "author": "PythonLover",
        "published": True,
        "likes": 56
    },
    8: {
        "title": "Why is Uvicorn so fast?",
        "content": "Reading about ASGI servers today. Uvicorn handles asynchronous requests beautifully.",
        "author": "FastAPI_Fanatic",
        "published": True,
        "likes": 88
    },
    9: {
        "title": "Handling CORS errors",
        "content": "My frontend couldn't talk to my FastAPI backend until I added the CORSMiddleware. Security features are strict!",
        "author": "FullStackWannabe",
        "published": True,
        "likes": 120
    },
    10: {
        "title": "Deploying my first app",
        "content": "Getting ready to push this code to a real server. Does anyone have tips for absolute beginners?",
        "author": "CodeNewbie",
        "published": True,
        "likes": 25
    }
}

#Endpoint GET: Returns all the post
@app.get("/posts")
def get_all_posts(limit : int = None):      # query parameter

# if the parameter is passed only in the function, than it automatically become a query PARAMETER
    if limit:
        return list(text_posts.values())[: limit]
    
    return text_posts

#Endpoint GET: return post based on the ID entered
@app.get("/posts/{id}")     # the id here is path parameter, a dynamic value
def get_post(id : int) -> PostResponse:

    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return text_posts.get(id)   

#Endpoint POST : creating a new text post
@app.post("/posts") 
def create_post(post : PostCreate) -> PostResponse:
    new_post = {
        "title" : post.title,
        "content" : post.content,
        "author" : post.author,
        "published" : post.published,
        "likes" : post.likes
    }

    text_posts[max(text_posts.keys()) + 1] = new_post

    return new_post
