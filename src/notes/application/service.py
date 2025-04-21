from src.common.timeutils import now_ist

from ..api.schemas import NoteCreate
from ..domain.model import Note
from ..logger import log
from ..persistence.repository import InMemoryNoteRepository


class NoteService:
    def __init__(self, repository: InMemoryNoteRepository):
        self.repository = repository

    async def create_note(self, note_create: NoteCreate) -> Note:
        created_at = now_ist()
        note = Note(title=note_create.title, content=note_create.content, created_at=created_at)
        log.info('Creating note', title=note.title, created_at=created_at.isoformat())
        return await self.repository.add_note(note)
