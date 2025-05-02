# src/tasknote/persistence/tasks_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasknote.persistence.mappers import tasks

from ..domain.exceptions import TaskNotFoundError
from ..domain.models import Task
from ..persistence.entities import TaskEntity


class TasksRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_task(self, task: Task) -> Task:
        task_orm = tasks.to_entity(task)
        self.session.add(task_orm)
        await self.session.commit()
        await self.session.refresh(task_orm)
        return tasks.to_domain(task_orm)

    async def get_all(self) -> list[Task]:
        result = await self.session.execute(select(TaskEntity))
        return [tasks.to_domain(row) for row in result.scalars().all()]

    async def get_task(self, task_id) -> Task:
        result = await self.session.execute(select(TaskEntity).where(TaskEntity.id == task_id))
        task_orm = result.scalars().first()
        if task_orm is None:
            raise TaskNotFoundError(task_id)
        return tasks.to_domain(task_orm)

    async def delete_task(self, task_id) -> None:
        result = await self.session.execute(select(TaskEntity).where(TaskEntity.id == task_id))
        task_orm = result.scalars().first()
        if task_orm is None:
            raise TaskNotFoundError(task_id)
        await self.session.delete(task_orm)
        await self.session.commit()
