# tests/tasknote/application/test_service.py
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.common.timeutils import now_ist
from src.tasknote.api.schemas import NoteCreate
from src.tasknote.application.note_service import NoteService
from src.tasknote.domain.exceptions import NoteNotFoundError
from src.tasknote.domain.models import Note


@pytest.mark.asyncio
async def test_create_note_calls_add_note():
    # Arrange
    mock_repository = AsyncMock()
    note_service = NoteService(repository=mock_repository)
    note_create = NoteCreate(title='Test Note', content='This is a test note from service.')

    # Act
    await note_service.create_note(note_create)

    # Assert
    mock_repository.add_note.assert_called_once()
    args, _ = mock_repository.add_note.call_args
    assert len(args) == 1
    note = args[0]
    assert note.title == 'Test Note'
    assert note.content == 'This is a test note from service.'
    assert isinstance(note.created_at, datetime)


@pytest.mark.asyncio
async def test_create_note_without_content():
    # Arrange
    mock_repository = AsyncMock()
    note_service = NoteService(repository=mock_repository)
    note_create = NoteCreate(title='Test Note Without Content')

    # Act
    await note_service.create_note(note_create)

    # Assert
    mock_repository.add_note.assert_called_once()
    args, _ = mock_repository.add_note.call_args
    assert len(args) == 1
    note = args[0]
    assert note.title == 'Test Note Without Content'
    assert note.content is None
    assert isinstance(note.created_at, datetime)


@pytest.mark.asyncio
async def test_get_note_returns_note():
    # Arrange
    mock_repository = AsyncMock()
    mock_note = Note(id=1, title='Test Note', content='This is a test note.', created_at=now_ist())
    mock_repository.get_note.return_value = mock_note
    note_service = NoteService(repository=mock_repository)

    # Act
    result = await note_service.get_note(1)

    # Assert
    assert result == mock_note
    mock_repository.get_note.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_note_propagates_not_found_error():
    # Arrange
    mock_repository = AsyncMock()
    mock_repository.get_note.side_effect = NoteNotFoundError(1)
    note_service = NoteService(repository=mock_repository)

    # Act & Assert
    with pytest.raises(NoteNotFoundError) as excinfo:
        await note_service.get_note(1)

    mock_repository.get_note.assert_called_once_with(1)
    assert 'Note not found: 1' in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_all_notes():
    # Arrange
    mock_repository = AsyncMock()
    mock_notes = [
        Note(id=1, title='Test Note 1', content='This is test note 1.', created_at=now_ist()),
        Note(id=2, title='Test Note 2', content='This is test note 2.', created_at=now_ist()),
    ]
    mock_repository.get_all.return_value = mock_notes
    note_service = NoteService(repository=mock_repository)

    # Act
    result = await note_service.get_all_notes()

    # Assert
    assert result == mock_notes
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_delete_note():
    # Arrange
    mock_repository = AsyncMock()
    note_service = NoteService(repository=mock_repository)
    note_id = 1

    # Act
    await note_service.delete_note(note_id)

    # Assert
    mock_repository.delete_note.assert_called_once_with(note_id)


@pytest.mark.asyncio
async def test_delete_note_propagates_not_found_error():
    # Arrange
    mock_repository = AsyncMock()
    mock_repository.delete_note.side_effect = NoteNotFoundError(1)
    note_service = NoteService(repository=mock_repository)

    # Act & Assert
    with pytest.raises(NoteNotFoundError) as excinfo:
        await note_service.delete_note(1)

    mock_repository.delete_note.assert_called_once_with(1)
    assert 'Note not found: 1' in str(excinfo.value)
