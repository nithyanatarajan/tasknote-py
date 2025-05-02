# tests/tasknote/persistence/test_notes_repository.py
import asyncio

import pytest

from src.common.timeutils import now_ist
from src.tasknote.domain.exceptions import NoteNotFoundError
from src.tasknote.domain.models import Note


@pytest.fixture(scope='session')
async def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_add_note(notes_repository):
    note = Note(title='Test Note', content='This is a test note from notes_repository.', created_at=now_ist())
    added_note = await notes_repository.add_note(note)

    assert added_note.id is not None
    assert added_note.title == 'Test Note'
    assert added_note.content == 'This is a test note from notes_repository.'


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_all_notes(notes_repository):
    note1 = Note(title='Note 1', content='Content 1', created_at=now_ist())
    note2 = Note(title='Note 2', content='Content 2', created_at=now_ist())
    await notes_repository.add_note(note1)
    await notes_repository.add_note(note2)

    notes = await notes_repository.get_all()

    assert len(notes) >= 2  # More robust check
    titles = [note.title for note in notes]
    contents = [note.content for note in notes]

    assert 'Note 1' in titles
    assert 'Note 2' in titles
    assert 'Content 1' in contents
    assert 'Content 2' in contents


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_note(notes_repository):
    # Arrange
    note = Note(title='Test Get Note', content='This is a test for get_note.', created_at=now_ist())
    added_note = await notes_repository.add_note(note)

    # Act
    retrieved_note = await notes_repository.get_note(added_note.id)

    # Assert
    assert retrieved_note is not None
    assert retrieved_note.id == added_note.id
    assert retrieved_note.title == 'Test Get Note'
    assert retrieved_note.content == 'This is a test for get_note.'


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_note_not_found(notes_repository):
    # Arrange
    non_existent_id = 9999  # Assuming this ID doesn't exist

    # Act & Assert
    with pytest.raises(NoteNotFoundError) as excinfo:
        await notes_repository.get_note(non_existent_id)

    assert str(non_existent_id) in str(excinfo.value)
    assert 'Note not found' in str(excinfo.value)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_note(notes_repository):
    # Arrange
    note = Note(title='Test Delete Note', content='This is a test for delete_note.', created_at=now_ist())
    added_note = await notes_repository.add_note(note)

    # Act
    await notes_repository.delete_note(added_note.id)

    # Assert
    with pytest.raises(NoteNotFoundError):
        await notes_repository.get_note(added_note.id)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_note_not_found(notes_repository):
    # Arrange
    non_existent_id = 9999  # Assuming this ID doesn't exist

    # Act & Assert
    with pytest.raises(NoteNotFoundError) as excinfo:
        await notes_repository.delete_note(non_existent_id)

    assert str(non_existent_id) in str(excinfo.value)
    assert 'Note not found' in str(excinfo.value)
