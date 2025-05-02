# src/tasknote/persistence/mappers/tasks.py
from src.tasknote.domain.models import Task
from src.tasknote.persistence.entities import TaskEntity


def to_domain(entity: TaskEntity) -> Task:
    return Task(
        id=entity.id,
        title=entity.title,
        created_at=entity.created_at,
        description=entity.description,
        priority=entity.priority,
        due_date=entity.due_date,
        completed_at=entity.completed_at,
        status=entity.status,
    )


def to_entity(model: Task) -> TaskEntity:
    return TaskEntity(
        title=model.title,
        created_at=model.created_at,
        description=model.description,
        priority=model.priority,
        due_date=model.due_date,
        completed_at=model.completed_at,
        status=model.status,
    )
