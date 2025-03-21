from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from src.api.health.schemas import HealthResponse
from src.api.utils import jsonify

router = APIRouter(tags=["monitoring"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    description="Check health of service",
    summary="Health check",
)
def health_check() -> JSONResponse:
    return jsonify(HealthResponse(message="The service is alive"))
