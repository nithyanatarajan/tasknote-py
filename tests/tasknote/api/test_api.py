# tests/tasknote/api/test_api.py
from datetime import timedelta

import pytest

from fastapi import FastAPI
from httpx import AsyncClient, codes
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.timeutils import now_ist, to_isoz
from tests.tasknote.conftest import override_db_session


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_note_e2e(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        response = await client.post(
            '/notes', json={'title': 'E2E Note', 'content': 'This is a test note created from the full stack.'}
        )

        assert response.status_code == codes.OK
        body = response.json()
        assert body['title'] == 'E2E Note'
        assert body['content'] == 'This is a test note created from the full stack.'
        assert body['id'] is not None
        assert 'created_at' in body


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_note_without_content_e2e(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        response = await client.post('/notes', json={'title': 'Note Without Content'})

        assert response.status_code == codes.OK
        body = response.json()
        assert body['title'] == 'Note Without Content'
        assert body['content'] is None
        assert body['id'] is not None
        assert 'created_at' in body


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_note_e2e_success(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        # First create a note
        create_response = await client.post(
            '/notes', json={'title': 'Get Note Test', 'content': 'This is a test for get note.'}
        )

        assert create_response.status_code == codes.OK
        created_note = create_response.json()
        note_id = created_note['id']

        # Then retrieve the note
        get_response = await client.get(f'/notes/{note_id}')

        assert get_response.status_code == codes.OK
        retrieved_note = get_response.json()
        assert retrieved_note['id'] == note_id
        assert retrieved_note['title'] == 'Get Note Test'
        assert retrieved_note['content'] == 'This is a test for get note.'
        assert 'created_at' in retrieved_note


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_note_e2e_not_found(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        # Try to retrieve a non-existent note
        non_existent_id = 9999  # Assuming this ID doesn't exist
        response = await client.get(f'/notes/{non_existent_id}')

        assert response.status_code == codes.NOT_FOUND
        error = response.json()
        assert 'Note not found' in error['detail']
        assert str(non_existent_id) in error['detail']


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_notes_e2e(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        # First create a few notes
        await client.post(
            '/notes', json={'title': 'List Test Note 1', 'content': 'This is test note 1 for list endpoint.'}
        )
        await client.post(
            '/notes', json={'title': 'List Test Note 2', 'content': 'This is test note 2 for list endpoint.'}
        )

        # Then retrieve all notes
        response = await client.get('/notes')

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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_note_e2e_success(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        # First create a note
        create_response = await client.post(
            '/notes', json={'title': 'Delete Note Test', 'content': 'This is a test for delete note.'}
        )

        assert create_response.status_code == codes.OK
        created_note = create_response.json()
        note_id = created_note['id']

        # Then delete the note
        delete_response = await client.delete(f'/notes/{note_id}')

        assert delete_response.status_code == codes.NO_CONTENT
        assert delete_response.content == b''  # No content in response body

        # Verify the note is deleted by trying to get it
        get_response = await client.get(f'/notes/{note_id}')

        assert get_response.status_code == codes.NOT_FOUND
        error = get_response.json()
        assert 'Note not found' in error['detail']
        assert str(note_id) in error['detail']


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_note_e2e_not_found(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        # Try to delete a non-existent note
        non_existent_id = 9999  # Assuming this ID doesn't exist
        response = await client.delete(f'/notes/{non_existent_id}')

        assert response.status_code == codes.NOT_FOUND
        error = response.json()
        assert 'Note not found' in error['detail']
        assert str(non_existent_id) in error['detail']


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_task_e2e(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        # Create a task with all fields
        due_date = now_ist() + timedelta(days=7)
        response = await client.post(
            '/tasks',
            json={
                'title': 'E2E Task',
                'description': 'This is a test task created from the full stack.',
                'priority': 1,
                'due_date': due_date.isoformat(),
            },
        )

        assert response.status_code == codes.OK
        body = response.json()
        assert body['title'] == 'E2E Task'
        assert body['description'] == 'This is a test task created from the full stack.'
        assert body['priority'] == 1
        assert body['due_date'] == to_isoz(due_date)
        assert body['id'] is not None
        assert body['status'] == 'NEW'
        assert body['completed_at'] is None
        assert 'created_at' in body


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_task_minimal_e2e(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        # Create a task with only required fields
        response = await client.post('/tasks', json={'title': 'Minimal Task'})

        assert response.status_code == codes.OK
        body = response.json()
        assert body['title'] == 'Minimal Task'
        assert body['description'] is None
        assert body['priority'] is None
        assert body['due_date'] is None
        assert body['id'] is not None
        assert body['status'] == 'NEW'
        assert body['completed_at'] is None
        assert 'created_at' in body


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_tasks_e2e(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        # First create a few tasks
        await client.post(
            '/tasks',
            json={
                'title': 'List Test Task 1',
                'description': 'This is test task 1 for list endpoint.',
                'priority': 1,
            },
        )
        await client.post(
            '/tasks',
            json={
                'title': 'List Test Task 2',
                'description': 'This is test task 2 for list endpoint.',
                'priority': 2,
            },
        )

        # Then retrieve all tasks
        response = await client.get('/tasks')

        assert response.status_code == codes.OK
        tasks = response.json()
        assert isinstance(tasks, list)

        # Check if our test tasks are in the list
        titles = [task['title'] for task in tasks]
        descriptions = [task['description'] for task in tasks]

        assert 'List Test Task 1' in titles
        assert 'List Test Task 2' in titles
        assert 'This is test task 1 for list endpoint.' in descriptions
        assert 'This is test task 2 for list endpoint.' in descriptions

        # Verify each task has the expected structure
        for task in tasks:
            assert 'id' in task
            assert 'title' in task
            assert 'description' in task
            assert 'priority' in task
            assert 'created_at' in task
            assert 'due_date' in task
            assert 'completed_at' in task
            assert 'status' in task


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_task_e2e_success(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        # First create a task
        create_response = await client.post(
            '/tasks',
            json={
                'title': 'Get Task Test',
                'description': 'This is a test for get task.',
                'priority': 1,
            },
        )

        assert create_response.status_code == codes.OK
        created_task = create_response.json()
        task_id = created_task['id']

        # Then retrieve the task
        get_response = await client.get(f'/tasks/{task_id}')

        assert get_response.status_code == codes.OK
        retrieved_task = get_response.json()
        assert retrieved_task['id'] == task_id
        assert retrieved_task['title'] == 'Get Task Test'
        assert retrieved_task['description'] == 'This is a test for get task.'
        assert retrieved_task['priority'] == 1
        assert 'created_at' in retrieved_task
        assert retrieved_task['status'] == 'NEW'


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_task_e2e_not_found(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        # Try to retrieve a non-existent task
        non_existent_id = 9999  # Assuming this ID doesn't exist
        response = await client.get(f'/tasks/{non_existent_id}')

        assert response.status_code == codes.NOT_FOUND
        error = response.json()
        assert 'Task not found' in error['detail']
        assert str(non_existent_id) in error['detail']


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_task_e2e_success(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        # First create a task
        create_response = await client.post(
            '/tasks',
            json={
                'title': 'Delete Task Test',
                'description': 'This is a test for delete task.',
                'priority': 1,
            },
        )

        assert create_response.status_code == codes.OK
        created_task = create_response.json()
        task_id = created_task['id']

        # Then delete the task
        delete_response = await client.delete(f'/tasks/{task_id}')

        assert delete_response.status_code == codes.NO_CONTENT
        assert delete_response.content == b''  # No content in response body

        # Verify the task is deleted by trying to get it
        get_response = await client.get(f'/tasks/{task_id}')

        assert get_response.status_code == codes.NOT_FOUND
        error = get_response.json()
        assert 'Task not found' in error['detail']
        assert str(task_id) in error['detail']


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_task_e2e_not_found(app: FastAPI, session: AsyncSession, client: AsyncClient):
    async with override_db_session(app, session):
        # Try to delete a non-existent task
        non_existent_id = 9999  # Assuming this ID doesn't exist
        response = await client.delete(f'/tasks/{non_existent_id}')

        assert response.status_code == codes.NOT_FOUND
        error = response.json()
        assert 'Task not found' in error['detail']
        assert str(non_existent_id) in error['detail']
