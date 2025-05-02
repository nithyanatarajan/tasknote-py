# tests/tasknote/conftest.py
from asyncio import sleep
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import pytest

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from testcontainers.postgres import PostgresContainer

from src.tasknote.api.dependencies import get_note_service, get_tasks_service
from src.tasknote.api.router import router
from src.tasknote.logger import log
from src.tasknote.persistence.db import get_db_session
from src.tasknote.persistence.entities import Base
from src.tasknote.persistence.note_repository import NotesRepository
from src.tasknote.persistence.tasks_repository import TasksRepository


@pytest.fixture(scope='session')
def postgres_container():
    """
    Create a PostgreSQL container for testing.
    """
    with PostgresContainer('postgres:latest') as postgres:
        postgres._configure()
        yield postgres


@pytest.fixture(scope='session')
def db_engine(postgres_container):
    """
    Create a SQLAlchemy engine for the test database.
    """
    db_url = f'postgresql+asyncpg://{postgres_container.username}:{postgres_container.password}@{postgres_container.get_container_host_ip()}:{postgres_container.get_exposed_port(postgres_container.port)}/{postgres_container.dbname}'
    log.info(f'Using test database URL: {db_url}')
    engine = create_async_engine(db_url, poolclass=NullPool)
    return engine


@pytest.fixture(scope='session')
async def setup_db(db_engine):
    """
    Set up the database for testing.
    """
    await sleep(3)
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session(db_engine, setup_db) -> AsyncSession:
    """
    Create a new SQLAlchemy session for each test.
    """
    async_session = async_sessionmaker(db_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.fixture
async def notes_repository(session):
    """
    Create a NotesRepository instance for testing.
    """
    return NotesRepository(session)


@pytest.fixture
async def tasks_repository(session):
    """
    Create a TasksRepository instance for testing.
    """
    return TasksRepository(session)


@pytest.fixture
def app() -> FastAPI:
    """
    Create a FastAPI app for testing.
    """
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient]:
    """
    Create an AsyncClient for testing the FastAPI app.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


@asynccontextmanager
async def override_db_session(app: FastAPI, session: AsyncSession):
    """
    Context manager to override the DB session for tests.
    """

    async def override_get_db_session():
        yield session

    app.dependency_overrides[get_db_session] = override_get_db_session
    try:
        yield
    finally:
        app.dependency_overrides.clear()


@asynccontextmanager
async def override_note_service(app: FastAPI, mock_service):
    """
    Context manager to override the note service for tests.
    """
    app.dependency_overrides[get_note_service] = lambda: mock_service
    try:
        yield
    finally:
        app.dependency_overrides.clear()


@asynccontextmanager
async def override_tasks_service(app: FastAPI, mock_service):
    """
    Context manager to override the tasks service for tests.
    """
    app.dependency_overrides[get_tasks_service] = lambda: mock_service
    try:
        yield
    finally:
        app.dependency_overrides.clear()
