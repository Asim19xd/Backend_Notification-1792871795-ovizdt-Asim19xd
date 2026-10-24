import pytest

from services.common.templates import render


def test_transaction_sms_rendering():
    result = render(
        "transaction_alert",
        "en-IN",
        "sms",
        {
            "amount": "1,250.00",
            "currency": "INR",
            "direction": "debit",
            "account_masked": "XXXX1234",
            "date": "25 Oct 2026",
        },
    )

    assert "1,250.00 INR" in result["body"]
    assert "XXXX1234" in result["body"]


def test_margin_call_email_rendering():
    result = render(
        "margin_call",
        "en-IN",
        "email",
        {"amount": "50,000", "currency": "INR", "due_date": "30 Oct 2026"},
    )

    assert result["subject"] == "Margin call due by 30 Oct 2026"


def test_unknown_template_raises():
    with pytest.raises(ValueError):
        render("unknown_event", "en-IN", "sms", {})
