# tests/notes/conftest.py
from asyncio import sleep

import pytest

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from testcontainers.postgres import PostgresContainer

from src.notes.logger import log
from src.notes.persistence.entities import Base
from src.notes.persistence.repository import NotesRepository


@pytest.fixture(scope='session')
def postgres_container():
    with PostgresContainer('postgres:latest') as postgres:
        postgres._configure()
        yield postgres


@pytest.fixture(scope='session')
def db_engine(postgres_container):
    db_url = f'postgresql+asyncpg://{postgres_container.username}:{postgres_container.password}@{postgres_container.get_container_host_ip()}:{postgres_container.get_exposed_port(postgres_container.port)}/{postgres_container.dbname}'
    log.info(f'Using test database URL: {db_url}')
    engine = create_async_engine(db_url, poolclass=NullPool)
    return engine


@pytest.fixture(scope='session')
async def setup_db(db_engine):
    await sleep(3)
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session(db_engine, setup_db) -> AsyncSession:
    async_session = async_sessionmaker(db_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.fixture
async def repository(session):
    return NotesRepository(session)
