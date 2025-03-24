from fastapi import FastAPI
from src.api.auth.endpoints import router as auth_router
from src.api.health.endpoints import router as health_router
from src.api.tasks.endpoints import router as tasks_router
from src.api.submissions.endpoints import router as submissions_router
from src.api.students.endpoints import router as students_router
from src.api.complaints.endpoints import router as complaints_router
from src.infrastructure.faststream.kafka_router import kafka_router


def add_routers(application: FastAPI) -> None:
    prefix = "/api"
    application.include_router(health_router, prefix=prefix)
    application.include_router(auth_router, prefix=prefix)
    application.include_router(tasks_router, prefix=prefix)
    application.include_router(submissions_router, prefix=prefix)
    application.include_router(students_router, prefix=prefix)
    application.include_router(complaints_router, prefix=prefix)
    application.include_router(kafka_router)
