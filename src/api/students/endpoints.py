from typing import Annotated

from fastapi import APIRouter, Depends, status, Body
from fastapi.params import Query
from starlette.responses import JSONResponse

from src.api.auth.dependencies import get_user
from src.api.students.dependencies import get_student_service
from src.api.students.schemas import StudentResponse, CreateStudentRequest
from src.api.utils import jsonify
from src.api.general_schemas import SuccessResponse
from src.services.auth import UserDTO
from src.services.stundents import StudentService


router = APIRouter(prefix="/students", tags=["students"])


@router.get(
    "",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    description="Get all students",
    summary="Get students",
)
async def get_students(
    _: Annotated[UserDTO, Depends(get_user)],
    student_service: Annotated[StudentService, Depends(get_student_service)],
    query: str = Query(default="")
) -> JSONResponse:
    students = await student_service.get_all(query)
    return jsonify([StudentResponse.from_dto(student) for student in students])


@router.post(
    "",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create student",
    summary="Create student",
)
async def create_student(
    student_service: Annotated[StudentService, Depends(get_student_service)],
    data: CreateStudentRequest = Body(),
) -> JSONResponse:
    await student_service.create(data.telegram_user_id, data.telegram_username, data.github_username)
    return jsonify(SuccessResponse(message="Студент успешно зарегистрирован"), status_code=status.HTTP_201_CREATED)
