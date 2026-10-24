from __future__ import annotations

from datetime import datetime, time, timezone
from zoneinfo import ZoneInfo

from .events import CRITICAL_EVENTS
from .models import UserPreferences


class SuppressionReason(str):
    DND = "TRAI_DND"
    QUIET_HOURS = "QUIET_HOURS"
    USER_OPT_OUT = "USER_OPT_OUT"
    CHANNEL_DISABLED = "CHANNEL_DISABLED"
    FREQUENCY_CAP = "FREQUENCY_CAP"


def is_within_quiet_hours(preferences: UserPreferences, now: datetime | None = None) -> bool:
    now = now or datetime.now(ZoneInfo(preferences.timezone))
    start = time.fromisoformat(preferences.quiet_hours_start)
    end = time.fromisoformat(preferences.quiet_hours_end)
    current = now.time()

    if start <= end:
        return start <= current < end

    return current >= start or current < end


def is_channel_allowed(
    event_type: str,
    channel: str,
    preferences: UserPreferences,
    sent_today: int,
    now: datetime | None = None,
) -> tuple[bool, str | None]:
    metadata_category = event_type.split("_")[0]
    is_critical = event_type in CRITICAL_EVENTS

    if not preferences.channels.get(channel, False):
        return False, SuppressionReason.CHANNEL_DISABLED

    if event_type in preferences.category_opt_outs or metadata_category in preferences.category_opt_outs:
        if not is_critical:
            return False, SuppressionReason.USER_OPT_OUT

    if preferences.dnd_enabled and channel in {"sms", "whatsapp"} and not is_critical:
        return False, SuppressionReason.DND

    if channel in {"sms", "whatsapp"} and not is_critical:
        if is_within_quiet_hours(preferences, now):
            return False, SuppressionReason.QUIET_HOURS

    if sent_today >= preferences.daily_limit and not is_critical:
        return False, SuppressionReason.FREQUENCY_CAP

    return True, None
