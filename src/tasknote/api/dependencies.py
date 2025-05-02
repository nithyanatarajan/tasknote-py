from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..application.note_service import NoteService
from ..persistence.db import get_db_session
from ..persistence.note_repository import NotesRepository


def get_notes_repository(session: AsyncSession = Depends(get_db_session)) -> NotesRepository:
    return NotesRepository(session)


def get_note_service(repository: NotesRepository = Depends(get_notes_repository)) -> NoteService:
    return NoteService(repository)
