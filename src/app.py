import logging
from src.infrastructure.fastapi import add_custom_docs_endpoints, add_routers

from fastapi import FastAPI


logging.basicConfig(level=logging.INFO)


def create_application() -> FastAPI:
    application = FastAPI(
        title="LLM Grading System",
        version="0.0.1",
        docs_url=None,
        redoc_url=None,
    )
    add_custom_docs_endpoints(application)
    add_routers(application)
    return application


app = create_application()
