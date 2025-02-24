from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.settings import app_settings

async_engine = create_async_engine(url=app_settings.db_url, echo=app_settings.is_dev)
async_session_factory = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session_factory() as session:
        yield session
