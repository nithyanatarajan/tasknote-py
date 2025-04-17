import pytest

from httpx import ASGITransport, AsyncClient, codes

from src.main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=(ASGITransport(app=app)), base_url='http://test') as ac:
        response = await ac.get('/')
    assert response.status_code == codes.OK
    assert response.json() == {'message': 'Hello World'}


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=(ASGITransport(app=app)), base_url='http://test') as ac:
        response = await ac.get('/health')
    assert response.status_code == codes.OK
    assert response.json() == {'status': 'OK'}


@pytest.mark.asyncio
async def test_say_hello():
    async with AsyncClient(transport=(ASGITransport(app=app)), base_url='http://test') as ac:
        response = await ac.get('/hello/User')
    assert response.status_code == codes.OK
    assert response.json() == {'message': 'Hello User'}
