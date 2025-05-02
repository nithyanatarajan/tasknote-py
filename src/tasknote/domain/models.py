# src/tasknote/domain/model.py
from datetime import datetime
from enum import Enum


class Note:
    def __init__(self, title: str, content: str | None, created_at: datetime, id: int | None = None):
        self.id = id
        self.title = title
        self.content = content
        self.created_at = created_at


class TaskStatus(str, Enum):
    NEW = 'NEW'
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'


class Task:
    def __init__(  # noqa: PLR0913
        self,
        title: str,
        created_at: datetime,
        description: str | None,
        priority: int | None,
        due_date: datetime | None,
        completed_at: datetime | None,
        status: TaskStatus = TaskStatus.NEW,
        id: int | None = None,
    ):
        self.id = id
        self.title = title
        self.created_at = created_at
        self.status = status

        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed_at = completed_at
