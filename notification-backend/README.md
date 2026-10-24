# Financial Event Notification Backend

Event-driven, multi-channel notification platform for financial events such as transaction alerts, margin calls, SIP reminders, price alerts, and regulatory notices.

## Channels

- SMS
- Email
- Push notification
- WhatsApp
- In-app inbox

## Features

- Processes 25+ financial event types
- Kafka-based event ingestion
- User preference management
- TRAI DND compliance and quiet hours
- Per-user and per-category frequency capping
- Template engine with personalisation and localisation
- Delivery tracking and status webhooks
- Dead-letter queue with exponential-backoff retry
- Real-time analytics pipeline
- OpenAPI contract
- Docker Compose local environment
- GitHub Actions CI
- GitHub transfer instructions for Day 15

## Local development

```bash
docker compose up -d
uvicorn services.api.main:app --reload --port 8000
python -m services.worker.consumer
pytest -q
```

## API

```http
POST /v1/preferences
GET  /v1/preferences/{user_id}
POST /v1/events
GET  /v1/notifications/{notification_id}
POST /v1/delivery-status
GET  /v1/analytics/summary
```

See `api/openapi.yaml`.
