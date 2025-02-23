from fastapi import APIRouter, status

from src.api.health.schemas import HealthResponse

router = APIRouter(tags=["monitoring"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    description="Check health of service",
    summary="Health check",
    responses={status.HTTP_200_OK: {"model": HealthResponse, "description": "The service is alive"}},
)
def health_check() -> HealthResponse:
    return HealthResponse(message="The service is alive")
