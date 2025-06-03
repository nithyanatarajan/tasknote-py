# src/tasknote/api/router.py
from fastapi import APIRouter, Depends, HTTPException

from ..api.schemas import NoteCreate, NoteRead, TaskCreate, TaskRead
from ..application.note_service import NoteService
from ..application.tasks_service import TasksService
from ..domain.exceptions import NoteNotFoundError, TaskNotFoundError
from .dependencies import get_note_service, get_tasks_service

router = APIRouter()


@router.get('/welcome')
async def root():
    return {'message': 'Welcome to the TaskNote'}


@router.get('/health')
async def health():
    return {'status': 'OK'}


@router.post('/notes', response_model=NoteRead)
async def create_note(note_create: NoteCreate, service: NoteService = Depends(get_note_service)):
    return await service.create_note(note_create)


@router.get('/notes', response_model=list[NoteRead])
async def get_notes(service: NoteService = Depends(get_note_service)):
    return await service.get_all_notes()


@router.get('/notes/{note_id}', response_model=NoteRead)
async def get_note(note_id: int, service: NoteService = Depends(get_note_service)):
    try:
        return await service.get_note(note_id)
    except NoteNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message) from e


@router.delete('/notes/{note_id}', status_code=204)
async def delete_note(note_id: int, service: NoteService = Depends(get_note_service)):
    try:
        await service.delete_note(note_id)
    except NoteNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message) from e


@router.post('/tasks', response_model=TaskRead)
async def create_task(task_create: TaskCreate, service: TasksService = Depends(get_tasks_service)):
    return await service.create_task(task_create)


@router.get('/tasks', response_model=list[TaskRead])
async def get_tasks(service: TasksService = Depends(get_tasks_service)):
    return await service.get_all_tasks()


@router.get('/tasks/{task_id}', response_model=TaskRead)
async def get_task(task_id: int, service: TasksService = Depends(get_tasks_service)):
    try:
        return await service.get_task(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message) from e


@router.delete('/tasks/{task_id}', status_code=204)
async def delete_task(task_id: int, service: TasksService = Depends(get_tasks_service)):
    try:
        await service.delete_task(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message) from e
