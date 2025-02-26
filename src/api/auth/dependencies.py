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
        user = await auth_service.get_user(auth_token)
    except NoUserError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_401_UNAUTHORIZED,
        ) from ex
    else:
        if user.role != "admin":
            raise APIError(
                message="У вас недостаточно прав для просмотра или совершения операции",
                status=status.HTTP_403_FORBIDDEN,
            )
        return user
