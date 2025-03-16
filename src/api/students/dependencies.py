from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.engine import get_async_session
from src.infrastructure.sqlalchemy.services import SqlAlchemyStudentService
from src.services.stundents import StudentService


def get_student_service(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> StudentService:
    return SqlAlchemyStudentService(db_session)
