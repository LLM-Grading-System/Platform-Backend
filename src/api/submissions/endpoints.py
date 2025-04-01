import io
import json
import uuid
import zipfile
from typing import Annotated

import aiohttp
from fastapi import APIRouter, File, UploadFile, Depends, status, Header, Body, Path
from faststream.kafka import KafkaBroker
from starlette.responses import JSONResponse
from miniopy_async import Minio

from src.api.auth.dependencies import get_user
from src.api.students.dependencies import get_student_service
from src.api.submissions.dependencies import get_submission_service
from src.api.submissions.events import SUBMISSION_TOPIC, SubmissionEventSchema, CreateCommentRequest
from src.api.submissions.schemas import SubmissionResponse, EvaluationSubmissionRequest
from src.api.tasks.dependencies import get_task_service
from src.api.utils import jsonify
from src.api.general_schemas import SuccessResponse
from src.infrastructure.faststream.dependencies import get_broker
from src.infrastructure.minio.client import get_s3_client
from src.services.auth import UserDTO
from src.services.exceptions import NotFoundError
from src.services.stundents import StudentService
from src.services.submissions import SubmissionService
from src.services.tasks import TaskService
from src.settings import app_settings

router = APIRouter(prefix="/submissions", tags=["submissions"])


@router.get(
    "",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    description="Get all submissions",
    summary="Get submissions",
)
async def get_submissions(
    _: Annotated[UserDTO, Depends(get_user)],
    submission_service: Annotated[SubmissionService, Depends(get_submission_service)],
) -> JSONResponse:
    submissions = await submission_service.get_all_submissions()
    return jsonify([SubmissionResponse.from_dto(submission) for submission in submissions])


@router.put(
    "/{submission_id}",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    description="Update submission with feedback",
    summary="Update submission",
)
async def evaluate_submission(
    broker: Annotated[KafkaBroker, Depends(get_broker)],
    submission_service: Annotated[SubmissionService, Depends(get_submission_service)],
    submission_id: str = Path(),
    data: EvaluationSubmissionRequest = Body(),
) -> JSONResponse:
    submission_dto = await submission_service.evaluate_submission(submission_id, data.llm_grade, data.llm_feedback, json.dumps(data.llm_report))
    parts = submission_dto.gh_repo_url.split('/')
    gh_username, gh_repo_name =  parts[3], parts[4]
    await broker.publish(
        CreateCommentRequest(
            username=gh_username,
            repo_name=gh_repo_name,
            pull_request_number=submission_dto.gh_pull_request_number,
            comment=submission_dto.llm_feedback
        ), topic=SUBMISSION_TOPIC
    )
    return jsonify(SuccessResponse(message="Вердикт успешно сохранен"))


@router.post(
    "",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    description="Submission successfully created",
    summary="Create submissions",
)
async def create_submission(
    broker: Annotated[KafkaBroker, Depends(get_broker)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    student_service: Annotated[StudentService, Depends(get_student_service)],
    submission_service: Annotated[SubmissionService, Depends(get_submission_service)],
    client: Annotated[Minio, Depends(get_s3_client)],
    autotests_log: UploadFile = File(...),
    linters_log: UploadFile = File(...),
    code: UploadFile = File(...),
    github_owner: str = Header(default="", alias="X-GitHub-Owner"),
    github_repository: str = Header(default="", alias="X-GitHub-Repository"),
    github_pull_request_number: int = Header(default="", alias="X-GitHub-Pull-Request-Number"),
) -> JSONResponse:
    github_repo_api_url = f"https://api.github.com/repos/{github_owner}/{github_repository}"
    async with aiohttp.ClientSession() as session:
        res = await session.get(github_repo_api_url)
        data: dict = await res.json(encoding="utf-8")

    if "status" in data.keys() and data["status"] != 200:
        error_message = data["message"]
        return jsonify(SuccessResponse(message=f"Репозиторий не существует или не доступен ({error_message})"), status_code=status.HTTP_400_BAD_REQUEST)
    elif "parent" not in data.keys():
        return jsonify(SuccessResponse(message="Репозиторий не является форком"), status_code=status.HTTP_400_BAD_REQUEST)
    current_repository_url = data["svn_url"]
    parent_repository_url = data["parent"]["svn_url"]
    try:
        task = await task_service.get_task_by_github_repository_url(parent_repository_url)
    except NotFoundError:
        return jsonify(SuccessResponse(message="Репозиторий не является форком репозитория какого-либо задания"), status_code=status.HTTP_404_NOT_FOUND)
    try:
        student = await student_service.get_by_github_username(github_owner)
    except NotFoundError:
        return jsonify(SuccessResponse(message=f"Студент с профилем {github_owner} на GitHub не зарегистрирован"), status_code=status.HTTP_404_NOT_FOUND)

    code_filename = f"{str(uuid.uuid4())}.zip"
    code_zip_buffer = io.BytesIO()
    with zipfile.ZipFile(code_zip_buffer, 'w') as zip_file:
        for file in [autotests_log, linters_log, code]:
            zip_file.writestr(file.filename, await file.read())
    code_zip_buffer.seek(0)
    await client.put_object(
        app_settings.MINIO_BUCKET,
        code_filename,
        code_zip_buffer,
        code_zip_buffer.getbuffer().nbytes
    )

    submission = await submission_service.create_submission(
        task.task_id, student.student_id, current_repository_url, github_pull_request_number, code_filename
    )

    await broker.publish(
        SubmissionEventSchema(
            submission_id=submission.submission_id,
            task_id=task.task_id,
            code_filename=code_filename,
        ), topic=SUBMISSION_TOPIC
    )

    return jsonify(SuccessResponse(message=f"Заявка на проверку создана, ее номер: {submission.submission_id}, пожалуйста ожидайте обратной связи"), status_code=status.HTTP_201_CREATED)


 # async with aiohttp.ClientSession() as session:
 #        response = await client.get_object(app_settings.MINIO_BUCKET, zip_filename, session)
 #        print(response.status)
 #        with open("data.zip", "wb") as f:
 #            content = await response.read()
 #            f.write(content)