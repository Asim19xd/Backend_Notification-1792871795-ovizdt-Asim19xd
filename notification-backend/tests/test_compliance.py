from datetime import datetime
from zoneinfo import ZoneInfo

from services.common.compliance import is_channel_allowed, SuppressionReason
from services.common.models import UserPreferences


def test_dnd_blocks_sms():
    preferences = UserPreferences(user_id="u1", dnd_enabled=True)
    allowed, reason = is_channel_allowed(
        "transaction_alert", "sms", preferences, 0
    )

    assert allowed is False
    assert reason == SuppressionReason.DND


def test_quiet_hours_block_non_critical_sms():
    preferences = UserPreferences(user_id="u1")
    now = datetime(2026, 10, 25, 22, 0, tzinfo=ZoneInfo("Asia/Kolkata"))

    allowed, reason = is_channel_allowed(
        "sip_reminder", "sms", preferences, 0, now
    )

    assert allowed is False
    assert reason == SuppressionReason.QUIET_HOURS


def test_critical_event_overrides_quiet_hours():
    preferences = UserPreferences(user_id="u1")
    now = datetime(2026, 10, 25, 22, 0, tzinfo=ZoneInfo("Asia/Kolkata"))

    allowed, reason = is_channel_allowed(
        "margin_call", "sms", preferences, 0, now
    )

    assert allowed is True
    assert reason is None


def test_frequency_cap_blocks_non_critical():
    preferences = UserPreferences(user_id="u1", daily_limit=2)

    allowed, reason = is_channel_allowed(
        "portfolio_summary", "push", preferences, 2
    )

    assert allowed is False
    assert reason == SuppressionReason.FREQUENCY_CAP
