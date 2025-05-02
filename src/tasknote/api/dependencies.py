from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..application.note_service import NoteService
from ..application.tasks_service import TasksService
from ..persistence.db import get_db_session
from ..persistence.note_repository import NotesRepository
from ..persistence.tasks_repository import TasksRepository


def get_notes_repository(session: AsyncSession = Depends(get_db_session)) -> NotesRepository:
    return NotesRepository(session)


def get_note_service(repository: NotesRepository = Depends(get_notes_repository)) -> NoteService:
    return NoteService(repository)


def get_tasks_repository(session: AsyncSession = Depends(get_db_session)) -> TasksRepository:
    return TasksRepository(session)


def get_tasks_service(repository: TasksRepository = Depends(get_tasks_repository)) -> TasksService:
    return TasksService(repository)
