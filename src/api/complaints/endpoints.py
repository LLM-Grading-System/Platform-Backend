from typing import Annotated

from fastapi import APIRouter, Depends, status, Body, Path, Request
from starlette.responses import JSONResponse

from src.services.auth import UserDTO
from src.services.complaints import ComplaintService
from src.services.stundents import StudentService
from src.api.auth.dependencies import get_user
from src.api.complaints.dependencies import get_complaint_service
from src.api.students.dependencies import get_student_service
from src.api.complaints.schemas import ComplaintResponse, CreateComplaintRequest, CreateAnswerRequest
from src.api.utils import jsonify
from src.api.general_schemas import SuccessResponse


router = APIRouter(prefix="/complaints", tags=["complaints"])


@router.get(
    "",
    response_model=list[ComplaintResponse],
    status_code=status.HTTP_200_OK,
    description="Get all complaints",
    summary="Get complaints",
)
async def get_complaints(
    _: Annotated[UserDTO, Depends(get_user)],
    complaint_service: Annotated[ComplaintService, Depends(get_complaint_service)],
) -> JSONResponse:
    complaints = await complaint_service.get_complaints()
    return jsonify([ComplaintResponse.from_dto(complaint) for complaint in complaints])


@router.post(
    "",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create complaint",
    summary="Create complaint",
)
async def create_student_complaint(
    complaint_service: Annotated[ComplaintService, Depends(get_complaint_service)],
    student_service: Annotated[StudentService, Depends(get_student_service)],
    data: CreateComplaintRequest = Body(),
) -> JSONResponse:
    student = await student_service.get_by_telegram_user_id(data.student_telegram_user_id)
    await complaint_service.create_complaint(student.student_id, data.task_id, data.student_request)
    return jsonify(SuccessResponse(message="Жалоба успешно зарегистрирована, ожидайте ответа в Telegram"), status_code=status.HTTP_201_CREATED)


@router.patch(
    "/{complaint_id}/answer",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    description="Create complaint",
    summary="Create complaint",
)
async def answer_complaint(
    _: Annotated[UserDTO, Depends(get_user)],
    complaint_service: Annotated[ComplaintService, Depends(get_complaint_service)],
    complaint_id: str = Path(),
    data: CreateAnswerRequest = Body(),
) -> JSONResponse:
    await complaint_service.answer_complaint(complaint_id, data.teacher_response)
    return jsonify(SuccessResponse(message="Ответ на жалобу успешно зарегистрирован"))


@router.get(
    "/{complaint_id}",
    response_model=ComplaintResponse,
    status_code=status.HTTP_200_OK,
    description="Get complaint",
    summary="Get complaint",
)
async def get_complaint(
    _: Annotated[UserDTO, Depends(get_user)],
    complaint_service: Annotated[ComplaintService, Depends(get_complaint_service)],
    complaint_id: str = Path(),
) -> JSONResponse:
    complaint = await complaint_service.get_complaint_by_id(complaint_id)
    return jsonify(ComplaintResponse.from_dto(complaint))
