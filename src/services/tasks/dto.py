from dataclasses import dataclass
from datetime import datetime


@dataclass
class TaskDTO:
    task_id: str
    name: str
    description: str
    github_repo_url: str
    level: str
    tags: list[str]
    is_draft: bool


@dataclass
class CriteriaDTO:
    criteria_id: str
    task_id: str
    description: str
    weight: float
    created_at: datetime
