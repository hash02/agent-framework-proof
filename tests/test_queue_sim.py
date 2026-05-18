import json

import pytest

from queue_sim import (
    ACTION_TYPES,
    QUEUE_STATES,
    WorkItem,
    sample_work_items,
    transition_item,
    validate_work_item,
    work_items_to_dicts,
)


def test_sample_work_items_cover_required_states_and_fields():
    rows = work_items_to_dicts(sample_work_items())
    states = {row["state"] for row in rows}

    assert {"queued", "running", "blocked", "completed", "rejected"}.issubset(states)
    for row in rows:
        assert row["item_id"]
        assert row["state"] in QUEUE_STATES
        assert row["owner"]
        assert row["action_type"] in ACTION_TYPES
        assert isinstance(row["retry_count"], int)
        assert isinstance(row["max_retries"], int)
        assert row["retry_count"] <= row["max_retries"]
        assert row["created_at"]
        assert row["updated_at"]
        assert isinstance(row["audit_rows"], list)
        assert "blocked_reason" in row


def test_blocked_and_rejected_items_require_reason():
    for state in ("blocked", "rejected"):
        item = WorkItem(
            item_id=f"item-{state}",
            state=state,
            owner="Codex",
            action_type="draft_packet",
            retry_count=0,
            max_retries=1,
            created_at="2026-05-18T00:00:00+00:00",
            updated_at="2026-05-18T00:00:00+00:00",
            blocked_reason="",
        )

        with pytest.raises(ValueError, match="blocked and rejected"):
            validate_work_item(item)


def test_retry_count_cannot_exceed_max_retries():
    item = WorkItem(
        item_id="item-retry",
        state="queued",
        owner="Codex",
        action_type="research_role",
        retry_count=3,
        max_retries=2,
        created_at="2026-05-18T00:00:00+00:00",
        updated_at="2026-05-18T00:00:00+00:00",
    )

    with pytest.raises(ValueError, match="retry_count"):
        validate_work_item(item)


def test_state_transition_appends_audit_row():
    item = WorkItem(
        item_id="item-transition",
        state="queued",
        owner="Codex",
        action_type="safety_eval",
        retry_count=0,
        max_retries=2,
        created_at="2026-05-18T00:00:00+00:00",
        updated_at="2026-05-18T00:00:00+00:00",
    )

    updated = transition_item(
        item,
        to_state="running",
        timestamp="2026-05-18T00:00:10+00:00",
        reason="Work started.",
    )

    assert updated.state == "running"
    assert len(updated.audit_rows) == 1
    assert updated.audit_rows[0].from_state == "queued"
    assert updated.audit_rows[0].to_state == "running"


def test_external_action_items_stay_blocked():
    item = WorkItem(
        item_id="item-external",
        state="queued",
        owner="Codex",
        action_type="file_form",
        retry_count=0,
        max_retries=0,
        created_at="2026-05-18T00:00:00+00:00",
        updated_at="2026-05-18T00:00:00+00:00",
    )

    with pytest.raises(ValueError, match="external-action"):
        transition_item(
            item,
            to_state="running",
            timestamp="2026-05-18T00:00:10+00:00",
            reason="Should not run.",
        )


def test_completed_items_require_audit_row():
    item = WorkItem(
        item_id="item-completed",
        state="completed",
        owner="Codex",
        action_type="draft_packet",
        retry_count=0,
        max_retries=1,
        created_at="2026-05-18T00:00:00+00:00",
        updated_at="2026-05-18T00:00:00+00:00",
    )

    with pytest.raises(ValueError, match="completed items"):
        validate_work_item(item)


def test_queue_items_do_not_include_private_paths_or_hosts():
    serialized = json.dumps(work_items_to_dicts(sample_work_items()))
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
