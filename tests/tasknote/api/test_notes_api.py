# tests/tasknote/api/test_notes_api.py

import pytest

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, codes

from src.tasknote.api.router import router
from src.tasknote.persistence.db import get_db_session

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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_note_without_content_e2e(session):
    # Override the app's DB session to use test session
    async def override_get_db_session():
        yield session

    app.dependency_overrides[get_db_session] = override_get_db_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.post('/notes', json={'title': 'Note Without Content'})

    assert response.status_code == codes.OK
    body = response.json()
    assert body['title'] == 'Note Without Content'
    assert body['content'] is None
    assert body['id'] is not None
    assert 'created_at' in body

    # Clean up to avoid override leakage
    app.dependency_overrides.clear()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_note_e2e_success(session):
    # Override the app's DB session to use test session
    async def override_get_db_session():
        yield session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # First create a note
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        create_response = await ac.post(
            '/notes', json={'title': 'Get Note Test', 'content': 'This is a test for get note.'}
        )

    assert create_response.status_code == codes.OK
    created_note = create_response.json()
    note_id = created_note['id']

    # Then retrieve the note
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        get_response = await ac.get(f'/notes/{note_id}')

    assert get_response.status_code == codes.OK
    retrieved_note = get_response.json()
    assert retrieved_note['id'] == note_id
    assert retrieved_note['title'] == 'Get Note Test'
    assert retrieved_note['content'] == 'This is a test for get note.'
    assert 'created_at' in retrieved_note

    # Clean up to avoid override leakage
    app.dependency_overrides.clear()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_note_e2e_not_found(session):
    # Override the app's DB session to use test session
    async def override_get_db_session():
        yield session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # Try to retrieve a non-existent note
    non_existent_id = 9999  # Assuming this ID doesn't exist
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.get(f'/notes/{non_existent_id}')

    assert response.status_code == codes.NOT_FOUND
    error = response.json()
    assert 'Note not found' in error['detail']
    assert str(non_existent_id) in error['detail']

    # Clean up to avoid override leakage
    app.dependency_overrides.clear()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_notes_e2e(session):
    # Override the app's DB session to use test session
    async def override_get_db_session():
        yield session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # First create a few notes
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        await ac.post('/notes', json={'title': 'List Test Note 1', 'content': 'This is test note 1 for list endpoint.'})
        await ac.post('/notes', json={'title': 'List Test Note 2', 'content': 'This is test note 2 for list endpoint.'})

    # Then retrieve all notes
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.get('/notes')

    assert response.status_code == codes.OK
    notes = response.json()
    assert isinstance(notes, list)

    # Check if our test notes are in the list
    titles = [note['title'] for note in notes]
    contents = [note['content'] for note in notes]

    assert 'List Test Note 1' in titles
    assert 'List Test Note 2' in titles
    assert 'This is test note 1 for list endpoint.' in contents
    assert 'This is test note 2 for list endpoint.' in contents

    # Verify each note has the expected structure
    for note in notes:
        assert 'id' in note
        assert 'title' in note
        assert 'content' in note
        assert 'created_at' in note

    # Clean up to avoid override leakage
    app.dependency_overrides.clear()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_note_e2e_success(session):
    # Override the app's DB session to use test session
    async def override_get_db_session():
        yield session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # First create a note
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        create_response = await ac.post(
            '/notes', json={'title': 'Delete Note Test', 'content': 'This is a test for delete note.'}
        )

    assert create_response.status_code == codes.OK
    created_note = create_response.json()
    note_id = created_note['id']

    # Then delete the note
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        delete_response = await ac.delete(f'/notes/{note_id}')

    assert delete_response.status_code == codes.NO_CONTENT
    assert delete_response.content == b''  # No content in response body

    # Verify the note is deleted by trying to get it
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        get_response = await ac.get(f'/notes/{note_id}')

    assert get_response.status_code == codes.NOT_FOUND
    error = get_response.json()
    assert 'Note not found' in error['detail']
    assert str(note_id) in error['detail']

    # Clean up to avoid override leakage
    app.dependency_overrides.clear()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_note_e2e_not_found(session):
    # Override the app's DB session to use test session
    async def override_get_db_session():
        yield session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # Try to delete a non-existent note
    non_existent_id = 9999  # Assuming this ID doesn't exist
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.delete(f'/notes/{non_existent_id}')

    assert response.status_code == codes.NOT_FOUND
    error = response.json()
    assert 'Note not found' in error['detail']
    assert str(non_existent_id) in error['detail']

    # Clean up to avoid override leakage
    app.dependency_overrides.clear()
