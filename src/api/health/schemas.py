from pydantic import Field

from src.api.base_schema import BaseSchema


class HealthResponse(BaseSchema):
    """Health response."""

    message: str = Field(examples=["The service is alive"])
