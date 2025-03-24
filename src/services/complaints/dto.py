from dataclasses import dataclass
from datetime import datetime


@dataclass
class ComplaintDTO:
    complaint_id: str
    task_id: str
    student_id: str
    student_request: str
    teacher_response: str
    created_at: datetime
