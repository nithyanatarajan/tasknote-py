# src/tasknote/application/tasks_service.py
from src.common.timeutils import now_ist

from ..api.schemas import TaskCreate
from ..domain.models import Task
from ..logger import log
from ..persistence.tasks_repository import TasksRepository


class TasksService:
    def __init__(self, repository: TasksRepository):
        self.repository = repository

    async def create_task(self, task_create: TaskCreate) -> Task:
        created_at = now_ist()
        task = Task(
            title=task_create.title,
            created_at=created_at,
            description=task_create.description,
            priority=task_create.priority,
            due_date=task_create.due_date,
            completed_at=None,
        )
        log.info('Creating task', title=task.title, created_at=created_at.isoformat())
        return await self.repository.add_task(task)

    async def get_task(self, task_id: int) -> Task:
        log.info('Fetching task', task_id=task_id)
        return await self.repository.get_task(task_id)

    async def get_all_tasks(self) -> list[Task]:
        log.info('Fetching all tasks')
        return await self.repository.get_all()

    async def delete_task(self, task_id: int) -> None:
        log.info('Deleting task', task_id=task_id)
        await self.repository.delete_task(task_id)
