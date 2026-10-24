from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class Channel(str, Enum):
    SMS = "sms"
    EMAIL = "email"
    PUSH = "push"
    WHATSAPP = "whatsapp"
    IN_APP = "in_app"


class DeliveryStatusEnum(str, Enum):
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"
    SUPPRESSED = "suppressed"
    DEAD_LETTER = "dead_letter"


class NotificationEvent(BaseModel):
    event_type: str
    user_id: str
    payload: dict[str, Any] = Field(default_factory=dict)
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    preferred_language: str = "en-IN"


class UserPreferences(BaseModel):
    user_id: str
    channels: dict[str, bool] = Field(
        default_factory=lambda: {
            "sms": True,
            "email": True,
            "push": True,
            "whatsapp": False,
            "in_app": True,
        }
    )
    category_opt_outs: list[str] = Field(default_factory=list)
    quiet_hours_start: str = "21:00"
    quiet_hours_end: str = "08:00"
    timezone: str = "Asia/Kolkata"
    daily_limit: int = 10
    dnd_enabled: bool = False


class NotificationRequest(BaseModel):
    notification_id: str
    event_type: str
    user_id: str
    channel: Channel
    template_id: str
    language: str
    payload: dict[str, Any]
    correlation_id: str


class DeliveryStatus(BaseModel):
    notification_id: str
    channel: Channel
    status: DeliveryStatusEnum
    provider_message_id: str | None = None
    error_code: str | None = None
