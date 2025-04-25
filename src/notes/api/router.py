# src/notes/api/router.py
from fastapi import APIRouter, Depends, HTTPException

from ..api.schemas import NoteCreate, NoteRead
from ..application.service import NoteService
from ..domain.exceptions import NoteNotFoundError
from .dependencies import get_note_service

router = APIRouter()


@router.get('/')
async def root():
    return {'message': 'Welcome to the Notes API'}


@router.get('/health')
async def health():
    return {'status': 'OK'}


@router.post('/notes', response_model=NoteRead)
async def create_note(note_create: NoteCreate, service: NoteService = Depends(get_note_service)):
    return await service.create_note(note_create)


@router.get('/notes/{note_id}', response_model=NoteRead)
async def get_note(note_id: int, service: NoteService = Depends(get_note_service)):
    try:
        return await service.get_note(note_id)
    except NoteNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message) from e
