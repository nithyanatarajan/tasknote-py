# src/notes/persistence/repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..domain.model import Note
from ..persistence.entities import NoteEntity
from ..persistence.mappers import to_domain, to_entity


class NotesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_note(self, note: Note) -> Note:
        note_orm = to_entity(note)
        self.session.add(note_orm)
        await self.session.commit()
        await self.session.refresh(note_orm)
        return to_domain(note_orm)

    async def get_all(self) -> list[Note]:
        result = await self.session.execute(select(NoteEntity))
        return [to_domain(row) for row in result.scalars().all()]
