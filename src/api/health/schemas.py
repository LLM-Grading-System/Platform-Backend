from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health response."""

    message: str = Field(examples=["The service is alive"])
