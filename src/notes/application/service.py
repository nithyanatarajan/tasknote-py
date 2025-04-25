from src.common.timeutils import now_ist

from ..api.schemas import NoteCreate
from ..domain.model import Note
from ..logger import log
from ..persistence.repository import NotesRepository


class NoteService:
    def __init__(self, repository: NotesRepository):
        self.repository = repository

    async def create_note(self, note_create: NoteCreate) -> Note:
        created_at = now_ist()
        note = Note(title=note_create.title, content=note_create.content, created_at=created_at)
        log.info('Creating note', title=note.title, created_at=created_at.isoformat())
        return await self.repository.add_note(note)

    async def get_note(self, note_id: int) -> Note:
        log.info('Fetching note', note_id=note_id)
        return await self.repository.get_note(note_id)
