"""Trace-like JSON events for governed AI workflow proofs.

This module is local proof only. It produces OpenTelemetry-style event shapes
for agent decisions, tool calls, evals, and gate outcomes without claiming
production tracing, monitoring, or incident response.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


ALLOWED_EVENT_TYPES = {
    "decision",
    "tool_call",
    "eval_result",
    "gate_check",
    "gate_blocked",
}

ALLOWED_GATE_STATUSES = {"open", "blocked", "not_applicable"}

BOUNDARY = (
    "Local trace-event proof for governed AI workflows; not production "
    "OpenTelemetry, monitoring, alerting, or incident response."
)


@dataclass(frozen=True)
class TraceEvent:
    trace_id: str
    span_id: str
    parent_span_id: str | None
    event_type: str
    timestamp: str
    agent: str
    input_summary: str
    output_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    gate_status: str = "not_applicable"
    duration_ms: int = 0
    reason: str = ""


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12]}"


def validate_trace_event(event: TraceEvent) -> None:
    if event.event_type not in ALLOWED_EVENT_TYPES:
        raise ValueError(f"Unsupported event_type: {event.event_type}")
    if event.gate_status not in ALLOWED_GATE_STATUSES:
        raise ValueError(f"Unsupported gate_status: {event.gate_status}")
    if event.duration_ms < 0:
        raise ValueError("duration_ms must be non-negative")
    if event.event_type == "gate_blocked" and not event.reason:
        raise ValueError("gate_blocked events require a non-empty reason")


def make_event(
    *,
    trace_id: str,
    event_type: str,
    agent: str,
    input_summary: str,
    output_summary: str,
    parent_span_id: str | None = None,
    evidence_refs: list[str] | None = None,
    gate_status: str = "not_applicable",
    duration_ms: int = 0,
    reason: str = "",
    timestamp: str | None = None,
) -> TraceEvent:
    event = TraceEvent(
        trace_id=trace_id,
        span_id=new_id("span"),
        parent_span_id=parent_span_id,
        event_type=event_type,
        timestamp=timestamp or utc_now(),
        agent=agent,
        input_summary=input_summary,
        output_summary=output_summary,
        evidence_refs=evidence_refs or [],
        gate_status=gate_status,
        duration_ms=duration_ms,
        reason=reason,
    )
    validate_trace_event(event)
    return event


def events_to_dicts(events: list[TraceEvent]) -> list[dict]:
    for event in events:
        validate_trace_event(event)
    return [asdict(event) for event in events]


def sample_trace_events() -> list[TraceEvent]:
    trace_id = "trace-career-proof-001"
    decision = make_event(
        trace_id=trace_id,
        event_type="decision",
        agent="Codex",
        input_summary="Review board state and choose next safe local build.",
        output_summary="Selected compact answer set for review-ready compliance packet.",
        evidence_refs=["50-career/career-agent/career-proof-board-latest.json"],
        duration_ms=18,
        timestamp="2026-05-18T00:00:00+00:00",
    )
    tool_call = make_event(
        trace_id=trace_id,
        parent_span_id=decision.span_id,
        event_type="tool_call",
        agent="Codex",
        input_summary="Read packet and checklist artifacts.",
        output_summary="Found role-specific questions and credential boundaries.",
        evidence_refs=[
            "50-career/career-agent/hiive-final-submit-checklist-2026-05-18.md"
        ],
        duration_ms=42,
        timestamp="2026-05-18T00:00:02+00:00",
    )
    eval_result = make_event(
        trace_id=trace_id,
        parent_span_id=tool_call.span_id,
        event_type="eval_result",
        agent="Codex",
        input_summary="Scan compact answer artifact for unsafe claims.",
        output_summary="No high or medium safety findings.",
        evidence_refs=["agent-framework-proof/agent_safety_eval.py"],
        duration_ms=51,
        timestamp="2026-05-18T00:00:05+00:00",
    )
    gate_check = make_event(
        trace_id=trace_id,
        parent_span_id=eval_result.span_id,
        event_type="gate_check",
        agent="Codex",
        input_summary="Check whether external action is requested.",
        output_summary="Only local artifact creation is allowed.",
        gate_status="open",
        duration_ms=7,
        timestamp="2026-05-18T00:00:07+00:00",
    )
    gate_blocked = make_event(
        trace_id=trace_id,
        parent_span_id=gate_check.span_id,
        event_type="gate_blocked",
        agent="Codex",
        input_summary="Evaluate form filing request boundary.",
        output_summary="External form action remains blocked for human review.",
        gate_status="blocked",
        duration_ms=5,
        reason="Job forms require human review and explicit final action.",
        timestamp="2026-05-18T00:00:08+00:00",
    )
    return [decision, tool_call, eval_result, gate_check, gate_blocked]


def save_trace_events(events: list[TraceEvent], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(events_to_dicts(events), indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local trace-event proof.")
    parser.add_argument(
        "--output",
        default="runs/trace-events-output-2026-05-18.json",
        help="Where to save the trace-event JSON array.",
    )
    args = parser.parse_args()
    output_path = Path(args.output)
    events = sample_trace_events()
    save_trace_events(events, output_path)
    print(json.dumps({"boundary": BOUNDARY, "output": str(output_path), "events": events_to_dicts(events)}, indent=2))


if __name__ == "__main__":
    main()
