from uuid import UUID

from sqlmodel import desc, select

from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlalchemy.models import Criteria, Task
from src.services.tasks import (
    CriteriaDTO,
    NoCriteriaError,
    NoTaskError,
    SuchGitHubURLTaskExistError,
    TaskDTO,
    TaskService,
)


class SqlAlchemyTaskService(TaskService):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_task(
        self, name: str, description: str, github_repo_url: str, level: str, tags: list[str], is_draft: bool
    ) -> TaskDTO:
        query = select(Task).where(Task.gh_repo_url == github_repo_url)
        result = await self.session.execute(query)
        task = result.scalars().first()
        if task:
            raise SuchGitHubURLTaskExistError(message="Задача с таким github url уже существует")
        task = Task(
            name=name,
            description=description,
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
        description: str,
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
        task.description = description
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

    async def get_criteria_by_task_id(self, task_id: str) -> list[CriteriaDTO]:
        query = select(Criteria).where(Criteria.task_id == UUID(task_id)).order_by(desc(Criteria.created_at))
        result = await self.session.execute(query)
        criteria = result.scalars().all()
        return [self.from_criteria_model_to_dto(criterion) for criterion in criteria]

    async def add_criteria_for_task(self, task_id: str, description: str, weight: float) -> CriteriaDTO:
        criterion = Criteria(task_id=UUID(task_id), description=description, weight=weight)
        self.session.add(criterion)
        await self.session.commit()
        await self.session.refresh(criterion)
        return self.from_criteria_model_to_dto(criterion)

    async def edit_criteria_by_criteria_id(self, criteria_id: str, description: str, weight: float) -> CriteriaDTO:
        criterion = await self._get_criteria_by_criteria_id(criteria_id)
        criterion.description = description
        criterion.weight = weight
        await self.session.commit()
        await self.session.refresh(criterion)
        return self.from_criteria_model_to_dto(criterion)

    async def remove_criteria_by_criteria_id(self, criteria_id: str) -> None:
        criterion = await self._get_criteria_by_criteria_id(criteria_id)
        await self.session.delete(criterion)
        await self.session.commit()

    async def _get_task_by_task_id(self, task_id: str) -> Task:
        query = select(Task).where(Task.task_id == UUID(task_id))
        result = await self.session.execute(query)
        task = result.scalars().first()
        if task is None:
            raise NoTaskError(message="Задачи с таким идентификатором не существует")
        return task

    async def _get_criteria_by_criteria_id(self, criteria_id: str) -> Criteria:
        query = select(Criteria).where(Criteria.criteria_id == UUID(criteria_id))
        result = await self.session.execute(query)
        criterion = result.scalars().first()
        if criterion is None:
            raise NoCriteriaError(message="Критерия с таким идентификатором не существует")
        return criterion

    @staticmethod
    def from_model_to_dto(model: Task) -> TaskDTO:
        return TaskDTO(
            task_id=str(model.task_id),
            name=model.name,
            description=model.description,
            github_repo_url=model.gh_repo_url,
            level=model.level,
            tags=model.tags.split(",") if model.tags else [],
            is_draft=model.is_draft,
        )

    @staticmethod
    def from_criteria_model_to_dto(model: Criteria) -> CriteriaDTO:
        return CriteriaDTO(
            criteria_id=str(model.criteria_id),
            task_id=str(model.task_id),
            description=model.description,
            weight=model.weight,
            created_at=model.created_at,
        )
