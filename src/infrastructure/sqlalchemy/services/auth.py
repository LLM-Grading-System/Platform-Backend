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

    async def register(self, login: str, password: str, role: str) -> None:
        existing_user = await self._get_user_by_login(login)
        if existing_user:
            raise UserAlreadyExistError(message="Пользователь с таким именем уже существует")
        hashed_password, salt = PasswordService.create_hashed_password_and_salt(password)
        user = User(login=login, salt=salt, hashed_password=hashed_password, role=role)
        self.session.add(user)
        await self.session.commit()

    async def get_user(self, session_id: str) -> UserDTO:
        query = select(User).options(joinedload(User.sessions)).where(Session.session_id == UUID(session_id))
        result = await self.session.execute(query)
        user = result.scalars().first()
        if not user:
            raise NoUserError(message="Пользователь не найден")
        if user.sessions[0].expired_at < datetime.now():
            raise NoUserError(message="Требуется перезайти в аккаунт")
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
