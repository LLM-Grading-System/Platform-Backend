import uuid

from pydantic import BaseModel, Field

from src.services.auth import UserDTO


class TokenResponse(BaseModel):
    token: str = Field(examples=[str(uuid.uuid4())])


class UserResponse(BaseModel):
    user_id: str
    login: str
    role: str
    created_at: int

    @staticmethod
    def from_dto(user: UserDTO) -> "UserResponse":
        return UserResponse(
            user_id=user.user_id, login=user.login, role=user.role, created_at=int(user.created_at.timestamp())
        )


class LoginRequest(BaseModel):
    login: str
    password: str
    user_agent: str


class RegisterRequest(BaseModel):
    login: str
    password: str
    role: str
