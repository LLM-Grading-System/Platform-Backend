import uuid

from pydantic import Field

from src.api.base_schema import BaseSchema
from src.services.stundents import StudentDTO


class CreateStudentRequest(BaseSchema):
    telegram_user_id: int = Field(examples=[42353453])
    telegram_username: str = Field(examples=["nikita"])

class SetGithubRequest(BaseSchema):
    github_username: str = Field(examples=["Nicki"])


class StudentResponse(BaseSchema):
    student_id: str = Field(examples=[uuid.uuid4()])
    telegram_user_id: int = Field(examples=[42353453])
    telegram_username: str = Field(examples=["nikita"])
    github_username: str = Field(examples=["Nicki"])
    registered_at: int = Field(examples=[1742159850])

    @staticmethod
    def from_dto(student: StudentDTO) -> "StudentResponse":
        return StudentResponse(
            student_id=student.student_id,
            telegram_user_id=student.telegram_user_id,
            telegram_username=student.telegram_username,
            github_username=student.github_username,
            registered_at=int(student.registered_at.timestamp()),
        )