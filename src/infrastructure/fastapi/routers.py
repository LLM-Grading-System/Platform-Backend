from fastapi import FastAPI
from src.api.health.endpoints import router as health_router


def add_routers(application: FastAPI) -> None:
    prefix = "/api"
    application.include_router(health_router, prefix=prefix)
