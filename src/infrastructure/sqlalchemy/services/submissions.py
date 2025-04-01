from uuid import UUID
from datetime import datetime

from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.sqlalchemy.models import Submission
from src.services.exceptions import NotFoundError
from src.services.submissions import SubmissionService, SubmissionDTO


class SqlAlchemySubmissionService(SubmissionService):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_submissions(self) -> list[SubmissionDTO]:
        query = select(Submission)
        result = await self.session.execute(query)
        submissions = result.scalars().all()
        return [self.from_model_to_dto(submission) for submission in submissions]

    async def create_submission(self, task_id: str, student_id: str, github_repo_url: str, github_pull_request_number: int, code_file_name: str) -> SubmissionDTO:
        submission = Submission(
            task_id=UUID(task_id),
            student_id=UUID(student_id),
            gh_repo_url=github_repo_url,
            gh_pull_request_number=github_pull_request_number,
            code_file_name=code_file_name,
        )
        self.session.add(submission)
        await self.session.commit()
        await self.session.refresh(submission)
        return self.from_model_to_dto(submission)

    async def evaluate_submission(self, submission_id: str, llm_grade: str, llm_feedback: str, llm_report: str) -> SubmissionDTO:
        submission = await self._get_submission_by_submission_id(submission_id)
        submission.llm_grade = llm_grade
        submission.llm_feedback = llm_feedback
        submission.llm_report = llm_report
        submission.evaluated_at = datetime.now()
        await self.session.commit()
        await self.session.refresh(submission)
        return self.from_model_to_dto(submission)

    async def _get_submission_by_submission_id(self, submission_id: str) -> Submission:
        query = select(Submission).where(Submission.submission_id == UUID(submission_id))
        result = await self.session.execute(query)
        submission = result.scalar_one_or_none()
        if not submission:
            raise NotFoundError(message="Сабмита с таким идентификатором не существует")
        return submission

    @staticmethod
    def from_model_to_dto(model: Submission) -> SubmissionDTO:
        return SubmissionDTO(
            submission_id=str(model.submission_id),
            task_id=str(model.task_id),
            student_id=str(model.student_id),
            gh_repo_url=model.gh_repo_url,
            gh_pull_request_number=model.gh_pull_request_number,
            code_file_name=model.code_file_name,
            llm_grade=model.llm_grade,
            llm_feedback=model.llm_feedback,
            llm_report=model.llm_report,
            created_at=model.created_at,
            evaluated_at=model.evaluated_at,
        )
