from observability_status import (
    RuntimeEvent,
    classify_freshness,
    summarize_events,
)


def test_classify_freshness_healthy_when_recent():
    assert classify_freshness(age_seconds=30, warn_after_seconds=60, fail_after_seconds=120) == "healthy"


def test_classify_freshness_warn_and_stale_thresholds():
    assert classify_freshness(age_seconds=75, warn_after_seconds=60, fail_after_seconds=120) == "warning"
    assert classify_freshness(age_seconds=130, warn_after_seconds=60, fail_after_seconds=120) == "stale"


def test_summarize_events_counts_statuses_and_detects_latest_event():
    events = [
        RuntimeEvent(
            run_id="run-001",
            component="retriever",
            status="ok",
            timestamp="2026-05-18T00:00:00+00:00",
            duration_ms=25,
            detail="retrieved project proof",
        ),
        RuntimeEvent(
            run_id="run-002",
            component="safety_eval",
            status="warning",
            timestamp="2026-05-18T00:01:00+00:00",
            duration_ms=40,
            detail="medium finding needs review",
        ),
        RuntimeEvent(
            run_id="run-003",
            component="rbac",
            status="blocked",
            timestamp="2026-05-18T00:02:00+00:00",
            duration_ms=10,
            detail="submit action denied",
        ),
    ]

    summary = summarize_events(events, now="2026-05-18T00:02:30+00:00")

    assert summary["boundary"] == (
        "Local observability proof for governed AI workflows; "
        "not production monitoring or incident response."
    )
    assert summary["total_events"] == 3
    assert summary["status_counts"] == {"blocked": 1, "ok": 1, "warning": 1}
    assert summary["latest_event"]["run_id"] == "run-003"
    assert summary["freshness"]["state"] == "healthy"
    assert summary["overall_state"] == "attention_needed"


def test_summarize_events_marks_stale_without_recent_events():
    events = [
        RuntimeEvent(
            run_id="run-001",
            component="retriever",
            status="ok",
            timestamp="2026-05-18T00:00:00+00:00",
            duration_ms=25,
            detail="retrieved project proof",
        )
    ]

    summary = summarize_events(events, now="2026-05-18T00:10:00+00:00")

    assert summary["freshness"]["state"] == "stale"
    assert summary["overall_state"] == "attention_needed"
