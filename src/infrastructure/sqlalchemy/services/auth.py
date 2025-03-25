from datetime import datetime, timedelta
from uuid import UUID

from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.infrastructure.sqlalchemy.models import Session, User
from src.services.auth import (
    SESSION_TTL,
    AuthService,
    TokenDTO,
    UserDTO,
)
from src.services.exceptions import NotFoundError, InvalidPropertyError, AlreadyExistError
from src.services.password import PasswordService


class SqlAlchemyAuthService(AuthService):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def login(self, login: str, password: str, user_agent: str) -> TokenDTO:
        user = await self._get_user_by_login(login)
        if not user:
            raise NotFoundError(message="Пользователь с таким именем не существует")
        is_verified = PasswordService.verify_password(password, user.hashed_password, user.salt)
        if not is_verified:
            raise InvalidPropertyError(message="Пароль неправильный")
        expired_datetime = datetime.now() + timedelta(days=SESSION_TTL)
        session = Session(user_id=user.user_id, expired_at=expired_datetime, user_agent=user_agent)
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return TokenDTO(token=str(session.session_id))

    async def register(self, login: str, password: str, role: str) -> None:
        existing_user = await self._get_user_by_login(login)
        if existing_user:
            raise AlreadyExistError(message="Пользователь с таким именем уже существует")
        hashed_password, salt = PasswordService.create_hashed_password_and_salt(password)
        user = User(login=login, salt=salt, hashed_password=hashed_password, role=role)
        self.session.add(user)
        await self.session.commit()

    async def get_user(self, session_id: str) -> UserDTO:
        # Check user
        query = select(User).join(Session).where(Session.session_id == UUID(session_id))
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError(message="Пользователь не найден")
        # Check session
        query = select(Session).where(Session.session_id == UUID(session_id))
        result = await self.session.execute(query)
        session = result.scalar_one_or_none()
        if session.expired_at < datetime.now():
            raise NotFoundError(message="Срок действия сессии истек, требуется перезайти в аккаунт")
        return UserDTO(
            user_id=str(user.user_id),
            login=user.login,
            role=user.role,
            created_at=user.created_at,
        )

    async def _get_user_by_login(self, login: str) -> User | None:
        query = select(User).where(User.login == login)
        result = await self.session.execute(query)
        return result.scalars().first()
