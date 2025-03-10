from src.infrastructure.minio.client import minio_client
from src.settings import app_settings


async def create_bucket_if_not_exist():
    is_bucket_exist = await minio_client.bucket_exists(app_settings.MINIO_BUCKET)
    if not is_bucket_exist:
        await minio_client.make_bucket(app_settings.MINIO_BUCKET)
