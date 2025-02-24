from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api.exceptions import APIError
from src.api.schemas import ErrorResponse


def add_exception_handler(application: FastAPI) -> None:
    @application.exception_handler(APIError)
    async def handle_application_error(_: Request, exc: APIError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status,
            content=ErrorResponse(message=exc.message).model_dump(),
        )
