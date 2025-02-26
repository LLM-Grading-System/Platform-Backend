from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from starlette.responses import JSONResponse

from src.api.auth.dependencies import get_auth_service, get_user
from src.api.auth.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from src.api.exceptions import APIError
from src.api.general_schemas import SuccessResponse
from src.api.utils import jsonify
from src.services.auth import AuthService, InvalidPasswordError, NoUserError, UserAlreadyExistError, UserDTO

router = APIRouter(prefix="/auth", tags=["authorization"])


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    description="Get current user",
    summary="Getting user",
)
async def get_current_user(
    user: Annotated[UserDTO, Depends(get_user)],
) -> JSONResponse:
    return jsonify(UserResponse.from_dto(user))


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    description="User login",
    summary="User Login",
)
async def login(
    data: Annotated[LoginRequest, Body()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> JSONResponse:
    try:
        token_data = await auth_service.login(data.login, data.password, data.user_agent)
        return jsonify(TokenResponse(token=token_data.token))
    except NoUserError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_404_NOT_FOUND,
        ) from ex
    except InvalidPasswordError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_400_BAD_REQUEST,
        ) from ex


@router.post(
    "/register",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    description="User  registration",
    summary="User  Registration",
)
async def register(
    register_request: Annotated[RegisterRequest, Body()],
    _: Annotated[UserDTO, Depends(get_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> JSONResponse:
    try:
        await auth_service.register(
            login=register_request.login, password=register_request.password, role=register_request.role
        )
        return jsonify(SuccessResponse(message="Аккаунт успешно создан"), status_code=status.HTTP_201_CREATED)
    except UserAlreadyExistError as ex:
        raise APIError(
            message=ex.message,
            status=status.HTTP_400_BAD_REQUEST,
        ) from ex
