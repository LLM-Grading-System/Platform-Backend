from abc import ABC, abstractmethod

from src.services.stundents.dto import StudentDTO


class StudentService(ABC):
    @abstractmethod
    async def get_all(self, username: str = "") -> list[StudentDTO]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, telegram_user_id: int, telegram_username: str, github_username: str) -> None:
        raise NotImplementedError
