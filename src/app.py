import logging

from fastapi import FastAPI

from src.infrastructure.fastapi import add_custom_docs_endpoints, add_exception_handler, add_routers, lifespan
from src.infrastructure.fastapi.cors import add_cors

logging.basicConfig(level=logging.INFO)


def create_application() -> FastAPI:
    application = FastAPI(title="LLM Grading System", version="0.0.1", docs_url=None, redoc_url=None, lifespan=lifespan)
    add_routers(application)
    add_custom_docs_endpoints(application)
    add_exception_handler(application)
    add_cors(application)
    return application


app = create_application()
