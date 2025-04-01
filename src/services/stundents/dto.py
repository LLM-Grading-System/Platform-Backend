from dataclasses import dataclass
from datetime import datetime


@dataclass
class StudentDTO:
    student_id: str
    telegram_user_id: int
    telegram_username: str
    github_username: str | None
    registered_at: datetime
