from datetime import datetime
from dataclasses import dataclass


@dataclass
class SubmissionDTO:
    submission_id: str
    task_id: str
    student_id: str
    gh_repo_url: str
    code_file_name: str

    llm_grade: str
    llm_feedback: str
    llm_report: str
    created_at: datetime
    evaluated_at: datetime
