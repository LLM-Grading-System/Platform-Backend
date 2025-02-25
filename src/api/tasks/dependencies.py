from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.engine import get_async_session
from src.infrastructure.sqlalchemy.services import SqlAlchemyTaskService
from src.services.tasks import TaskService


def get_task_service(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> TaskService:
    return SqlAlchemyTaskService(db_session)
