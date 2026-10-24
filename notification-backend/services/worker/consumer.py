from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone

from services.common.compliance import is_channel_allowed
from services.common.events import get_event_metadata
from services.common.models import Channel, DeliveryStatusEnum, UserPreferences
from services.common.templates import render

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
EVENT_TOPIC = "financial-notification-events"
DLQ_TOPIC = "financial-notification-dlq"
MAX_ATTEMPTS = 5

CHANNEL_PRIORITY = {
    "critical": ["push", "sms", "whatsapp", "email", "in_app"],
    "high": ["push", "sms", "email", "in_app"],
    "medium": ["push", "email", "in_app"],
    "low": ["in_app", "email"],
}


def select_channels(event_type: str, preferences: UserPreferences, sent_today: int = 0):
    metadata = get_event_metadata(event_type)
    selected = []

    for channel in CHANNEL_PRIORITY[metadata["priority"]]:
        allowed, reason = is_channel_allowed(
            event_type=event_type,
            channel=channel,
            preferences=preferences,
            sent_today=sent_today,
        )

        if allowed:
            selected.append(channel)

    return selected


def process_event(event: dict, preferences: UserPreferences) -> dict:
    event_type = event["event_type"]
    metadata = get_event_metadata(event_type)
    rendered = []

    for channel in select_channels(event_type, preferences):
        try:
            content = render(
                event_type=event_type,
                language=event.get("preferred_language", "en-IN"),
                channel=channel,
                payload=event.get("payload", {}),
            )
            rendered.append(
                {
                    "channel": channel,
                    "status": DeliveryStatusEnum.QUEUED.value,
                    "content": content,
                }
            )
        except ValueError as exc:
            rendered.append(
                {
                    "channel": channel,
                    "status": DeliveryStatusEnum.DEAD_LETTER.value,
                    "error": str(exc),
                }
            )

    return {
        "notification_id": event.get("correlation_id"),
        "event_type": event_type,
        "user_id": event["user_id"],
        "priority": metadata["priority"],
        "category": metadata["category"],
        "notifications": rendered,
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }


def handle_failure(event: dict, attempt: int, error: str) -> dict:
    """Returns retry or dead-letter instruction using exponential backoff."""
    if attempt >= MAX_ATTEMPTS:
        return {
            "action": "dead_letter",
            "topic": DLQ_TOPIC,
            "attempt": attempt,
            "error": error,
        }

    delay_seconds = min(2**attempt, 300)

    return {
        "action": "retry",
        "delay_seconds": delay_seconds,
        "attempt": attempt + 1,
        "error": error,
    }


if __name__ == "__main__":
    print(f"Consumer configured for {KAFKA_BOOTSTRAP_SERVERS}, topic={EVENT_TOPIC}")
