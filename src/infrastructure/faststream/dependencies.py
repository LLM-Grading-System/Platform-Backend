from faststream.kafka import KafkaBroker
from src.infrastructure.faststream.kafka_router import kafka_router


def get_broker() -> KafkaBroker:
    return kafka_router.broker
