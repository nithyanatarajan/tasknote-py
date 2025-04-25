from unittest.mock import AsyncMock

import pytest

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, codes

from src.notes.api.dependencies import get_note_service
from src.notes.api.router import router
from src.notes.api.schemas import NoteCreate
from src.notes.domain.exceptions import NoteNotFoundError

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
    assert data == mock_note
    mock_service.create_note.assert_called_once_with(
        NoteCreate(title='Test Note', content='This is a test note from api.')
    )

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_note():
    mock_note = {
        'id': 1,
        'title': 'Test Note',
        'content': 'This is a test note from api.',
        'created_at': '2023-10-01T00:00:00',
    }

    mock_service = AsyncMock()
    mock_service.get_note.return_value = mock_note

    app.dependency_overrides[get_note_service] = lambda: mock_service

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.get('/notes/1')

    assert response.status_code == codes.OK
    data = response.json()
    assert data == mock_note
    mock_service.get_note.assert_called_once_with(1)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_note_not_found():
    note_id = 999
    mock_service = AsyncMock()
    mock_service.get_note.side_effect = NoteNotFoundError(note_id)

    app.dependency_overrides[get_note_service] = lambda: mock_service

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.get(f'/notes/{note_id}')

    assert response.status_code == codes.NOT_FOUND
    data = response.json()
    assert data == {'detail': f'Note not found: {note_id}'}
    mock_service.get_note.assert_called_once_with(note_id)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_notes():
    mock_notes = [
        {
            'id': 1,
            'title': 'Test Note 1',
            'content': 'This is test note 1.',
            'created_at': '2023-10-01T00:00:00',
        },
        {
            'id': 2,
            'title': 'Test Note 2',
            'content': 'This is test note 2.',
            'created_at': '2023-10-02T00:00:00',
        },
    ]

    mock_service = AsyncMock()
    mock_service.get_all_notes.return_value = mock_notes

    app.dependency_overrides[get_note_service] = lambda: mock_service

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.get('/notes')

    assert response.status_code == codes.OK
    data = response.json()
    assert data == mock_notes
    mock_service.get_all_notes.assert_called_once()

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_delete_note():
    note_id = 1
    mock_service = AsyncMock()

    app.dependency_overrides[get_note_service] = lambda: mock_service

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.delete(f'/notes/{note_id}')

    assert response.status_code == codes.NO_CONTENT
    assert response.content == b''  # No content in response body
    mock_service.delete_note.assert_called_once_with(note_id)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_delete_note_not_found():
    note_id = 999
    mock_service = AsyncMock()
    mock_service.delete_note.side_effect = NoteNotFoundError(note_id)

    app.dependency_overrides[get_note_service] = lambda: mock_service

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.delete(f'/notes/{note_id}')

    assert response.status_code == codes.NOT_FOUND
    data = response.json()
    assert data == {'detail': f'Note not found: {note_id}'}
    mock_service.delete_note.assert_called_once_with(note_id)

    app.dependency_overrides.clear()
