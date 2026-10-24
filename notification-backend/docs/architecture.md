# Architecture

```text
Core banking / trading / lending / UPI systems
                    |
                    v
        Kafka: financial-notification-events
                    |
                    v
        Notification Orchestrator
                    |
    +---------------+----------------+
    |               |                |
    v               v                v
Preference       Compliance       Template
Service          Engine           Engine
    |               |                |
    +-------+-------+--------+-------+
            |                |
            v                v
      Frequency Cap     Channel Router
            |                |
            +--------+-------+
                     |
        +----+----+----+----+----+
        |    |    |    |    |    |
       SMS Email Push WhatsApp In-app
        |    |    |    |    |    |
        +----+----+----+----+----+
                     |
          Delivery Status Webhooks
                     |
        Kafka: notification-delivery-status
                     |
        Real-time Analytics Pipeline
                     |
     Failed events -> Retry -> DLQ
```

## Flow

1. Source systems publish canonical financial events to Kafka.
2. The orchestrator validates the event type and loads user preferences.
3. The compliance engine applies DND, quiet hours, opt-outs, and frequency caps.
4. The template engine renders channel-specific, localised content.
5. The channel router dispatches to SMS, email, push, WhatsApp, or in-app providers.
6. Provider webhooks update delivery status.
7. Failed notifications retry with exponential backoff and eventually enter the DLQ.
8. The analytics pipeline aggregates delivery metrics in real time.
