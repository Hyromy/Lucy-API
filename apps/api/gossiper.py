from json import dumps as json_dumps
from redis import from_url as redis_from_url
from typing import Literal

from project.config import config

MODEL = Literal[
    "guild",
    "language",
]
MODEL_VALUES = MODEL.__args__

EVENT = Literal["created", "updated", "deleted"]
EVENT_VALUES = EVENT.__args__

redis_client = redis_from_url(config.REDIS_URL)


def event_name(m: MODEL, e: EVENT, /) -> str:
    """Helper function to create a standardized event name for Redis messages."""

    def err_msg(value: str, valid_values: tuple[str]) -> str:
        return f"Invalid value: {value}. Must be one of: {', '.join(valid_values)}"

    if m not in MODEL_VALUES:
        raise ValueError(err_msg(m, MODEL_VALUES))

    if e not in EVENT_VALUES:
        raise ValueError(err_msg(e, EVENT_VALUES))

    return f"lucy.{m}.{e}"


def publish_on_redis(channel: str, payload: dict):
    """Publish a message on Redis. The payload is serialized to JSON before publishing."""

    try:
        redis_client.publish(channel, json_dumps(payload))
    except Exception as e:
        print(f"Failed to publish on Redis: {e}")


def redis_payload(*, event: str, version: int, updated_at: str, source: str) -> dict:
    """Helper function to create a standardized payload for Redis messages. This ensures that all messages have a consistent structure."""

    return {
        "event": event,
        "version": version,
        "updated_at": updated_at,
        "source": source,
    }
