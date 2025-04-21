import pytest

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, codes

from src.notes.api.router import router

app = FastAPI()
app.include_router(router)


@pytest.mark.asyncio
async def test_create_note():
    async with AsyncClient(transport=(ASGITransport(app=app)), base_url='http://test') as ac:
        response = await ac.post('/notes', json={'title': 'Test Note', 'content': 'This is a test note.'})
    assert response.status_code == codes.OK
    assert response.json()['title'] == 'Test Note'
    assert response.json()['content'] == 'This is a test note.'
