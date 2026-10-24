from __future__ import annotations

import json
from datetime import datetime, timezone


class DeadLetterQueue:
    """Persists permanently failed notifications for replay and audit."""

    def __init__(self, path: str = "state/dlq.jsonl"):
        self.path = path
        import os

        os.makedirs(os.path.dirname(path), exist_ok=True)

    def write(self, event: dict, error: str, attempts: int) -> None:
        record = {
            "failed_at": datetime.now(timezone.utc).isoformat(),
            "attempts": attempts,
            "error": error,
            "event": event,
        }

        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")

    def replay(self) -> list[dict]:
        if not os.path.exists(self.path):
            return []

        records = []

        with open(self.path, encoding="utf-8") as handle:
            for line in handle:
                records.append(json.loads(line))

        return records
