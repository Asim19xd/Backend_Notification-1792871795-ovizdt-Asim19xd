from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone


class AnalyticsPipeline:
    """Maintains real-time notification delivery metrics."""

    def __init__(self):
        self.counters = defaultdict(int)
        self.channel_status = defaultdict(lambda: defaultdict(int))
        self.event_type_status = defaultdict(lambda: defaultdict(int))

    def record_event(self, event_type: str) -> None:
        self.counters["events_received"] += 1
        self.event_type_status[event_type]["received"] += 1

    def record_dispatch(self, channel: str, event_type: str, status: str) -> None:
        self.counters["notifications_dispatched"] += 1
        self.channel_status[channel][status] += 1
        self.event_type_status[event_type][status] += 1

        if status == "delivered":
            self.counters["delivered"] += 1
        elif status == "failed":
            self.counters["failed"] += 1
        elif status == "suppressed":
            self.counters["suppressed"] += 1

    def summary(self) -> dict:
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "counters": dict(self.counters),
            "by_channel": {
                channel: dict(statuses)
                for channel, statuses in self.channel_status.items()
            },
            "by_event_type": {
                event_type: dict(statuses)
                for event_type, statuses in self.event_type_status.items()
            },
        }
