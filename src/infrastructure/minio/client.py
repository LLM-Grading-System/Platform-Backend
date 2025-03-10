from miniopy_async import Minio

from src.settings import app_settings


minio_client = Minio(
    app_settings.s3_endpoint,
    access_key=app_settings.MINIO_ACCESS_KEY,
    secret_key=app_settings.MINIO_SECRET_KEY,
    secure=False
)

def get_s3_client() -> Minio:
    return minio_client

