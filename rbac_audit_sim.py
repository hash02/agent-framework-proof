"""Local RBAC and audit simulation for governed AI workflows.

This is intentionally small and deterministic. It demonstrates role-scoped
actions and audit rows for recruiter-facing proof without claiming enterprise
IAM, production authorization, or cloud security ownership.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime


BOUNDARY = (
    "Local RBAC and audit simulation for governed AI workflows; "
    "not enterprise IAM or production authorization."
)

ROLE_PERMISSIONS: dict[str, set[str]] = {
    "researcher": {"retrieve_project_proof", "read_board_state"},
    "reviewer": {"evaluate_artifact_safety", "read_board_state"},
    "applicant": {"prepare_application_packet", "read_board_state"},
}

ACTION_RISK: dict[str, str] = {
    "retrieve_project_proof": "low",
    "read_board_state": "low",
    "evaluate_artifact_safety": "medium",
    "prepare_application_packet": "medium",
    "submit_application": "high",
    "edit_public_profile": "high",
}


@dataclass(frozen=True)
class ActionRequest:
    role: str
    action: str
    resource: str = "career-proof-workflow"


@dataclass(frozen=True)
class PolicyDecision:
    role: str
    action: str
    resource: str
    allowed: bool
    reason: str
    risk: str


@dataclass(frozen=True)
class AuditRow:
    timestamp: str
    role: str
    action: str
    resource: str
    allowed: bool
    reason: str
    risk: str


def check_permission(request: ActionRequest) -> PolicyDecision:
    permissions = ROLE_PERMISSIONS.get(request.role)
    risk = ACTION_RISK.get(request.action, "unknown")
    if permissions is None:
        return PolicyDecision(
            role=request.role,
            action=request.action,
            resource=request.resource,
            allowed=False,
            reason="unknown_role",
            risk=risk,
        )
    if request.action not in permissions:
        return PolicyDecision(
            role=request.role,
            action=request.action,
            resource=request.resource,
            allowed=False,
            reason="role_missing_permission",
            risk=risk,
        )
    return PolicyDecision(
        role=request.role,
        action=request.action,
        resource=request.resource,
        allowed=True,
        reason="role_has_permission",
        risk=risk,
    )


def audit_decision(decision: PolicyDecision, timestamp: str | None = None) -> AuditRow:
    return AuditRow(
        timestamp=timestamp or datetime.now(UTC).replace(microsecond=0).isoformat(),
        role=decision.role,
        action=decision.action,
        resource=decision.resource,
        allowed=decision.allowed,
        reason=decision.reason,
        risk=decision.risk,
    )


def sample_requests() -> list[ActionRequest]:
    return [
        ActionRequest(role="researcher", action="retrieve_project_proof"),
        ActionRequest(role="researcher", action="evaluate_artifact_safety"),
        ActionRequest(role="reviewer", action="evaluate_artifact_safety"),
        ActionRequest(role="reviewer", action="prepare_application_packet"),
        ActionRequest(role="applicant", action="prepare_application_packet"),
        ActionRequest(role="applicant", action="submit_application"),
        ActionRequest(role="applicant", action="edit_public_profile"),
    ]


def run_policy_simulation(requests: list[ActionRequest] | None = None) -> dict:
    selected_requests = requests or sample_requests()
    fixed_timestamp = "2026-05-18T00:00:00+00:00"
    rows = [
        audit_decision(check_permission(request), timestamp=fixed_timestamp)
        for request in selected_requests
    ]
    allowed_count = sum(1 for row in rows if row.allowed)
    denied_count = len(rows) - allowed_count
    return {
        "boundary": BOUNDARY,
        "roles": {role: sorted(permissions) for role, permissions in ROLE_PERMISSIONS.items()},
        "summary": {
            "total": len(rows),
            "allowed": allowed_count,
            "denied": denied_count,
        },
        "audit_rows": [asdict(row) for row in rows],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local RBAC and audit simulation.")
    parser.parse_args()
    print(json.dumps(run_policy_simulation(), indent=2))


if __name__ == "__main__":
    main()
