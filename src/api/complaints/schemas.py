import uuid

from pydantic import Field

from src.api.base_schema import BaseSchema
from src.services.complaints import ComplaintDTO


class CreateComplaintRequest(BaseSchema):
    task_id: str = Field(examples=[uuid.uuid4()])
    student_telegram_user_id: int = Field(examples=[3252352523])
    student_request: str = Field(examples=["Не работает ничего!"])


class CreateAnswerRequest(BaseSchema):
    teacher_response: str = Field(examples=["Напишите ChatGPT"])


class ComplaintResponse(BaseSchema):
    complaint_id: str = Field(examples=[uuid.uuid4()])
    task_id: str = Field(examples=[uuid.uuid4()])
    student_id: str = Field(examples=[uuid.uuid4()])
    student_request: str = Field(examples=["Не работает ничего!"])
    teacher_response: str = Field(examples=[""])
    created_at: int = Field(examples=[1742159850])

    @staticmethod
    def from_dto(complaint: ComplaintDTO) -> "ComplaintResponse":
        return ComplaintResponse(
            complaint_id=complaint.complaint_id,
            task_id=complaint.task_id,
            student_id=complaint.student_id,
            student_request=complaint.student_request,
            teacher_response=complaint.teacher_response,
            created_at=int(complaint.created_at.timestamp()),
        )
