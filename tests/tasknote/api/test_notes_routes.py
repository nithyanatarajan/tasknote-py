from datetime import timedelta
from unittest.mock import AsyncMock

import pytest

from fastapi import FastAPI
from httpx import AsyncClient, codes

from src.common.timeutils import now_ist
from src.tasknote.api.schemas import NoteCreate, TaskCreate
from src.tasknote.domain.exceptions import NoteNotFoundError
from src.tasknote.domain.models import TaskStatus
from tests.tasknote.conftest import override_note_service, override_tasks_service


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get('/')
    assert response.status_code == codes.OK
    assert response.json() == {'message': 'Welcome to the TaskNote'}


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    response = await client.get('/health')
    assert response.status_code == codes.OK
    assert response.json() == {'status': 'OK'}


@pytest.mark.asyncio
async def test_create_note(app: FastAPI, client: AsyncClient):
    mock_note = {
        'id': 1,
        'title': 'Test Note',
        'content': 'This is a test note from api.',
        'created_at': '2023-10-01T00:00:00',
    }

    mock_service = AsyncMock()
    mock_service.create_note.return_value = mock_note

    async with override_note_service(app, mock_service):
        response = await client.post('/notes', json={'title': 'Test Note', 'content': 'This is a test note from api.'})

        assert response.status_code == codes.OK
        data = response.json()
        assert data == mock_note
        mock_service.create_note.assert_called_once_with(
            NoteCreate(title='Test Note', content='This is a test note from api.')
        )


@pytest.mark.asyncio
async def test_get_note(app: FastAPI, client: AsyncClient):
    mock_note = {
        'id': 1,
        'title': 'Test Note',
        'content': 'This is a test note from api.',
        'created_at': '2023-10-01T00:00:00',
    }

    mock_service = AsyncMock()
    mock_service.get_note.return_value = mock_note

    async with override_note_service(app, mock_service):
        response = await client.get('/notes/1')

        assert response.status_code == codes.OK
        data = response.json()
        assert data == mock_note
        mock_service.get_note.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_note_not_found(app: FastAPI, client: AsyncClient):
    note_id = 999
    mock_service = AsyncMock()
    mock_service.get_note.side_effect = NoteNotFoundError(note_id)

    async with override_note_service(app, mock_service):
        response = await client.get(f'/notes/{note_id}')

        assert response.status_code == codes.NOT_FOUND
        data = response.json()
        assert data == {'detail': f'Note not found: {note_id}'}
        mock_service.get_note.assert_called_once_with(note_id)


@pytest.mark.asyncio
async def test_get_notes(app: FastAPI, client: AsyncClient):
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

    async with override_note_service(app, mock_service):
        response = await client.get('/notes')

        assert response.status_code == codes.OK
        data = response.json()
        assert data == mock_notes
        mock_service.get_all_notes.assert_called_once()


@pytest.mark.asyncio
async def test_delete_note(app: FastAPI, client: AsyncClient):
    note_id = 1
    mock_service = AsyncMock()

    async with override_note_service(app, mock_service):
        response = await client.delete(f'/notes/{note_id}')

        assert response.status_code == codes.NO_CONTENT
        assert response.content == b''  # No content in response body
        mock_service.delete_note.assert_called_once_with(note_id)


@pytest.mark.asyncio
async def test_delete_note_not_found(app: FastAPI, client: AsyncClient):
    note_id = 999
    mock_service = AsyncMock()
    mock_service.delete_note.side_effect = NoteNotFoundError(note_id)

    async with override_note_service(app, mock_service):
        response = await client.delete(f'/notes/{note_id}')

        assert response.status_code == codes.NOT_FOUND
        data = response.json()
        assert data == {'detail': f'Note not found: {note_id}'}
        mock_service.delete_note.assert_called_once_with(note_id)


@pytest.mark.asyncio
async def test_create_task(app: FastAPI, client: AsyncClient):
    created_at = now_ist()
    mock_task = {
        'id': 1,
        'title': 'Test Task',
        'description': 'This is a test task.',
        'priority': 1,
        'created_at': created_at.isoformat(),
        'due_date': (created_at + timedelta(days=7)).isoformat(),
        'completed_at': None,
        'status': TaskStatus.NEW,
    }

    mock_service = AsyncMock()
    mock_service.create_task.return_value = mock_task

    async with override_tasks_service(app, mock_service):
        response = await client.post(
            '/tasks',
            json={
                'title': 'Test Task',
                'description': 'This is a test task.',
                'priority': 1,
                'due_date': (created_at + timedelta(days=7)).isoformat(),
            },
        )

        assert response.status_code == codes.OK
        data = response.json()
        assert data == mock_task
        mock_service.create_task.assert_called_once_with(
            TaskCreate(
                title='Test Task',
                description='This is a test task.',
                priority=1,
                due_date=(created_at + timedelta(days=7)).isoformat(),
            )
        )


@pytest.mark.asyncio
async def test_create_task_minimal(app: FastAPI, client: AsyncClient):
    created_at = now_ist()
    mock_task = {
        'id': 1,
        'title': 'Minimal Task',
        'description': None,
        'priority': None,
        'created_at': created_at.isoformat(),
        'due_date': None,
        'completed_at': None,
        'status': TaskStatus.NEW,
    }

    mock_service = AsyncMock()
    mock_service.create_task.return_value = mock_task

    async with override_tasks_service(app, mock_service):
        response = await client.post('/tasks', json={'title': 'Minimal Task'})

        assert response.status_code == codes.OK
        data = response.json()
        assert data == mock_task
        mock_service.create_task.assert_called_once_with(TaskCreate(title='Minimal Task'))
