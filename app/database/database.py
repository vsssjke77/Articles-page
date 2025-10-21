from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import os
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase
from config import settings

class Base(DeclarativeBase):
    pass

load_dotenv()

DB_URL = settings.database_url
async_engine = create_async_engine(DB_URL, echo=True)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)



