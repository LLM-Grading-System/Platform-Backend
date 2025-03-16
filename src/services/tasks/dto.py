from dataclasses import dataclass


@dataclass
class TaskDTO:
    task_id: str
    name: str
    system_instructions: str
    ideas: str
    github_repo_url: str
    level: str
    tags: list[str]
    is_draft: bool
