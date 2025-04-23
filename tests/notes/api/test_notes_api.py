# tests/notes/api/test_notes_api.py

import pytest

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, codes

from src.notes.api.router import router
from src.notes.persistence.db import get_db_session

app = FastAPI()
app.include_router(router)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_note_e2e(session):
    # Override the app's DB session to use test session
    async def override_get_db_session():
        yield session

    app.dependency_overrides[get_db_session] = override_get_db_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.post('/notes', json={'title': 'E2E Note', 'content': 'This is a test from the full stack.'})

    assert response.status_code == codes.OK
    body = response.json()
    assert body['title'] == 'E2E Note'
    assert body['content'] == 'This is a test from the full stack.'
    assert body['id'] is not None
    assert 'created_at' in body

    # Clean up to avoid override leakage
    app.dependency_overrides.clear()
