from uuid import UUID

from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlalchemy.models import Task
from src.services.tasks import (
    NoTaskError,
    SuchGitHubURLTaskExistError,
    TaskDTO,
    TaskService,
)


class SqlAlchemyTaskService(TaskService):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_task(
        self, name: str, system_instructions: str, ideas: str, github_repo_url: str, level: str, tags: list[str], is_draft: bool
    ) -> TaskDTO:
        query = select(Task).where(Task.gh_repo_url == github_repo_url)
        result = await self.session.execute(query)
        task = result.scalars().first()
        if task:
            raise SuchGitHubURLTaskExistError(message="Задача с таким github url уже существует")
        task = Task(
            name=name,
            system_instructions=system_instructions,
            ideas=ideas,
            gh_repo_url=github_repo_url,
            level=level,
            tags=",".join(tags),
            is_draft=is_draft,
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return self.from_model_to_dto(task)

    async def get_task_by_github_repository_url(self, github_repo_url: str) -> TaskDTO:
        query = select(Task).where(Task.gh_repo_url == github_repo_url)
        result = await self.session.execute(query)
        task = result.scalars().first()
        if task is None:
            raise NoTaskError(message="Задачи с таким URL не существует")
        return self.from_model_to_dto(task)

    async def get_task_by_task_id(self, task_id: str) -> TaskDTO:
        task = await self._get_task_by_task_id(task_id)
        return self.from_model_to_dto(task)

    async def get_all_tasks(self) -> list[TaskDTO]:
        query = select(Task)
        result = await self.session.execute(query)
        tasks = result.scalars().all()
        return [self.from_model_to_dto(task) for task in tasks]

    async def edit_task_by_task_id(
        self,
        task_id: str,
        name: str,
        system_instructions: str,
        ideas: str,
        github_repo_url: str,
        level: str,
        tags: list[str],
        is_draft: bool,
    ) -> TaskDTO:
        query = select(Task).where(Task.gh_repo_url == github_repo_url, Task.task_id != UUID(task_id))
        result = await self.session.execute(query)
        task = result.scalars().first()
        if task:
            raise SuchGitHubURLTaskExistError(message="Задача с таким github url уже существует")
        task = await self._get_task_by_task_id(task_id)
        task.name = name
        task.system_instructions = system_instructions
        task.ideas = ideas
        task.gh_repo_url = github_repo_url
        task.level = level
        task.tags = ",".join(tags)
        task.is_draft = is_draft
        await self.session.commit()
        await self.session.refresh(task)
        return self.from_model_to_dto(task)

    async def remove_task_by_task_id(self, task_id: str) -> None:
        task = await self._get_task_by_task_id(task_id)
        await self.session.delete(task)
        await self.session.commit()

    async def _get_task_by_task_id(self, task_id: str) -> Task:
        query = select(Task).where(Task.task_id == UUID(task_id))
        result = await self.session.execute(query)
        task = result.scalars().first()
        if task is None:
            raise NoTaskError(message="Задачи с таким идентификатором не существует")
        return task

    @staticmethod
    def from_model_to_dto(model: Task) -> TaskDTO:
        return TaskDTO(
            task_id=str(model.task_id),
            name=model.name,
            system_instructions=model.system_instructions,
            ideas=model.ideas,
            github_repo_url=model.gh_repo_url,
            level=model.level,
            tags=model.tags.split(",") if model.tags else [],
            is_draft=model.is_draft,
        )
