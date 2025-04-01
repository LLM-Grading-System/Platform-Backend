from uuid import uuid4

from pydantic import BaseModel, Field

SUBMISSION_TOPIC = "new_submission"


class SubmissionEventSchema(BaseModel):
    submission_id: str = Field(examples=[str(uuid4())])
    task_id: str = Field(examples=[str(uuid4())])
    code_filename: str = Field(examples=["code_folder.zip"])


NEW_COMMENT_TOPIC = "new_comment"

class CreateCommentRequest(BaseModel):
    username: str = Field(examples=["octocat"])
    repo_name: str = Field(examples=["task-1"])
    pull_request_number: int = Field(examples=[1])
    comment: str = Field(examples=["Хорошая работа"])
