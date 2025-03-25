from abc import ABC, abstractmethod

from src.services.stundents.dto import StudentDTO


class StudentService(ABC):
    @abstractmethod
    async def get_all(self, username: str = "") -> list[StudentDTO]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, telegram_user_id: int, telegram_username: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_github_username(self, telegram_user_id: int,github_username: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_github_username(self, github_username: str) -> StudentDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_telegram_user_id(self, telegram_user_id: int) -> StudentDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, student_id: str) -> StudentDTO:
        raise NotImplementedError