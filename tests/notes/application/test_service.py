# tests/notes/application/test_service.py
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.notes.api.schemas import NoteCreate
from src.notes.application.service import NoteService


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
