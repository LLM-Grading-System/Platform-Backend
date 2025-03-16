from uuid import uuid4

from pydantic import BaseModel, Field

SUBMISSION_TOPIC = "new_submission"


class SubmissionEventSchema(BaseModel):
    submission_id: str = Field(examples=[str(uuid4())])
