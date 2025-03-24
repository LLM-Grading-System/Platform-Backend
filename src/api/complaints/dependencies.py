from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.engine import get_async_session
from src.infrastructure.sqlalchemy.services import SqlAlchemyComplaintService
from src.services.complaints import ComplaintService


def get_complaint_service(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ComplaintService:
    return SqlAlchemyComplaintService(db_session)
