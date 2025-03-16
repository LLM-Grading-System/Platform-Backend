from faststream.kafka.fastapi import KafkaRouter

from src.settings import app_settings


kafka_router = KafkaRouter(
    bootstrap_servers=app_settings.KAFKA_BOOTSTRAP_SERVERS,
    schema_url="/asyncapi",
    include_in_schema=True,
)
