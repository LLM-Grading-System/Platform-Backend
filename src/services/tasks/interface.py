from abc import ABC, abstractmethod

from src.services.tasks.dto import TaskDTO


class TaskService(ABC):
    @abstractmethod
    async def create_task(
        self, name: str, system_instructions: str, ideas: str, github_repo_url: str, level: str, tags: list[str], is_draft: bool
    ) -> TaskDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_github_repository_url(self, github_repo_url: str) -> TaskDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_task_id(self, task_id: str) -> TaskDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_all_tasks(self, public_only: bool = False) -> list[TaskDTO]:
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
    async def remove_task_by_task_id(self, task_id: str) -> None:
        raise NotImplementedError
