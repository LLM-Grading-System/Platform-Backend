## Task

Complete target section by examples

## Example Services

dto.py
```Python
@dataclass
class TokenDTO:
    token: str


@dataclass
class UserDTO:
    user_id: str
    login: str
    role: str
    created_at: datetime

```

auth.py
```Python
from abc import ABC, abstractmethod

from src.services.auth.dto import TokenDTO, UserDTO


class AuthService(ABC):
    @abstractmethod
    async def login(self, login: str, password: str, user_agent: str) -> TokenDTO:
        raise NotImplementedError
```

exceptions.py
```Python
from dataclasses import dataclass


@dataclass
class NoUserError(Exception):
    message: str
```

sqlalchemy_auth.py
```Python
from datetime import datetime, timedelta
from uuid import UUID

from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.infrastructure.sqlalchemy.models import Session, User
from src.services.auth import (
    SESSION_TTL,
    AuthService,
    InvalidPasswordError,
    NoUserError,
    TokenDTO,
    UserAlreadyExistError,
    UserDTO,
)
from src.services.password import PasswordService


class SqlAlchemyAuthService(AuthService):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def login(self, login: str, password: str, user_agent: str) -> TokenDTO:
        user = await self._get_user_by_login(login)
        if not user:
            raise NoUserError(message="Пользователь с таким именем не существует")
        is_verified = PasswordService.verify_password(password, user.hashed_password, user.salt)
        if not is_verified:
            raise InvalidPasswordError(message="Пароль неправильный")
        expired_datetime = datetime.now() + timedelta(days=SESSION_TTL)
        session = Session(user_id=user.user_id, expired_at=expired_datetime, user_agent=user_agent)
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return TokenDTO(token=str(session.session_id))
```


## Example Endpoints

dependencies.py
```Python
from __future__ import annotations

from typing import Annotated

from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.exceptions import APIError
from src.infrastructure.sqlalchemy.engine import get_async_session
from src.infrastructure.sqlalchemy.services import SqlAlchemyAuthService
from src.services.auth import AuthService, NoUserError, UserDTO


def get_auth_service(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> AuthService:
    return SqlAlchemyAuthService(db_session)


def get_auth_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))]) -> str:
    if not credentials:
        raise APIError(
            message="Требуется войти в аккаунт",
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return credentials.credentials


async def get_user(
    auth_token: Annotated[str, Depends(get_auth_token)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserDTO:
    try:
        return await auth_service.get_user(auth_token)
    except NoUserError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_401_UNAUTHORIZED,
        ) from ex
```

schemas.py
```Python

import uuid

from pydantic import BaseModel, Field

from src.services.auth import UserDTO


class TokenResponse(BaseModel):
    token: str = Field(examples=[str(uuid.uuid4())])


class LoginRequest(BaseModel):
    login: str
    password: str
    user_agent: str
```

endpoints.py
```Python
@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    description="User login",
    summary="User Login",
)
async def login(
    data: Annotated[LoginRequest, Body()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> JSONResponse:
    try:
        token_data = await auth_service.login(data.login, data.password, data.user_agent)
        return JSONResponse(
            content=TokenResponse(token=token_data.token).model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except NoUserError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_404_NOT_FOUND,
        ) from ex
    except InvalidPasswordError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_400_BAD_REQUEST,
        ) from ex
```

## Target Service

dto.py
```Python
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TaskDTO:
    task_id: str
    name: str
    description: str
    github_repo_url: str
    level: str
    tags: list[str]
    is_draft: bool


@dataclass
class CriteriaDTO:
    criteria_id: str
    description: str
    weight: float
    created_at: datetime
```

exceptions.py
```Python
@dataclass
class NoTaskError(Exception):
    message: str


@dataclass
class NoCriteriaError(Exception):
    message: str
```

interface.py
```Python
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
```

sqlalchemy_tasks.py
```Python
from uuid import UUID

from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlalchemy.models import Criteria, Task
from src.services.tasks import CriteriaDTO, NoCriteriaError, NoTaskError, TaskDTO, TaskService


class SqlAlchemyTaskService(TaskService):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_task(
        self, name: str, description: str, github_repo_url: str, level: str, tags: list[str], is_draft: bool
    ) -> TaskDTO:
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
        query = select(Criteria).where(Criteria.task_id == UUID(task_id))
        result = await self.session.execute(query)
        criteria = result.scalars().all()
        return [self.from_criteria_model_to_dto(criterion) for criterion in criteria]

    async def add_criteria_for_task(self, task_id: str, description: str, weight: float) -> None:
        criteria = Criteria(task_id=UUID(task_id), description=description, weight=weight)
        self.session.add(criteria)
        await self.session.commit()

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
            description=model.description,
            weight=model.weight,
            created_at=model.created_at,
        )

```

## Important Rules
- Each endpoint returns JSONResponse
- Each error excepts like this:
```Python
from src.api.exceptions import APIError

except NoUserError as ex:
    raise APIError(
        message=ex.message,
        status=status.HTTP_404_NOT_FOUND,
    ) from ex 
```
- Implement static method from_dto in schema class
- In endpoints body use entity without "dto"-suffix
- In endpoints params use Annotated
- For DELETE endpoints return 200 OK response
- In endpoints body use model_dump instead ot dict to get dictionary from pydantic-model

## Target Endpoints

