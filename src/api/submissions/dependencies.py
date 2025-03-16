from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.engine import get_async_session
from src.infrastructure.sqlalchemy.services import SqlAlchemySubmissionService
from src.services.submissions import SubmissionService


def get_submission_service(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> SubmissionService:
    return SqlAlchemySubmissionService(db_session)
