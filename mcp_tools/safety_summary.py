"""Public-safe safety summary tool for the local MCP-style server."""

from __future__ import annotations


BLOCKED_MARKERS = {
    "external_action_token",
    "profile_change_token",
    "live_site_change_token",
}


def safety_summary(text: str) -> dict:
    lowered = text.lower()
    matched = sorted(marker for marker in BLOCKED_MARKERS if marker in lowered)
    if matched:
        return {
            "status": "blocked",
            "findings": [
                {
                    "rule": "external_action_boundary",
                    "severity": "high",
                    "marker": marker,
                }
                for marker in matched
            ],
            "boundary_note": "External actions require human review and final action.",
        }
    return {
        "status": "pass",
        "findings": [],
        "boundary_note": "Local proof artifact only.",
    }
