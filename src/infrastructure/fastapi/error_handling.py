from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.api.exceptions import APIError
from src.api.general_schemas import ErrorResponse
from src.api.utils import jsonify
from src.services.exceptions import ServiceError, NotFoundError, AlreadyExistError, InvalidPropertyError


def add_exception_handler(application: FastAPI) -> None:
    @application.exception_handler(APIError)
    async def handle_application_error(_: Request, exc: APIError) -> JSONResponse:
        return jsonify(ErrorResponse(message=exc.message), status_code=exc.status)

    @application.exception_handler(ServiceError)
    async def handle_application_error(_: Request, exc: ServiceError) -> JSONResponse:
        if isinstance(exc, NotFoundError):
            status_code = status.HTTP_404_NOT_FOUND
        elif isinstance(exc, AlreadyExistError):
            status_code = status.HTTP_409_CONFLICT
        elif isinstance(exc, InvalidPropertyError):
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            status_code = status.HTTP_400_BAD_REQUEST
        return jsonify(ErrorResponse(message=exc.message), status_code=status_code)
