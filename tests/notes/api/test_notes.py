import pytest

from httpx import ASGITransport, AsyncClient, codes

from src.notes.main import app


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
