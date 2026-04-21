from collections.abc import AsyncGenerator
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
from fastapi import Depends

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass          

# creating a user table
class User(SQLAlchemyBaseUserTableUUID, Base):
    posts = relationship("Post", back_populates="user")

#creating a table for Posts
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="posts")

# Enigne is the control center which manages the connection pool and directly interact with the database
engine = create_async_engine(DATABASE_URL)

# session is yhe workspace for the database operations
# expire_on_commint restrict the database to fetch the latest data by quering the DB
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

#asyncronous func allowing the part of the program to keep run while the slow operation of DB are being performed
async def create_db_and_tables():
    async with engine.begin() as conn:      # here async handles opening and closing of the connection along with commit and rollback
        await conn.run_sync(Base.metadata.create_all)    # create_all is a syncronous func. .run_async enables to run a sync function inside async function

#asyncronous session maker
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session   # instead of returning, it hands over the session and pauses the function right here

# the get_user_db function basically give access to the User table of the database instead of the whole database(session). since when a person will be accessing the table he will be wanting to either extract, update or delete the data from the table for which it is required SQL. but since our fastapi_user is based on python so it couldnt execute those commands. it have functions like delete, update something similar which is in more readble(english) form. the SQLAlchemyuserDatabase contains SQL commnads for those specific fastapi_user functions and enable the communication with the database table User
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

