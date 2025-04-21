from datetime import datetime

import pytest

from src.notes.api.schemas import NoteCreate
from src.notes.application.service import NoteService
from src.notes.persistence.repository import InMemoryNoteRepository


@pytest.fixture
async def repository():
    repo = InMemoryNoteRepository()
    # Clear notes before each test
    await repo.delete_all_notes()
    return repo


@pytest.fixture
async def service(repository):
    return NoteService(repository)


@pytest.mark.asyncio
async def test_create_note(service):
    note_create = NoteCreate(title='Test Note', content='This is a test note.')
    note = await service.create_note(note_create)

    assert note.id == 1
    assert note.title == 'Test Note'
    assert note.content == 'This is a test note.'
    assert isinstance(note.created_at, datetime)
