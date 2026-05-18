from rbac_audit_sim import (
    ActionRequest,
    ROLE_PERMISSIONS,
    check_permission,
    run_policy_simulation,
)


def test_role_permissions_keep_submit_blocked_for_all_roles():
    for permissions in ROLE_PERMISSIONS.values():
        assert "submit_application" not in permissions


def test_researcher_can_retrieve_but_not_evaluate():
    allowed = check_permission(ActionRequest(role="researcher", action="retrieve_project_proof"))
    denied = check_permission(ActionRequest(role="researcher", action="evaluate_artifact_safety"))

    assert allowed.allowed is True
    assert allowed.reason == "role_has_permission"
    assert denied.allowed is False
    assert denied.reason == "role_missing_permission"


def test_reviewer_can_evaluate_but_not_prepare_application():
    allowed = check_permission(ActionRequest(role="reviewer", action="evaluate_artifact_safety"))
    denied = check_permission(ActionRequest(role="reviewer", action="prepare_application_packet"))

    assert allowed.allowed is True
    assert denied.allowed is False


def test_unknown_role_is_denied():
    decision = check_permission(ActionRequest(role="admin", action="retrieve_project_proof"))

    assert decision.allowed is False
    assert decision.reason == "unknown_role"


def test_policy_simulation_returns_audit_rows_with_no_private_data():
    result = run_policy_simulation()
    audit_rows = result["audit_rows"]

    assert result["boundary"] == (
        "Local RBAC and audit simulation for governed AI workflows; "
        "not enterprise IAM or production authorization."
    )
    assert len(audit_rows) >= 5
    assert any(row["allowed"] is True for row in audit_rows)
    assert any(row["allowed"] is False for row in audit_rows)
    assert all("timestamp" in row for row in audit_rows)
    assert all("private" not in str(row).lower() for row in audit_rows)
