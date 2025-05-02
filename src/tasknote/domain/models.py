# src/tasknote/domain/model.py
from datetime import datetime


class Note:
    def __init__(self, title: str, content: str, created_at: datetime, id: int | None = None):
        self.id = id
        self.title = title
        self.content = content
        self.created_at = created_at
