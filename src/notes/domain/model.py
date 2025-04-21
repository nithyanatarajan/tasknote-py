from datetime import datetime


class Note:
    id = 0

    def __init__(self, title: str, content: str, created_at: datetime):
        self.title = title
        self.content = content
        self.created_at = created_at
