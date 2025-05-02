# tests/tasknote/persistence/test_tasks_repository.py
import asyncio

from datetime import timedelta

import pytest

from src.common.timeutils import now_ist
from src.tasknote.domain.exceptions import TaskNotFoundError
from src.tasknote.domain.models import Task, TaskStatus


@pytest.fixture(scope='session')
async def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_add_task(tasks_repository):
    created_at = now_ist()
    task = Task(
        title='Test Task',
        created_at=created_at,
        description='This is a test task from tasks_repository.',
        priority=1,
        due_date=created_at + timedelta(days=7),
        completed_at=None,
        status=TaskStatus.NEW,
    )
    added_task = await tasks_repository.add_task(task)

    assert added_task.id is not None
    assert added_task.title == 'Test Task'
    assert added_task.description == 'This is a test task from tasks_repository.'
    assert added_task.priority == 1
    assert added_task.due_date is not None
    assert added_task.status == TaskStatus.NEW
    assert added_task.completed_at is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_add_task_minimal(tasks_repository):
    created_at = now_ist()
    task = Task(
        title='Minimal Task',
        created_at=created_at,
        description=None,
        priority=None,
        due_date=None,
        completed_at=None,
        status=TaskStatus.NEW,
    )
    added_task = await tasks_repository.add_task(task)

    assert added_task.id is not None
    assert added_task.title == 'Minimal Task'
    assert added_task.description is None
    assert added_task.priority is None
    assert added_task.due_date is None
    assert added_task.status == TaskStatus.NEW
    assert added_task.completed_at is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_all_tasks(tasks_repository):
    created_at = now_ist()
    task1 = Task(
        title='Task 1',
        created_at=created_at,
        description='Content 1',
        priority=1,
        due_date=created_at + timedelta(days=7),
        completed_at=None,
        status=TaskStatus.NEW,
    )
    task2 = Task(
        title='Task 2',
        created_at=created_at,
        description='Content 2',
        priority=2,
        due_date=created_at + timedelta(days=14),
        completed_at=None,
        status=TaskStatus.PENDING,
    )
    await tasks_repository.add_task(task1)
    await tasks_repository.add_task(task2)

    tasks = await tasks_repository.get_all()

    assert len(tasks) >= 2  # More robust check
    titles = [task.title for task in tasks]
    descriptions = [task.description for task in tasks]

    assert 'Task 1' in titles
    assert 'Task 2' in titles
    assert 'Content 1' in descriptions
    assert 'Content 2' in descriptions


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_task(tasks_repository):
    # Arrange
    created_at = now_ist()
    task = Task(
        title='Test Get Task',
        created_at=created_at,
        description='This is a test for get_task.',
        priority=1,
        due_date=created_at + timedelta(days=7),
        completed_at=None,
        status=TaskStatus.NEW,
    )
    added_task = await tasks_repository.add_task(task)

    # Act
    retrieved_task = await tasks_repository.get_task(added_task.id)

    # Assert
    assert retrieved_task is not None
    assert retrieved_task.id == added_task.id
    assert retrieved_task.title == 'Test Get Task'
    assert retrieved_task.description == 'This is a test for get_task.'
    assert retrieved_task.priority == 1
    assert retrieved_task.status == TaskStatus.NEW
    assert retrieved_task.completed_at is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_task_not_found(tasks_repository):
    # Arrange
    non_existent_id = 9999  # Assuming this ID doesn't exist

    # Act & Assert
    with pytest.raises(TaskNotFoundError) as excinfo:
        await tasks_repository.get_task(non_existent_id)

    assert str(non_existent_id) in str(excinfo.value)
    assert 'Task not found' in str(excinfo.value)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_task(tasks_repository):
    # Arrange
    created_at = now_ist()
    task = Task(
        title='Test Delete Task',
        created_at=created_at,
        description='This is a test for delete_task.',
        priority=1,
        due_date=created_at + timedelta(days=7),
        completed_at=None,
        status=TaskStatus.NEW,
    )
    added_task = await tasks_repository.add_task(task)

    # Act
    await tasks_repository.delete_task(added_task.id)

    # Assert
    with pytest.raises(TaskNotFoundError):
        await tasks_repository.get_task(added_task.id)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_task_not_found(tasks_repository):
    # Arrange
    non_existent_id = 9999  # Assuming this ID doesn't exist

    # Act & Assert
    with pytest.raises(TaskNotFoundError) as excinfo:
        await tasks_repository.delete_task(non_existent_id)

    assert str(non_existent_id) in str(excinfo.value)
    assert 'Task not found' in str(excinfo.value)
