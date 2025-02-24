from abc import ABC, abstractmethod

from src.services.auth.dto import TokenDTO, UserDTO


class AuthService(ABC):
    @abstractmethod
    async def login(self, login: str, password: str, user_agent: str) -> TokenDTO:
        raise NotImplementedError

    @abstractmethod
    async def register(self, login: str, password: str, role: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, session_id: str) -> UserDTO:
        raise NotImplementedError
