from pydantic import Field

from src.api.base_schema import BaseSchema


class ErrorResponse(BaseSchema):
    message: str = Field(examples=["Произошла ошибка при обработке запроса"])


class SuccessResponse(BaseSchema):
    message: str = Field(examples=["Операция успешно выполнена"])
