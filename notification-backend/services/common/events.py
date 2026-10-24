"""Canonical financial event taxonomy."""

EVENT_CATALOG = {
    "transaction_alert": {"category": "transaction", "priority": "high"},
    "transaction_failure": {"category": "transaction", "priority": "high"},
    "upi_transaction": {"category": "transaction", "priority": "high"},
    "upi_failure": {"category": "transaction", "priority": "high"},
    "refund_processed": {"category": "transaction", "priority": "high"},
    "margin_call": {"category": "trading", "priority": "critical"},
    "price_alert": {"category": "trading", "priority": "medium"},
    "price_alert_triggered": {"category": "trading", "priority": "high"},
    "sip_reminder": {"category": "investment", "priority": "medium"},
    "sip_installment_due": {"category": "investment", "priority": "high"},
    "mutual_fund_purchase": {"category": "investment", "priority": "medium"},
    "mutual_fund_redemption": {"category": "investment", "priority": "medium"},
    "dividend_credit": {"category": "investment", "priority": "medium"},
    "corporate_action": {"category": "investment", "priority": "medium"},
    "fixed_deposit_maturity": {"category": "investment", "priority": "medium"},
    "portfolio_summary": {"category": "investment", "priority": "low"},
    "loan_disbursement": {"category": "lending", "priority": "high"},
    "loan_emi_due": {"category": "lending", "priority": "high"},
    "loan_emi_overdue": {"category": "lending", "priority": "critical"},
    "credit_card_statement": {"category": "lending", "priority": "medium"},
    "credit_card_payment_due": {"category": "lending", "priority": "high"},
    "kyc_status": {"category": "compliance", "priority": "high"},
    "regulatory_notice": {"category": "compliance", "priority": "critical"},
    "tax_statement_ready": {"category": "compliance", "priority": "medium"},
    "account_statement_ready": {"category": "account", "priority": "low"},
    "security_alert": {"category": "security", "priority": "critical"},
    "password_change": {"category": "security", "priority": "critical"},
    "login_from_new_device": {"category": "security", "priority": "critical"},
}

CRITICAL_EVENTS = {
    event_type
    for event_type, metadata in EVENT_CATALOG.items()
    if metadata["priority"] == "critical"
}


def get_event_metadata(event_type: str) -> dict:
    if event_type not in EVENT_CATALOG:
        raise ValueError(f"Unsupported financial event type: {event_type}")
    return EVENT_CATALOG[event_type]
