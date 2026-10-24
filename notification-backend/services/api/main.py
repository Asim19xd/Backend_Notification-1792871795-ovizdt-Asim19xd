from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.common.events import get_event_metadata
from services.common.models import (
    Channel,
    DeliveryStatus,
    NotificationEvent,
    UserPreferences,
)

app = FastAPI(title="Financial Notification Platform", version="1.0.0")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
EVENT_TOPIC = "financial-notification-events"
STATUS_TOPIC = "notification-delivery-status"

# In production, replace this in-memory store with PostgreSQL and Redis.
preferences_store: dict[str, UserPreferences] = {}
notifications_store: dict[str, dict] = {}
analytics_counters: dict[str, int] = {
    "events_received": 0,
    "notifications_queued": 0,
    "delivered": 0,
    "failed": 0,
    "suppressed": 0,
}


class EventResponse(BaseModel):
    event_id: str
    status: str
    topic: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/v1/events", response_model=EventResponse, status_code=202)
def publish_event(event: NotificationEvent):
    try:
        metadata = get_event_metadata(event.event_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    event_id = str(uuid4())
    notifications_store[event_id] = {
        "event_id": event_id,
        "event_type": event.event_type,
        "user_id": event.user_id,
        "status": "queued",
        "category": metadata["category"],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    analytics_counters["events_received"] += 1
    analytics_counters["notifications_queued"] += 1

    return EventResponse(
        event_id=event_id,
        status="queued",
        topic=EVENT_TOPIC,
    )


@app.post("/v1/preferences")
def save_preferences(preferences: UserPreferences):
    preferences_store[preferences.user_id] = preferences
    return {"user_id": preferences.user_id, "status": "saved"}


@app.get("/v1/preferences/{user_id}")
def get_preferences(user_id: str):
    preferences = preferences_store.get(user_id)

    if not preferences:
        raise HTTPException(status_code=404, detail="Preferences not found")

    return preferences


@app.get("/v1/notifications/{notification_id}")
def get_notification(notification_id: str):
    notification = notifications_store.get(notification_id)

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    return notification


@app.post("/v1/delivery-status", status_code=202)
def delivery_status(status: DeliveryStatus):
    notification = notifications_store.get(status.notification_id)

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification["status"] = status.status.value
    notification["channel"] = status.channel.value
    notification["updated_at"] = datetime.now(timezone.utc).isoformat()

    if status.status == DeliveryStatusEnum.DELIVERED:
        analytics_counters["delivered"] += 1
    elif status.status == DeliveryStatusEnum.FAILED:
        analytics_counters["failed"] += 1

    return {"notification_id": status.notification_id, "status": "accepted"}


@app.get("/v1/analytics/summary")
def analytics_summary():
    return analytics_counters
