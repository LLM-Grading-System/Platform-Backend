from abc import ABC, abstractmethod

from src.services.submissions.dto import SubmissionDTO


class SubmissionService(ABC):
    @abstractmethod
    async def create_submission(self, task_id: str, student_id: str, github_repo_url: str, code_file_name: str) -> SubmissionDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_all_submissions(self) -> list[SubmissionDTO]:
        raise NotImplementedError

    @abstractmethod
    async def evaluate_submission(self, submission_id: str, llm_grade: str, llm_feedback: str, llm_report: str) -> None:
        raise NotImplementedError
