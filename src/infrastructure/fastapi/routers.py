from fastapi import FastAPI
from src.api.auth.endpoints import router as auth_router
from src.api.health.endpoints import router as health_router
from src.api.tasks.endpoints import router as tasks_router


def add_routers(application: FastAPI) -> None:
    prefix = "/api"
    application.include_router(auth_router, prefix=prefix)
    application.include_router(health_router, prefix=prefix)
    application.include_router(tasks_router, prefix=prefix)
