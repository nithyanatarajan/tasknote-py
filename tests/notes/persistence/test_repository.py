# tests/notes/persistence/test_repository.py
import asyncio

import pytest

from src.common.timeutils import now_ist
from src.notes.domain.model import Note


@pytest.fixture(scope='session')
async def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_add_note(repository):
    note = Note(title='Test Note', content='This is a test note from repository.', created_at=now_ist())
    added_note = await repository.add_note(note)

    assert added_note.id is not None
    assert added_note.title == 'Test Note'
    assert added_note.content == 'This is a test note from repository.'


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_all_notes(repository):
    note1 = Note(title='Note 1', content='Content 1', created_at=now_ist())
    note2 = Note(title='Note 2', content='Content 2', created_at=now_ist())
    await repository.add_note(note1)
    await repository.add_note(note2)

    notes = await repository.get_all()

    assert len(notes) >= 2  # More robust check
    titles = [note.title for note in notes]
    contents = [note.content for note in notes]

    assert 'Note 1' in titles
    assert 'Note 2' in titles
    assert 'Content 1' in contents
    assert 'Content 2' in contents
