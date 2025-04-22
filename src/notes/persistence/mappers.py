from src.notes.domain.model import Note
from src.notes.persistence.entities import NoteEntity


def to_domain(entity: NoteEntity) -> Note:
    return Note(
        title=entity.title,
        content=entity.content,
        created_at=entity.created_at,
    )


def to_entity(model: Note) -> NoteEntity:
    return NoteEntity(
        title=model.title,
        content=model.content,
        created_at=model.created_at,
    )
