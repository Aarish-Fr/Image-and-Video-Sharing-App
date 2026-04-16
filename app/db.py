from collections.abc import AsyncGenerator
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass          

#creating a table for Posts
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

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