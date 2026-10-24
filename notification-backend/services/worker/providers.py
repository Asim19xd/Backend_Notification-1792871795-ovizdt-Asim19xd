from __future__ import annotations

import os
from typing import Any

import httpx


class ProviderError(Exception):
    pass


class SMSProvider:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("SMS_PROVIDER_API_KEY")

    def send(self, recipient: str, message: str) -> dict[str, Any]:
        if not self.api_key:
            raise ProviderError("SMS provider credentials missing")

        return {"provider": "sms", "message_id": "sms-" + recipient}


class EmailProvider:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("EMAIL_PROVIDER_API_KEY")

    def send(self, recipient: str, subject: str, body: str) -> dict[str, Any]:
        if not self.api_key:
            raise ProviderError("Email provider credentials missing")

        return {"provider": "email", "message_id": "email-" + recipient}


class PushProvider:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("PUSH_PROVIDER_API_KEY")

    def send(self, device_token: str, message: str) -> dict[str, Any]:
        if not self.api_key:
            raise ProviderError("Push provider credentials missing")

        return {"provider": "push", "message_id": "push-" + device_token}


class WhatsAppProvider:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("WHATSAPP_PROVIDER_API_KEY")

    def send(self, recipient: str, template: str, payload: dict) -> dict[str, Any]:
        if not self.api_key:
            raise ProviderError("WhatsApp provider credentials missing")

        return {"provider": "whatsapp", "message_id": "wa-" + recipient}


class InAppProvider:
    def send(self, user_id: str, message: str) -> dict[str, Any]:
        return {"provider": "in_app", "message_id": "inapp-" + user_id}
