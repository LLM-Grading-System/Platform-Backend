from abc import ABC, abstractmethod

from src.services.tasks.dto import CriteriaDTO, TaskDTO


class TaskService(ABC):
    @abstractmethod
    def create_task(
        self, name: str, description: str, github_repo_url: str, level: str, tags: list[str], is_draft: bool
    ) -> TaskDTO:
        raise NotImplementedError

    @abstractmethod
    def get_task_by_github_repository_url(self, github_repo_url: str) -> TaskDTO:
        raise NotImplementedError

    @abstractmethod
    def get_task_by_task_id(self, task_id: str) -> TaskDTO:
        raise NotImplementedError

    @abstractmethod
    def get_all_tasks(self) -> list[TaskDTO]:
        raise NotImplementedError

    @abstractmethod
    def edit_task_by_task_id(
        self,
        task_id: str,
        name: str,
        description: str,
        github_repo_url: str,
        level: str,
        tags: list[str],
        is_draft: bool,
    ) -> TaskDTO:
        raise NotImplementedError

    @abstractmethod
    def remove_task_by_task_id(self, task_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_criteria_by_task_id(self, task_id: str) -> list[CriteriaDTO]:
        raise NotImplementedError

    @abstractmethod
    def add_criteria_for_task(self, task_id: str, description: str, weight: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def edit_criteria_by_criteria_id(self, criteria_id: str, description: str, weight: float) -> CriteriaDTO:
        raise NotImplementedError

    @abstractmethod
    def remove_criteria_by_criteria_id(self, criteria_id: str) -> None:
        raise NotImplementedError
