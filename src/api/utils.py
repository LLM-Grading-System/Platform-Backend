from fastapi import status
from fastapi.responses import JSONResponse

from src.api.base_schema import BaseSchema


def jsonify(response: BaseSchema | list[BaseSchema], status_code: int = status.HTTP_200_OK) -> JSONResponse:
    if isinstance(response, BaseSchema):
        data = response.model_dump(by_alias=True)
    elif isinstance(response, list):
        data = [res.model_dump(by_alias=True) for res in response]
    else:
        error_message = f"Тип {type(response)} не обрабатывается jsonify"
        raise TypeError(error_message)
    return JSONResponse(
        content=data,
        status_code=status_code,
    )
