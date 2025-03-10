import io
import secrets
import zipfile
from typing import Annotated

from fastapi import APIRouter, File, UploadFile, Depends, status
from starlette.responses import JSONResponse
from miniopy_async import Minio

from src.api.utils import jsonify
from src.api.general_schemas import SuccessResponse
from src.infrastructure.minio.client import get_s3_client
from src.settings import app_settings

router = APIRouter(prefix="/submissions", tags=["submissions"])


@router.post(
    "",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    description="Submission successfully created",
    summary="Create submissions",
)
async def create_submission(
    client: Annotated[Minio, Depends(get_s3_client)],
    autotests_log: UploadFile = File(...),
    linters_log: UploadFile = File(...),
    code: UploadFile = File(...),

) -> JSONResponse:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file in [autotests_log, linters_log, code]:
            zip_file.writestr(file.filename, await file.read())
    zip_buffer.seek(0)

    zip_filename = f"{secrets.token_hex(32)}.zip"
    print(zip_filename)
    await client.put_object(
        app_settings.MINIO_BUCKET,
        zip_filename,
        zip_buffer,
        zip_buffer.getbuffer().nbytes
    )
    # create name, give github url, author, create task to review
    return jsonify(SuccessResponse(message="The submissions is successfully got"), status_code=status.HTTP_201_CREATED)
