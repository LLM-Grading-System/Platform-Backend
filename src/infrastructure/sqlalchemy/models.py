from datetime import datetime
from uuid import UUID, uuid4

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
    gh_username: str = Field(nullable=False)
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


class Attempt(SQLModel, table=True):
    __tablename__ = "attempts"

    attempt_id: UUID = Field(default_factory=uuid4, primary_key=True)
    task_id: UUID = Field(foreign_key="tasks.task_id")
    student_id: UUID = Field(foreign_key="students.student_id")
    gh_repo_url: str = Field(nullable=False)

    llm_grade: float = Field(nullable=False)
    llm_feedback: str = Field(nullable=False)
    teacher_grade: float = Field(nullable=False)
    teacher_feedback: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    evaluated_at: datetime | None = Field(default=None)
