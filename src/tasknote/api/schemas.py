from datetime import datetime

from pydantic import BaseModel

from ..domain.models import TaskStatus


class NoteCreate(BaseModel):
    title: str
    content: str | None = None


class NoteRead(BaseModel):
    id: int
    title: str
    content: str | None = None
    created_at: datetime


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: int | None = None
    due_date: datetime | None = None


class TaskRead(BaseModel):
    id: int
    title: str
    created_at: datetime
    status: TaskStatus
    description: str | None = None
    priority: int | None = None
    due_date: datetime | None = None
    completed_at: datetime | None = None
