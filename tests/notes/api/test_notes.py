from unittest.mock import AsyncMock

import pytest

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, codes

from src.notes.api.dependencies import get_note_service
from src.notes.api.router import router
from src.notes.api.schemas import NoteCreate

app = FastAPI()
app.include_router(router)


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=(ASGITransport(app=app)), base_url='http://test') as ac:
        response = await ac.get('/')
    assert response.status_code == codes.OK
    assert response.json() == {'message': 'Welcome to the Notes API'}


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=(ASGITransport(app=app)), base_url='http://test') as ac:
        response = await ac.get('/health')
    assert response.status_code == codes.OK
    assert response.json() == {'status': 'OK'}


@pytest.mark.asyncio
async def test_create_note():
    mock_note = {
        'id': 1,
        'title': 'Test Note',
        'content': 'This is a test note from api.',
        'created_at': '2023-10-01T00:00:00',
    }

    mock_service = AsyncMock()
    mock_service.create_note.return_value = mock_note

    app.dependency_overrides[get_note_service] = lambda: mock_service

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.post('/notes', json={'title': 'Test Note', 'content': 'This is a test note from api.'})

    assert response.status_code == codes.OK
    data = response.json()
    assert data['title'] == 'Test Note'
    assert data['content'] == 'This is a test note from api.'
    mock_service.create_note.assert_called_once_with(
        NoteCreate(title='Test Note', content='This is a test note from api.')
    )

    app.dependency_overrides.clear()
