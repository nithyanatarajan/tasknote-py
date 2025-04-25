class NoteNotFoundError(Exception):
    """Exception raised when a note is not found."""

    def __init__(self, note_id: int, message: str = 'Note not found'):
        self.note_id = note_id
        self.message = f'{message}: {note_id}'
        super().__init__(self.message)
