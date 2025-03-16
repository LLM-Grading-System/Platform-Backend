from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from src.infrastructure.sqlalchemy.models import SQLModel, User
from src.services.auth import Role
from src.services.password import PasswordService
from src.settings import app_settings


async def create_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def create_admin_user(engine: AsyncEngine, login: str, password: str) -> None:
    async with AsyncSession(engine) as session:
        query = select(User).where(User.login == login)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            hashed_password, salt = PasswordService.create_hashed_password_and_salt(password)
            user = User(login=login, salt=salt, hashed_password=hashed_password, role=Role.ADMIN.value)
            session.add(user)
            await session.commit()


async def init_database() -> None:
    engine = create_async_engine(url=app_settings.db_url, echo=app_settings.is_dev)
    await create_tables(engine)

    await create_admin_user(engine, app_settings.ADMIN_USER, app_settings.ADMIN_PASSWORD)
