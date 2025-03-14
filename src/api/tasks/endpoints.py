from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import JSONResponse

from src.api.auth.dependencies import get_user
from src.api.exceptions import APIError
from src.api.general_schemas import SuccessResponse
from src.api.tasks.dependencies import get_task_service
from src.api.tasks.schemas import (
    AddCriteriaRequest,
    CreateTaskRequest,
    CriteriaResponse,
    EditCriteriaRequest,
    EditTaskRequest,
    TaskResponse,
)
from src.api.utils import jsonify
from src.services.auth import UserDTO
from src.services.tasks import NoCriteriaError, NoTaskError, SuchGitHubURLTaskExistError, TaskService

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
    try:
        task = await task_service.create_task(
            name=data.name,
            description=data.description,
            github_repo_url=data.github_repo_url,
            level=data.level,
            tags=data.tags,
            is_draft=data.is_draft,
        )
        return jsonify(TaskResponse.from_dto(task), status_code=status.HTTP_201_CREATED)
    except SuchGitHubURLTaskExistError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_400_BAD_REQUEST,
        ) from ex


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
    try:
        task = await task_service.get_task_by_task_id(task_id)
        return jsonify(TaskResponse.from_dto(task))
    except NoTaskError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_404_NOT_FOUND,
        ) from ex


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
    gh_repo_url: str | None = Query(default=None),
) -> JSONResponse:
    if gh_repo_url:
        try:
            task = await task_service.get_task_by_github_repository_url(gh_repo_url)
            return jsonify([TaskResponse.from_dto(task)])
        except NoTaskError:
            return jsonify([])
    else:
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
    try:
        task = await task_service.edit_task_by_task_id(
            task_id=task_id,
            name=data.name,
            description=data.description,
            github_repo_url=data.github_repo_url,
            level=data.level,
            tags=data.tags,
            is_draft=data.is_draft,
        )
        return jsonify(TaskResponse.from_dto(task))
    except NoTaskError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_404_NOT_FOUND,
        ) from ex
    except SuchGitHubURLTaskExistError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_400_BAD_REQUEST,
        ) from ex


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
    try:
        await task_service.remove_task_by_task_id(task_id)
        return jsonify(SuccessResponse(message="Задача успешно удалена"))
    except NoTaskError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_404_NOT_FOUND,
        ) from ex


@router.post(
    "/{task_id}/criteria",
    response_model=CriteriaResponse,
    status_code=status.HTTP_201_CREATED,
    description="Add criteria for a task",
    summary="Add Criteria",
)
async def add_criteria(
    task_id: str,
    data: AddCriteriaRequest,
    _: Annotated[UserDTO, Depends(get_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> JSONResponse:
    criteria = await task_service.add_criteria_for_task(task_id, data.description, data.weight)
    return jsonify(CriteriaResponse.from_dto(criteria), status_code=status.HTTP_201_CREATED)


@router.get(
    "/{task_id}/criteria",
    response_model=list[CriteriaResponse],
    status_code=status.HTTP_200_OK,
    description="Get criteria by task ID",
    summary="Get Criteria by Task ID",
)
async def get_criteria_by_task_id(
    task_id: Annotated[str, Path()],
    _: Annotated[UserDTO, Depends(get_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> JSONResponse:
    try:
        await task_service.get_task_by_task_id(task_id)
        criteria = await task_service.get_criteria_by_task_id(task_id)
        return jsonify([CriteriaResponse.from_dto(criterion) for criterion in criteria])
    except NoCriteriaError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_404_NOT_FOUND,
        ) from ex
    except NoTaskError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_404_NOT_FOUND,
        ) from ex


@router.put(
    "/{task_id}/criteria/{criteria_id}",
    response_model=CriteriaResponse,
    status_code=status.HTTP_200_OK,
    description="Edit criteria by ID",
    summary="Edit Criteria",
)
async def edit_criteria(
    criteria_id: Annotated[str, Path()],
    task_id: Annotated[str, Path()],
    data: EditCriteriaRequest,
    _: Annotated[UserDTO, Depends(get_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> JSONResponse:
    try:
        await task_service.get_task_by_task_id(task_id)
        criteria = await task_service.edit_criteria_by_criteria_id(criteria_id, data.description, data.weight)
        return jsonify(CriteriaResponse.from_dto(criteria))
    except NoCriteriaError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_404_NOT_FOUND,
        ) from ex
    except NoTaskError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_404_NOT_FOUND,
        ) from ex


@router.delete(
    "/{task_id}/criteria/{criteria_id}",
    status_code=status.HTTP_200_OK,
    description="Remove criteria by ID",
    summary="Remove Criteria",
)
async def remove_criteria(
    criteria_id: Annotated[str, Path()],
    task_id: Annotated[str, Path()],
    _: Annotated[UserDTO, Depends(get_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> JSONResponse:
    try:
        await task_service.get_task_by_task_id(task_id)
        await task_service.remove_criteria_by_criteria_id(criteria_id)
        return jsonify(SuccessResponse(message="Критерий успешно удален"))
    except NoCriteriaError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_404_NOT_FOUND,
        ) from ex
    except NoTaskError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_404_NOT_FOUND,
        ) from ex
