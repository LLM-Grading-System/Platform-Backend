from faststream.kafka.fastapi import KafkaRouter

from src.settings import app_settings


kafka_router = KafkaRouter(
    bootstrap_servers=app_settings.KAFKA_BOOTSTRAP_SERVERS,
)
# https://faststream.airt.ai/latest/getting-started/publishing/broker/