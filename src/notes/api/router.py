from fastapi import APIRouter

from ..api.schemas import NoteCreate, NoteRead
from ..application.service import NoteService
from ..persistence.repository import InMemoryNoteRepository

router = APIRouter()


# Dependency
async def get_note_service() -> NoteService:
    repository = InMemoryNoteRepository()
    return NoteService(repository)


@router.post('/notes', response_model=NoteRead)
async def create_note(note_create: NoteCreate):
    service = await get_note_service()
    note = await service.create_note(note_create)
    return note
