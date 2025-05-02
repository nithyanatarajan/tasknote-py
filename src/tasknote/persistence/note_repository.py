# src/tasknote/persistence/repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasknote.persistence.mappers import notes

from ..domain.exceptions import NoteNotFoundError
from ..domain.models import Note
from ..persistence.entities import NoteEntity


class NotesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_note(self, note: Note) -> Note:
        note_orm = notes.to_entity(note)
        self.session.add(note_orm)
        await self.session.commit()
        await self.session.refresh(note_orm)
        return notes.to_domain(note_orm)

    async def get_all(self) -> list[Note]:
        result = await self.session.execute(select(NoteEntity))
        return [notes.to_domain(row) for row in result.scalars().all()]

    async def get_note(self, note_id) -> Note:
        result = await self.session.execute(select(NoteEntity).where(NoteEntity.id == note_id))
        note_orm = result.scalars().first()
        if note_orm is None:
            raise NoteNotFoundError(note_id)
        return notes.to_domain(note_orm)

    async def delete_note(self, note_id) -> None:
        result = await self.session.execute(select(NoteEntity).where(NoteEntity.id == note_id))
        note_orm = result.scalars().first()
        if note_orm is None:
            raise NoteNotFoundError(note_id)
        await self.session.delete(note_orm)
        await self.session.commit()
