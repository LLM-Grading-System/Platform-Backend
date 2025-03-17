from uuid import uuid4

from pydantic import BaseModel, Field

SUBMISSION_TOPIC = "new_submission"


class SubmissionEventSchema(BaseModel):
    submission_id: str = Field(examples=[str(uuid4())])
    task_id: str = Field(examples=[str(uuid4())])
    code_filename: str = Field(examples=["code_folder.zip"])
