from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api.exceptions import APIError
from src.api.general_schemas import ErrorResponse
from src.api.utils import jsonify


def add_exception_handler(application: FastAPI) -> None:
    @application.exception_handler(APIError)
    async def handle_application_error(_: Request, exc: APIError) -> JSONResponse:
        return jsonify(ErrorResponse(message=exc.message), status_code=exc.status)
