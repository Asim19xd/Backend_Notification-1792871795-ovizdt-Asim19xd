from __future__ import annotations

from jinja2 import Environment, BaseLoader, StrictUndefined

_templates = {
    "transaction_alert": {
        "en-IN": {
            "sms": "PaySecure: {{ amount }} {{ currency }} {{ direction }} your account {{ account_masked }} on {{ date }}.",
            "email_subject": "Transaction alert: {{ amount }} {{ currency }}",
            "email_body": "A {{ direction }} transaction of {{ amount }} {{ currency }} was processed on {{ date }}.",
            "push": "{{ amount }} {{ currency }} {{ direction }}",
            "whatsapp": "Your account had a {{ direction }} of {{ amount }} {{ currency }} on {{ date }}.",
            "in_app": "Transaction of {{ amount }} {{ currency }} {{ direction }}.",
        }
    },
    "margin_call": {
        "en-IN": {
            "sms": "URGENT: Margin call of {{ amount }} {{ currency }} due by {{ due_date }}.",
            "email_subject": "Margin call due by {{ due_date }}",
            "email_body": "You must deposit {{ amount }} {{ currency }} by {{ due_date }} to avoid liquidation.",
            "push": "Margin call due: {{ amount }} {{ currency }}",
            "whatsapp": "Margin call of {{ amount }} {{ currency }} is due by {{ due_date }}.",
            "in_app": "Margin call due by {{ due_date }}.",
        }
    },
    "sip_reminder": {
        "en-IN": {
            "sms": "Reminder: SIP of {{ amount }} {{ currency }} for {{ fund_name }} is due on {{ due_date }}.",
            "email_subject": "SIP reminder: {{ fund_name }}",
            "email_body": "Your SIP for {{ fund_name }} of {{ amount }} {{ currency }} is due on {{ due_date }}.",
            "push": "SIP due on {{ due_date }}",
            "whatsapp": "Your {{ fund_name }} SIP is due on {{ due_date }}.",
            "in_app": "SIP due on {{ due_date }}.",
        }
    },
    "price_alert": {
        "en-IN": {
            "sms": "{{ symbol}} is now {{ price }} {{ currency }}.",
            "email_subject": "Price alert: {{ symbol }}",
            "email_body": "{{ symbol }} reached {{ price }} {{ currency }}.",
            "push": "{{ symbol }}: {{ price }} {{ currency }}",
            "whatsapp": "{{ symbol }} is now {{ price }} {{ currency }}.",
            "in_app": "{{ symbol }} reached {{ price }} {{ currency }}.",
        }
    },
    "regulatory_notice": {
        "en-IN": {
            "sms": "Important regulatory notice regarding your PaySecure account.",
            "email_subject": "Important regulatory notice",
            "email_body": "Please review the regulatory notice: {{ notice_url }}",
            "push": "Important regulatory notice",
            "whatsapp": "Please review an important regulatory notice.",
            "in_app": "You have a new regulatory notice.",
        }
    },
}

_environment = Environment(loader=BaseLoader(), undefined=StrictUndefined)


def render(event_type: str, language: str, channel: str, payload: dict) -> dict:
    event_templates = _templates.get(event_type)

    if not event_templates:
        raise ValueError(f"No template configured for event: {event_type}")

    language_templates = event_templates.get(language) or event_templates["en-IN"]

    if channel not in language_templates:
        raise ValueError(f"No {channel} template for event: {event_type}")

    if channel == "email":
        return {
            "subject": _environment.from_string(language_templates["email_subject"]).render(**payload),
            "body": _environment.from_string(language_templates["email_body"]).render(**payload),
        }

    return {
        "body": _environment.from_string(language_templates[channel]).render(**payload),
    }
