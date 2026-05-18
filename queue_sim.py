"""Local queue simulation for governed AI workflow proofs.

This module models work items, state transitions, retries, audit rows, and
external-action gates. It is local proof only, not a production queue, broker,
workflow engine, or authorization system.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


QUEUE_STATES = {"queued", "running", "blocked", "completed", "rejected"}

ACTION_TYPES = {
    "research_role",
    "draft_packet",
    "safety_eval",
    "render_local_artifact",
    "file_form",
    "change_live_site",
    "third_party_contact",
}

EXTERNAL_ACTION_TYPES = {"file_form", "change_live_site", "third_party_contact"}

BOUNDARY = (
    "Local queue simulation for governed AI workflows; not a production "
    "queue, broker, workflow engine, or authorization system."
)


@dataclass(frozen=True)
class AuditRow:
    timestamp: str
    from_state: str
    to_state: str
    reason: str


@dataclass
class WorkItem:
    item_id: str
    state: str
    owner: str
    action_type: str
    retry_count: int
    max_retries: int
    created_at: str
    updated_at: str
    audit_rows: list[AuditRow] = field(default_factory=list)
    blocked_reason: str = ""


def validate_work_item(item: WorkItem) -> None:
    if item.state not in QUEUE_STATES:
        raise ValueError(f"Unsupported state: {item.state}")
    if item.action_type not in ACTION_TYPES:
        raise ValueError(f"Unsupported action_type: {item.action_type}")
    if item.retry_count < 0 or item.max_retries < 0:
        raise ValueError("retry_count and max_retries must be non-negative")
    if item.retry_count > item.max_retries:
        raise ValueError("retry_count must not exceed max_retries")
    if item.state in {"blocked", "rejected"} and not item.blocked_reason:
        raise ValueError("blocked and rejected items require blocked_reason")
    if item.action_type in EXTERNAL_ACTION_TYPES and item.state != "blocked":
        raise ValueError("external-action items must remain blocked")
    if item.state == "completed" and not item.audit_rows:
        raise ValueError("completed items require at least one audit row")


def transition_item(
    item: WorkItem,
    *,
    to_state: str,
    timestamp: str,
    reason: str,
    blocked_reason: str = "",
) -> WorkItem:
    if to_state not in QUEUE_STATES:
        raise ValueError(f"Unsupported state: {to_state}")
    next_blocked_reason = blocked_reason if to_state in {"blocked", "rejected"} else ""
    updated = WorkItem(
        item_id=item.item_id,
        state=to_state,
        owner=item.owner,
        action_type=item.action_type,
        retry_count=item.retry_count,
        max_retries=item.max_retries,
        created_at=item.created_at,
        updated_at=timestamp,
        audit_rows=[
            *item.audit_rows,
            AuditRow(
                timestamp=timestamp,
                from_state=item.state,
                to_state=to_state,
                reason=reason,
            ),
        ],
        blocked_reason=next_blocked_reason,
    )
    validate_work_item(updated)
    return updated


def work_items_to_dicts(items: list[WorkItem]) -> list[dict]:
    for item in items:
        validate_work_item(item)
    return [asdict(item) for item in items]


def sample_work_items() -> list[WorkItem]:
    queued = WorkItem(
        item_id="item-001",
        state="queued",
        owner="Codex",
        action_type="research_role",
        retry_count=0,
        max_retries=2,
        created_at="2026-05-18T00:00:00+00:00",
        updated_at="2026-05-18T00:00:00+00:00",
    )
    running = transition_item(
        WorkItem(
            item_id="item-002",
            state="queued",
            owner="CloudCode",
            action_type="safety_eval",
            retry_count=0,
            max_retries=2,
            created_at="2026-05-18T00:01:00+00:00",
            updated_at="2026-05-18T00:01:00+00:00",
        ),
        to_state="running",
        timestamp="2026-05-18T00:01:30+00:00",
        reason="Reviewer picked up safety evaluation task.",
    )
    completed = transition_item(
        WorkItem(
            item_id="item-003",
            state="running",
            owner="Codex",
            action_type="draft_packet",
            retry_count=1,
            max_retries=2,
            created_at="2026-05-18T00:02:00+00:00",
            updated_at="2026-05-18T00:02:30+00:00",
        ),
        to_state="completed",
        timestamp="2026-05-18T00:03:00+00:00",
        reason="Draft packet completed and saved as local artifact.",
    )
    blocked = transition_item(
        WorkItem(
            item_id="item-004",
            state="queued",
            owner="Codex",
            action_type="file_form",
            retry_count=0,
            max_retries=0,
            created_at="2026-05-18T00:04:00+00:00",
            updated_at="2026-05-18T00:04:00+00:00",
        ),
        to_state="blocked",
        timestamp="2026-05-18T00:04:05+00:00",
        reason="External form action detected.",
        blocked_reason="HASH manual review and explicit final action are required.",
    )
    rejected = transition_item(
        WorkItem(
            item_id="item-005",
            state="running",
            owner="CloudCode",
            action_type="render_local_artifact",
            retry_count=2,
            max_retries=2,
            created_at="2026-05-18T00:05:00+00:00",
            updated_at="2026-05-18T00:05:20+00:00",
        ),
        to_state="rejected",
        timestamp="2026-05-18T00:06:00+00:00",
        reason="Artifact failed local safety requirements after max retries.",
        blocked_reason="Needs redesign before another run.",
    )
    return [queued, running, completed, blocked, rejected]


def save_work_items(items: list[WorkItem], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(work_items_to_dicts(items), indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local queue simulation proof.")
    parser.add_argument(
        "--output",
        default="runs/queue-sim-output-2026-05-18.json",
        help="Where to save queue simulation output.",
    )
    args = parser.parse_args()
    output_path = Path(args.output)
    items = sample_work_items()
    save_work_items(items, output_path)
    print(json.dumps({"boundary": BOUNDARY, "output": str(output_path), "items": work_items_to_dicts(items)}, indent=2))


if __name__ == "__main__":
    main()
