from uuid import uuid4

from pydantic import Field

from src.api.base_schema import BaseSchema
from src.services.tasks import TaskDTO


class TaskResponse(BaseSchema):
    task_id: str = Field(examples=[str(uuid4())])
    name: str
    system_instructions: str
    ideas: str
    github_repo_url: str
    level: str
    tags: list[str]
    is_draft: bool

    @staticmethod
    def from_dto(task: TaskDTO) -> "TaskResponse":
        return TaskResponse(
            task_id=task.task_id,
            name=task.name,
            system_instructions=task.system_instructions,
            ideas=task.ideas,
            github_repo_url=task.github_repo_url,
            level=task.level,
            tags=task.tags,
            is_draft=task.is_draft,
        )


class TaskPromptResponse(BaseSchema):
    system_instructions: str
    github_repo_url: str

    @staticmethod
    def from_dto(task: TaskDTO) -> "TaskPromptResponse":
        return TaskPromptResponse(
            system_instructions=task.system_instructions,
            github_repo_url=task.github_repo_url,
        )


class CreateTaskRequest(BaseSchema):
    name: str
    system_instructions: str
    ideas: str
    github_repo_url: str
    level: str
    tags: list[str]
    is_draft: bool


class EditTaskRequest(BaseSchema):
    name: str
    system_instructions: str
    ideas: str
    github_repo_url: str
    level: str
    tags: list[str]
    is_draft: bool
