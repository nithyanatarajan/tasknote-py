from unittest.mock import AsyncMock, patch

import pytest

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, codes

from src.notes.api.router import router
from src.notes.api.schemas import NoteCreate

app = FastAPI()
app.include_router(router)


@pytest.mark.asyncio
async def test_create_note():
    mock_note = {
        'id': 1,
        'title': 'Test Note',
        'content': 'This is a test note from api.',
        'created_at': '2023-10-01T00:00:00',
    }

    with patch('src.notes.api.router.get_db_session', return_value=AsyncMock()):
        with patch('src.notes.api.router.NoteService') as MockNoteService:
            mock_service_instance = MockNoteService.return_value
            mock_service_instance.create_note = AsyncMock(return_value=mock_note)

            async with AsyncClient(transport=(ASGITransport(app=app)), base_url='http://test') as ac:
                response = await ac.post(
                    '/notes', json={'title': 'Test Note', 'content': 'This is a test note from api.'}
                )

            assert response.status_code == codes.OK
            assert response.json()['title'] == 'Test Note'
            assert response.json()['content'] == 'This is a test note from api.'

            # Ensure the service's create_note method was called once
            mock_service_instance.create_note.assert_called_once_with(
                NoteCreate(title='Test Note', content='This is a test note from api.')
            )
