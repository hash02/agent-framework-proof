from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langgraph_board_runner import run_board


PRIVATE_PATTERNS = (
    re.compile(r"[A-Za-z]:\\"),
    re.compile(r"/home/"),
    re.compile(r"\b100\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
    re.compile(r"\b(?:Wukong|Kala|Maya01|MAYA|KALA|WUKONG)\b", re.IGNORECASE),
)

UNAUTHORIZED_ACTION_WORDS = ("submitted", "applied", "sent", "emailed", "contacted", "published")


def write_board(tmp_path: Path, lanes: list[dict[str, str]]) -> Path:
    board = {
        "active_board": "job_proof_chess",
        "lanes": lanes,
    }
    path = tmp_path / "career-proof-board-latest.json"
    path.write_text(json.dumps(board), encoding="utf-8")
    return path


def flatten(value) -> str:
    if isinstance(value, dict):
        return " ".join(flatten(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(flatten(v) for v in value)
    return str(value)


def test_open_gate_produces_proposed_move(tmp_path: Path) -> None:
    path = write_board(
        tmp_path,
        [
            {
                "name": "Job Tech Build Quests",
                "state": "langgraph_board_runner_proposed",
                "next_action": "Use missing role requirements as project upgrades.",
            },
            {
                "name": "PointClickCare",
                "state": "framework_gate",
                "next_action": "Parked until HASH confirms framework use.",
            },
        ],
    )

    output = run_board(path)

    assert output["hold_signal"] is False
    assert output["proposed_move"] is not None
    assert output["current_lane"] == "Job Tech Build Quests"


def test_board_reader_accepts_utf8_bom(tmp_path: Path) -> None:
    path = write_board(
        tmp_path,
        [
            {
                "name": "Job Tech Build Quests",
                "state": "langgraph_board_runner_proposed",
                "next_action": "Use missing role requirements as project upgrades.",
            }
        ],
    )
    body = path.read_text(encoding="utf-8")
    path.write_text("\ufeff" + body, encoding="utf-8")

    output = run_board(path)

    assert output["hold_signal"] is False


def test_all_blocked_gates_produce_hold_signal(tmp_path: Path) -> None:
    path = write_board(
        tmp_path,
        [
            {
                "name": "PointClickCare",
                "state": "framework_gate",
                "next_action": "Parked until HASH confirms framework use.",
            },
            {
                "name": "Kraken",
                "state": "blocked",
                "next_action": "Awaiting HASH factual answers.",
            },
        ],
    )

    output = run_board(path)

    assert output["hold_signal"] is True
    assert output["proposed_move"] is None
    assert output["open_gates"] == []


def test_output_contains_no_private_paths_ips_or_machine_names(tmp_path: Path) -> None:
    path = write_board(
        tmp_path,
        [
            {
                "name": "Job Tech Build Quests",
                "state": "langgraph_board_runner_proposed",
                "next_action": r"Use C:\secret\file and Wukong at 100.86.26.81 only in private notes.",
            }
        ],
    )

    output_text = flatten(run_board(path))

    assert not any(pattern.search(output_text) for pattern in PRIVATE_PATTERNS)


def test_output_contains_no_unauthorized_action_triggers(tmp_path: Path) -> None:
    path = write_board(
        tmp_path,
        [
            {
                "name": "Application Packets",
                "state": "voleon_precheck_next",
                "next_action": "Research only. No application or contact.",
            }
        ],
    )

    output_text = flatten(run_board(path)).lower()

    assert not any(word in output_text for word in UNAUTHORIZED_ACTION_WORDS)


def test_next_state_overrides_mixed_blocker_reason(tmp_path: Path) -> None:
    path = write_board(
        tmp_path,
        [
            {
                "name": "Application Packets",
                "state": "voleon_precheck_next",
                "next_action": "PointClickCare parked on framework gate; next unblocked lane is Voleon precheck.",
            }
        ],
    )

    output = run_board(path)

    assert output["hold_signal"] is False
    assert output["open_gates"][0]["name"] == "Application Packets"
