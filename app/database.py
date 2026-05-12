import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv
 
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create the Engine (The core of the connection) 
engine = create_async_engine(DATABASE_URL, echo=True)

# Create SessionLocal (How we will talk to the DB in each request) 
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Provide Base for Models 
class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        logging.info("Database connection established") 
        try:
            yield session
        finally:
            logging.info("Database connection closed") 




            