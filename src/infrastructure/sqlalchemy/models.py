from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: UUID = Field(default_factory=uuid4, primary_key=True)
    login: str = Field(nullable=False, unique=True)
    salt: str = Field(nullable=False)
    hashed_password: str = Field(nullable=False)
    role: str = Field(default="student")
    created_at: datetime = Field(default_factory=datetime.now)

    sessions: list["Session"] = Relationship(back_populates="user")


class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    session_id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.user_id")
    expired_at: datetime = Field(nullable=False)
    user_agent: str = Field(nullable=False)

    user: User = Relationship(back_populates="sessions")


class Student(SQLModel, table=True):
    __tablename__ = "students"

    student_id: UUID = Field(default_factory=uuid4, primary_key=True)
    tg_user_id: int = Field(nullable=False, unique=True)
    tg_username: str = Field(nullable=False)
    gh_username: str | None = Field(nullable=True, default=None, unique=True)
    registered_at: datetime = Field(default_factory=datetime.now)


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    task_id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False)
    system_instructions: str = Field(nullable=False)
    ideas: str = Field(nullable=False)
    gh_repo_url: str = Field(nullable=False, unique=True)
    level: str = Field(nullable=False)
    tags: str = Field(nullable=False)
    is_draft: bool = Field(nullable=False)


class Submission(SQLModel, table=True):
    __tablename__ = "submissions"

    submission_id: UUID = Field(default_factory=uuid4, primary_key=True)
    task_id: UUID = Field(foreign_key="tasks.task_id")
    student_id: UUID = Field(foreign_key="students.student_id")
    gh_repo_url: str = Field(nullable=False)
    gh_pull_request_number: int = Field(nullable=False)
    code_file_name: str = Field(nullable=False)

    llm_grade: str = Field(default="")
    llm_feedback: str = Field(default="")
    llm_report: str = Field(default="")
    evaluated_at: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)


class Complaint(SQLModel, table=True):
    __tablename__ = "complaints"

    complaint_id: UUID = Field(default_factory=uuid4, primary_key=True)
    task_id: UUID = Field(foreign_key="tasks.task_id")
    student_id: UUID = Field(foreign_key="students.student_id")
    student_request: str = Field(nullable=False)
    teacher_response: str = Field(nullable=False, default="")
    created_at: datetime = Field(default_factory=datetime.now)
