from services.common.models import UserPreferences
from services.worker.consumer import handle_failure, process_event, select_channels


def test_select_channels_respects_preferences():
    preferences = UserPreferences(
        user_id="u1",
        channels={"sms": False, "email": True, "push": True, "whatsapp": False, "in_app": True},
    )

    channels = select_channels("transaction_alert", preferences)

    assert "sms" not in channels
    assert "push" in channels
    assert "email" in channels


def test_process_event_renders_notifications():
    preferences = UserPreferences(user_id="u1")
    event = {
        "event_type": "transaction_alert",
        "user_id": "u1",
        "correlation_id": "corr-1",
        "payload": {
            "amount": "1,000",
            "currency": "INR",
            "direction": "debit",
            "account_masked": "XXXX1234",
            "date": "25 Oct 2026",
        },
    }

    result = process_event(event, preferences)

    assert result["notification_id"] == "corr-1"
    assert result["notifications"]


def test_retry_becomes_dead_letter():
    result = handle_failure({"event": "x"}, 5, "provider unavailable")

    assert result["action"] == "dead_letter"
    assert result["topic"] == "financial-notification-dlq"
