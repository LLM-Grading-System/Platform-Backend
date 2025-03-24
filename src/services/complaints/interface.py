from abc import ABC, abstractmethod

from src.services.complaints.dto import ComplaintDTO


class ComplaintService(ABC):
    @abstractmethod
    async def create_complaint(self, student_id: str, task_id: str, student_text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def answer_complaint(self, complaint_id: str, teacher_text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_complaints(self) -> list[ComplaintDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_complaint_by_id(self, complaint_id: str) -> ComplaintDTO:
        raise NotImplementedError
