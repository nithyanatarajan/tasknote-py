from typing import ClassVar

from ..domain.model import Note


class InMemoryNoteRepository:
    _notes: ClassVar[list[Note]] = []  # Shared across all instances

    async def add_note(self, note: Note) -> Note:
        note.id = len(self._notes) + 1
        self._notes.append(note)
        return note

    async def get_all_notes(self) -> list[Note]:
        return self._notes

    async def delete_all_notes(self):
        self._notes.clear()
