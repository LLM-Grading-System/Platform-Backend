from uuid import uuid4

from pydantic import Field

from src.api.base_schema import BaseSchema
from src.services.tasks import CriteriaDTO, TaskDTO


class TaskResponse(BaseSchema):
    task_id: str = Field(examples=[str(uuid4())])
    name: str
    description: str
    github_repo_url: str
    level: str
    tags: list[str]
    is_draft: bool

    @staticmethod
    def from_dto(task: TaskDTO) -> "TaskResponse":
        return TaskResponse(
            task_id=task.task_id,
            name=task.name,
            description=task.description,
            github_repo_url=task.github_repo_url,
            level=task.level,
            tags=task.tags,
            is_draft=task.is_draft,
        )


class CriteriaResponse(BaseSchema):
    task_id: str = Field(examples=[str(uuid4())])
    criteria_id: str = Field(examples=[str(uuid4())])
    description: str
    weight: float
    created_at: int

    @staticmethod
    def from_dto(criteria: CriteriaDTO) -> "CriteriaResponse":
        return CriteriaResponse(
            criteria_id=criteria.criteria_id,
            task_id=criteria.task_id,
            description=criteria.description,
            weight=criteria.weight,
            created_at=int(criteria.created_at.timestamp()),
        )


class CreateTaskRequest(BaseSchema):
    name: str
    description: str
    github_repo_url: str
    level: str
    tags: list[str]
    is_draft: bool


class EditTaskRequest(BaseSchema):
    name: str
    description: str
    github_repo_url: str
    level: str
    tags: list[str]
    is_draft: bool


class AddCriteriaRequest(BaseSchema):
    description: str
    weight: float


class EditCriteriaRequest(BaseSchema):
    description: str
    weight: float
