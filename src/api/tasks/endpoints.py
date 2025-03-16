from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from src.api.auth.dependencies import get_user
from src.api.general_schemas import SuccessResponse
from src.api.tasks.dependencies import get_task_service
from src.api.tasks.schemas import (
    CreateTaskRequest,
    EditTaskRequest,
    TaskResponse,
)
from src.api.utils import jsonify
from src.services.auth import UserDTO
from src.services.tasks import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a new task",
    summary="Create Task",
)
async def create_task(
    data: CreateTaskRequest,
    _: Annotated[UserDTO, Depends(get_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> JSONResponse:
    task = await task_service.create_task(
        name=data.name,
        system_instructions=data.system_instructions,
        ideas=data.ideas,
        github_repo_url=data.github_repo_url,
        level=data.level,
        tags=data.tags,
        is_draft=data.is_draft,
    )
    return jsonify(TaskResponse.from_dto(task), status_code=status.HTTP_201_CREATED)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    description="Get task by ID",
    summary="Get Task",
)
async def get_task(
    task_id: str,
    _: Annotated[UserDTO, Depends(get_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> JSONResponse:
    task = await task_service.get_task_by_task_id(task_id)
    return jsonify(TaskResponse.from_dto(task))


@router.get(
    "",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK,
    description="Get all tasks",
    summary="Get All Tasks",
)
async def get_all_tasks(
    _: Annotated[UserDTO, Depends(get_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> JSONResponse:
    tasks = await task_service.get_all_tasks()
    return jsonify([TaskResponse.from_dto(task) for task in tasks])


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    description="Edit task by ID",
    summary="Edit Task",
)
async def edit_task(
    task_id: str,
    data: EditTaskRequest,
    _: Annotated[UserDTO, Depends(get_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> JSONResponse:
    task = await task_service.edit_task_by_task_id(
        task_id=task_id,
        name=data.name,
        system_instructions=data.system_instructions,
        ideas=data.ideas,
        github_repo_url=data.github_repo_url,
        level=data.level,
        tags=data.tags,
        is_draft=data.is_draft,
    )
    return jsonify(TaskResponse.from_dto(task))


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    description="Remove task by ID",
    summary="Remove Task",
)
async def remove_task(
    task_id: str,
    _: Annotated[UserDTO, Depends(get_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> JSONResponse:
    await task_service.remove_task_by_task_id(task_id)
    return jsonify(SuccessResponse(message="Задача успешно удалена"))
