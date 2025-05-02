from datetime import datetime

from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str | None = None


class NoteRead(BaseModel):
    id: int
    title: str
    content: str | None = None
    created_at: datetime
