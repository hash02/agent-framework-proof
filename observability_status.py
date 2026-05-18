"""Local observability proof for governed AI workflows.

This module turns deterministic runtime events into a status summary with
freshness and attention signals. It is intentionally local and lightweight:
not production monitoring, tracing, alerting, or incident response.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime


BOUNDARY = (
    "Local observability proof for governed AI workflows; "
    "not production monitoring or incident response."
)

ATTENTION_STATUSES = {"blocked", "error", "warning"}


@dataclass(frozen=True)
class RuntimeEvent:
    run_id: str
    component: str
    status: str
    timestamp: str
    duration_ms: int
    detail: str


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def classify_freshness(
    age_seconds: float,
    warn_after_seconds: int = 120,
    fail_after_seconds: int = 300,
) -> str:
    if age_seconds >= fail_after_seconds:
        return "stale"
    if age_seconds >= warn_after_seconds:
        return "warning"
    return "healthy"


def latest_event(events: list[RuntimeEvent]) -> RuntimeEvent | None:
    if not events:
        return None
    return max(events, key=lambda event: parse_timestamp(event.timestamp))


def summarize_events(events: list[RuntimeEvent], now: str | None = None) -> dict:
    current_time = parse_timestamp(now) if now else datetime.now(UTC).replace(microsecond=0)
    status_counts = Counter(event.status for event in events)
    latest = latest_event(events)
    if latest is None:
        freshness = {
            "state": "stale",
            "latest_age_seconds": None,
            "latest_event_timestamp": None,
        }
    else:
        age_seconds = (current_time - parse_timestamp(latest.timestamp)).total_seconds()
        freshness = {
            "state": classify_freshness(age_seconds),
            "latest_age_seconds": int(age_seconds),
            "latest_event_timestamp": latest.timestamp,
        }

    has_attention = bool(ATTENTION_STATUSES.intersection(status_counts))
    overall_state = (
        "attention_needed"
        if has_attention or freshness["state"] != "healthy"
        else "healthy"
    )

    return {
        "boundary": BOUNDARY,
        "generated_at": current_time.isoformat(),
        "overall_state": overall_state,
        "total_events": len(events),
        "status_counts": dict(sorted(status_counts.items())),
        "freshness": freshness,
        "latest_event": asdict(latest) if latest else None,
        "events": [asdict(event) for event in events],
    }


def sample_events() -> list[RuntimeEvent]:
    return [
        RuntimeEvent(
            run_id="run-001",
            component="langchain_tool_caller",
            status="ok",
            timestamp="2026-05-18T00:00:00+00:00",
            duration_ms=31,
            detail="retrieval tool returned cited project proof",
        ),
        RuntimeEvent(
            run_id="run-002",
            component="rbac_audit_sim",
            status="blocked",
            timestamp="2026-05-18T00:01:00+00:00",
            duration_ms=12,
            detail="high-risk submit action denied by local role policy",
        ),
        RuntimeEvent(
            run_id="run-003",
            component="agent_safety_eval",
            status="ok",
            timestamp="2026-05-18T00:02:00+00:00",
            duration_ms=44,
            detail="source artifact scan completed with zero findings",
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local observability status proof.")
    parser.add_argument(
        "--now",
        default="2026-05-18T00:02:30+00:00",
        help="Timestamp used for deterministic freshness summary",
    )
    args = parser.parse_args()
    print(json.dumps(summarize_events(sample_events(), now=args.now), indent=2))


if __name__ == "__main__":
    main()
