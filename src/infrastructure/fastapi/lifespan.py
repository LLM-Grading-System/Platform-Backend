from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from src.infrastructure.minio.scripts import create_bucket_if_not_exist
from src.infrastructure.sqlalchemy.scripts import init_database


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[dict[Any, Any], Any]:  # noqa: ARG001
    await init_database()
    await create_bucket_if_not_exist()
    yield {}
