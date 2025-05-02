# tests/tasknote/application/test_tasks_service.py
from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from src.common.timeutils import now_ist
from src.tasknote.api.schemas import TaskCreate
from src.tasknote.application.tasks_service import TasksService
from src.tasknote.domain.exceptions import TaskNotFoundError
from src.tasknote.domain.models import Task, TaskStatus


@pytest.mark.asyncio
async def test_create_task_calls_add_task():
    # Arrange
    mock_repository = AsyncMock()
    tasks_service = TasksService(repository=mock_repository)
    task_create = TaskCreate(
        title='Test Task',
        description='This is a test task from service.',
        priority=1,
        due_date=(now_ist() + timedelta(days=7)),
    )

    # Act
    await tasks_service.create_task(task_create)

    # Assert
    mock_repository.add_task.assert_called_once()
    args, _ = mock_repository.add_task.call_args
    assert len(args) == 1
    task = args[0]
    assert task.title == 'Test Task'
    assert task.description == 'This is a test task from service.'
    assert task.priority == 1
    assert task.due_date is not None
    assert task.status == TaskStatus.NEW
    assert task.completed_at is None
    assert isinstance(task.created_at, datetime)


@pytest.mark.asyncio
async def test_create_task_minimal():
    # Arrange
    mock_repository = AsyncMock()
    tasks_service = TasksService(repository=mock_repository)
    task_create = TaskCreate(title='Minimal Task')

    # Act
    await tasks_service.create_task(task_create)

    # Assert
    mock_repository.add_task.assert_called_once()
    args, _ = mock_repository.add_task.call_args
    assert len(args) == 1
    task = args[0]
    assert task.title == 'Minimal Task'
    assert task.description is None
    assert task.priority is None
    assert task.due_date is None
    assert task.status == TaskStatus.NEW
    assert task.completed_at is None
    assert isinstance(task.created_at, datetime)


@pytest.mark.asyncio
async def test_get_task_returns_task():
    # Arrange
    mock_repository = AsyncMock()
    mock_task = Task(
        id=1,
        title='Test Task',
        created_at=now_ist(),
        description='This is a test task.',
        priority=1,
        due_date=now_ist() + timedelta(days=7),
        completed_at=None,
        status=TaskStatus.NEW,
    )
    mock_repository.get_task.return_value = mock_task
    tasks_service = TasksService(repository=mock_repository)

    # Act
    result = await tasks_service.get_task(1)

    # Assert
    assert result == mock_task
    mock_repository.get_task.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_task_propagates_not_found_error():
    # Arrange
    mock_repository = AsyncMock()
    mock_repository.get_task.side_effect = TaskNotFoundError(1)
    tasks_service = TasksService(repository=mock_repository)

    # Act & Assert
    with pytest.raises(TaskNotFoundError) as excinfo:
        await tasks_service.get_task(1)

    mock_repository.get_task.assert_called_once_with(1)
    assert 'Task not found: 1' in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_all_tasks():
    # Arrange
    mock_repository = AsyncMock()
    mock_tasks = [
        Task(
            id=1,
            title='Test Task 1',
            created_at=now_ist(),
            description='This is test task 1.',
            priority=1,
            due_date=now_ist() + timedelta(days=7),
            completed_at=None,
            status=TaskStatus.NEW,
        ),
        Task(
            id=2,
            title='Test Task 2',
            created_at=now_ist(),
            description='This is test task 2.',
            priority=2,
            due_date=now_ist() + timedelta(days=14),
            completed_at=None,
            status=TaskStatus.PENDING,
        ),
    ]
    mock_repository.get_all.return_value = mock_tasks
    tasks_service = TasksService(repository=mock_repository)

    # Act
    result = await tasks_service.get_all_tasks()

    # Assert
    assert result == mock_tasks
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_delete_task():
    # Arrange
    mock_repository = AsyncMock()
    tasks_service = TasksService(repository=mock_repository)
    task_id = 1

    # Act
    await tasks_service.delete_task(task_id)

    # Assert
    mock_repository.delete_task.assert_called_once_with(task_id)


@pytest.mark.asyncio
async def test_delete_task_propagates_not_found_error():
    # Arrange
    mock_repository = AsyncMock()
    mock_repository.delete_task.side_effect = TaskNotFoundError(1)
    tasks_service = TasksService(repository=mock_repository)

    # Act & Assert
    with pytest.raises(TaskNotFoundError) as excinfo:
        await tasks_service.delete_task(1)

    mock_repository.delete_task.assert_called_once_with(1)
    assert 'Task not found: 1' in str(excinfo.value)
