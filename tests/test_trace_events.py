import json
from pathlib import Path

import pytest

from trace_events import (
    ALLOWED_EVENT_TYPES,
    ALLOWED_GATE_STATUSES,
    TraceEvent,
    events_to_dicts,
    make_event,
    sample_trace_events,
    save_trace_events,
    validate_trace_event,
)


def test_sample_trace_events_have_required_shape():
    events = sample_trace_events()
    rows = events_to_dicts(events)

    assert len(rows) == 5
    for row in rows:
        assert row["trace_id"]
        assert row["span_id"]
        assert row["event_type"] in ALLOWED_EVENT_TYPES
        assert row["timestamp"]
        assert row["agent"]
        assert row["input_summary"]
        assert row["output_summary"]
        assert isinstance(row["evidence_refs"], list)
        assert row["gate_status"] in ALLOWED_GATE_STATUSES
        assert isinstance(row["duration_ms"], int)
        assert row["duration_ms"] >= 0


def test_parent_span_links_create_trace_tree():
    events = sample_trace_events()
    span_ids = {event.span_id for event in events}

    child_events = [event for event in events if event.parent_span_id is not None]
    assert child_events
    assert all(event.parent_span_id in span_ids for event in child_events)


def test_gate_blocked_requires_reason():
    event = TraceEvent(
        trace_id="trace-test",
        span_id="span-test",
        parent_span_id=None,
        event_type="gate_blocked",
        timestamp="2026-05-18T00:00:00+00:00",
        agent="Codex",
        input_summary="Check blocked action.",
        output_summary="Blocked.",
        evidence_refs=[],
        gate_status="blocked",
        duration_ms=1,
        reason="",
    )

    with pytest.raises(ValueError, match="gate_blocked events require"):
        validate_trace_event(event)


def test_make_event_rejects_invalid_event_type():
    with pytest.raises(ValueError, match="Unsupported event_type"):
        make_event(
            trace_id="trace-test",
            event_type="unknown",
            agent="Codex",
            input_summary="input",
            output_summary="output",
        )


def test_trace_events_do_not_include_private_paths_or_hosts():
    serialized = json.dumps(events_to_dicts(sample_trace_events()))

    forbidden_fragments = [
        "win_drive_marker",
        "home_user_marker",
        "100.",
        "credential_phrase",
        "wallet_credential_phrase",
        "employer_customer_records_phrase",
    ]
    for fragment in forbidden_fragments:
        assert fragment not in serialized


def test_save_trace_events_writes_json_array(tmp_path):
    output = tmp_path / "trace-events.json"
    save_trace_events(sample_trace_events(), output)

    rows = json.loads(output.read_text(encoding="utf-8"))
    assert isinstance(rows, list)
    assert rows[0]["event_type"] == "decision"
