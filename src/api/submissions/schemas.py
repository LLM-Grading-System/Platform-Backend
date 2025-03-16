from uuid import uuid4

from pydantic import Field

from src.api.base_schema import BaseSchema
from src.services.submissions import SubmissionDTO


class SubmissionResponse(BaseSchema):
    submission_id: str = Field(examples=[str(uuid4())])
    task_id: str = Field(examples=[str(uuid4())])
    student_id: str = Field(examples=[str(uuid4())])
    gh_repo_url: str
    code_file_name: str

    llm_grade: str
    llm_feedback: str
    llm_report: str
    created_at: int
    evaluated_at: int | None

    @staticmethod
    def from_dto(submission: SubmissionDTO) -> "SubmissionResponse":
        return SubmissionResponse(
            submission_id=submission.submission_id,
            task_id=submission.task_id,
            student_id=submission.student_id,
            gh_repo_url=submission.gh_repo_url,
            code_file_name=submission.code_file_name,
            llm_grade=submission.llm_grade,
            llm_feedback=submission.llm_feedback,
            llm_report=submission.llm_report,
            created_at=int(submission.created_at.timestamp()),
            evaluated_at=int(submission.evaluated_at.timestamp()) if submission.evaluated_at else None,
        )


class EvaluationSubmissionRequest(BaseSchema):
    llm_grade: str
    llm_feedback: str
    llm_report: str
