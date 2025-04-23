# src/notes/persistence/db.py
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.notes.settings import settings

engine = create_async_engine(settings.db_url_async, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
