from uuid import UUID

from sqlmodel import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlalchemy.models import Complaint
from src.services.exceptions import NotFoundError
from src.services.complaints import ComplaintDTO, ComplaintService


class SqlAlchemyComplaintService(ComplaintService):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_complaint(self, student_id: str, task_id: str, student_text: str) -> None:
        complaint = Complaint(student_id=UUID(student_id), task_id=UUID(task_id), student_request=student_text)
        self.session.add(complaint)
        await self.session.commit()

    async def answer_complaint(self, complaint_id: str, teacher_text: str) -> None:
        complaint = await self._get_complaint_by_id(complaint_id)
        complaint.teacher_response = teacher_text
        self.session.add(complaint)
        await self.session.commit()

    async def get_complaints(self) -> list[ComplaintDTO]:
        query = select(Complaint).order_by(desc(Complaint.created_at))
        result = await self.session.execute(query)
        complaints = result.scalars().all()
        return [self.from_model_to_dto(complaint) for complaint in complaints]

    async def get_complaint_by_id(self, complaint_id: str) -> ComplaintDTO:
        complaint = await self._get_complaint_by_id(complaint_id)
        return self.from_model_to_dto(complaint)

    @staticmethod
    def from_model_to_dto(model: Complaint) -> ComplaintDTO:
        return ComplaintDTO(
            complaint_id=str(model.complaint_id),
            student_id=str(model.student_id),
            task_id=str(model.task_id),
            student_request=model.student_request,
            teacher_response=model.teacher_response,
            created_at=model.created_at,
        )

    async def _get_complaint_by_id(self, complaint_id: str) -> Complaint:
        query = select(Complaint).where(Complaint.complaint_id == UUID(complaint_id))
        result = await self.session.execute(query)
        complaint = result.scalar_one_or_none()
        if not complaint:
            raise NotFoundError(f"Жалоба с ID {complaint_id} не найдена")
        return complaint
