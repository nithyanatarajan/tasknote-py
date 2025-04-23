# src/notes/api/router.py
from fastapi import APIRouter

from ..api.schemas import NoteCreate, NoteRead
from ..application.service import NoteService
from ..persistence.db import get_db_session
from ..persistence.repository import NotesRepository

router = APIRouter()


@router.get('/')
async def root():
    return {'message': 'Welcome to the Notes API'}


@router.get('/health')
async def health():
    return {'status': 'OK'}


@router.post('/notes', response_model=NoteRead)
async def create_note(note_create: NoteCreate):
    async with get_db_session() as session:
        service = NoteService(NotesRepository(session))
        note = await service.create_note(note_create)
        return note
