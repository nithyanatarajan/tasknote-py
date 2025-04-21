from datetime import datetime

import pytest

from src.notes.domain.model import Note
from src.notes.persistence.repository import InMemoryNoteRepository


@pytest.fixture
async def repository():
    repo = InMemoryNoteRepository()
    # Clear notes before each test
    await repo.delete_all_notes()
    return repo


@pytest.mark.asyncio
async def test_add_note(repository):
    note = Note(title='Test Note', content='This is a test note.', created_at=datetime.now())
    added_note = await repository.add_note(note)

    assert added_note.id == 1
    assert added_note.title == 'Test Note'
    assert added_note.content == 'This is a test note.'


@pytest.mark.asyncio
async def test_get_all_notes(repository):
    note1 = Note(title='Note 1', content='Content 1', created_at=datetime.now())
    note2 = Note(title='Note 2', content='Content 2', created_at=datetime.now())
    await repository.add_note(note1)
    await repository.add_note(note2)

    notes = await repository.get_all_notes()

    assert len(notes) == 2
    assert notes[0].title == 'Note 1'
    assert notes[1].title == 'Note 2'
    assert notes[0].content == 'Content 1'
    assert notes[1].content == 'Content 2'
