"""LangGraph runner for Career Proof Chess board state.

This is a small proof module: read board JSON, classify gates, and propose the
next safe local move without applying to jobs, contacting anyone, or publishing.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Literal, TypedDict

from langgraph.graph import END, START, StateGraph


BLOCKED_WORDS = (
    "blocked",
    "parked",
    "gate",
    "gated",
    "awaiting",
    "unconfirmed",
    "requires",
    "hash framework",
    "sponsorship",
)

OPEN_WORDS = (
    "authorized",
    "proposed",
    "next",
    "route",
    "ready",
    "active",
)

PRIVATE_PATTERNS = (
    re.compile(r"[A-Za-z]:\\"),
    re.compile(r"/home/"),
    re.compile(r"\b100\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
    re.compile(r"\b(?:Wukong|Kala|Maya01|MAYA|KALA|WUKONG)\b", re.IGNORECASE),
    re.compile(r"\b(?:private key|wallet secret|api key|token)\b", re.IGNORECASE),
)

UNAUTHORIZED_ACTION_WORDS = (
    "applied",
    "submitted",
    "sent",
    "emailed",
    "contacted",
    "published",
)


class Gate(TypedDict):
    name: str
    state: str
    reason: str


class BoardRunnerState(TypedDict, total=False):
    board_path: str
    board: dict[str, Any]
    current_lane: str
    open_gates: list[Gate]
    blocked_gates: list[Gate]
    proposed_move: str | None
    hold_signal: bool
    errors: list[str]


def _safe_text(value: Any) -> str:
    text = str(value)
    for pattern in PRIVATE_PATTERNS:
        text = pattern.sub("[redacted]", text)
    return text


def _contains_private_text(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_private_text(v) for v in value.values())
    if isinstance(value, list):
        return any(_contains_private_text(v) for v in value)
    text = str(value)
    return any(pattern.search(text) for pattern in PRIVATE_PATTERNS)


def _is_blocked(lane: dict[str, Any]) -> bool:
    state_text = str(lane.get("state", "")).lower()
    reason_text = str(lane.get("next_action", "")).lower()
    if any(word in state_text for word in ("next", "route", "authorized", "proposed", "ready")):
        return False
    return any(word in f"{state_text} {reason_text}" for word in BLOCKED_WORDS)


def _is_open(lane: dict[str, Any]) -> bool:
    state_text = str(lane.get("state", "")).lower()
    if any(word in state_text for word in ("next", "route", "authorized", "proposed", "ready")):
        return True
    text = f"{state_text} {lane.get('next_action', '')}".lower()
    return any(word in text for word in OPEN_WORDS) and not _is_blocked(lane)


def read_board(state: BoardRunnerState) -> BoardRunnerState:
    board_path = state.get("board_path")
    if not board_path:
        return {"errors": ["board_path missing"], "hold_signal": True}

    path = Path(board_path)
    board = json.loads(path.read_text(encoding="utf-8-sig"))
    active_board = _safe_text(board.get("active_board", "unknown"))
    return {
        "board": board,
        "current_lane": active_board,
        "errors": [],
    }


def check_gates(state: BoardRunnerState) -> BoardRunnerState:
    board = state.get("board") or {}
    lanes = board.get("lanes") or []
    open_gates: list[Gate] = []
    blocked_gates: list[Gate] = []

    for lane in lanes:
        name = _safe_text(lane.get("name", "unnamed"))
        gate = {
            "name": name,
            "state": _safe_text(lane.get("state", "unknown")),
            "reason": _safe_text(lane.get("next_action", "")),
        }
        if _is_blocked(lane):
            blocked_gates.append(gate)
        elif _is_open(lane):
            open_gates.append(gate)

    return {
        "open_gates": open_gates,
        "blocked_gates": blocked_gates,
        "hold_signal": len(open_gates) == 0,
    }


def route_after_gates(state: BoardRunnerState) -> Literal["propose_move", "blocked_state"]:
    return "propose_move" if state.get("open_gates") else "blocked_state"


def propose_move(state: BoardRunnerState) -> BoardRunnerState:
    open_gates = state.get("open_gates") or []
    chosen = choose_gate(open_gates)
    proposed_move = proposal_for_gate(chosen)
    return {
        "current_lane": chosen["name"],
        "proposed_move": proposed_move,
        "hold_signal": False,
    }


def blocked_state(state: BoardRunnerState) -> BoardRunnerState:
    return {
        "proposed_move": None,
        "hold_signal": True,
    }


def choose_gate(open_gates: list[Gate]) -> Gate:
    priority = (
        "Job Tech Build Quests",
        "Application Packets",
        "Global 100k Scanner",
        "Portfolio Proof Console",
    )
    for wanted in priority:
        for gate in open_gates:
            if gate["name"] == wanted:
                return gate
    return open_gates[0]


def proposal_for_gate(gate: Gate) -> str:
    text = f"{gate['name']} {gate['state']} {gate['reason']}".lower()
    if "langgraph" in text:
        return "Build the local LangGraph Board Runner proof, run tests, and keep resume claims unchanged until proof exists."
    if "voleon" in text:
        return "Run a research-only Voleon precheck from the canonical posting before drafting any packet."
    if "proof console" in text:
        return "Prepare a local proof-console improvement proposal without changing the live website."
    return f"Work the {gate['name']} lane locally and keep all external actions blocked."


def build_graph():
    graph = StateGraph(BoardRunnerState)
    graph.add_node("read_board", read_board)
    graph.add_node("check_gates", check_gates)
    graph.add_node("propose_move", propose_move)
    graph.add_node("blocked_state", blocked_state)
    graph.add_edge(START, "read_board")
    graph.add_edge("read_board", "check_gates")
    graph.add_conditional_edges(
        "check_gates",
        route_after_gates,
        {"propose_move": "propose_move", "blocked_state": "blocked_state"},
    )
    graph.add_edge("propose_move", END)
    graph.add_edge("blocked_state", END)
    return graph.compile()


def run_board(board_path: str | Path) -> dict[str, Any]:
    graph = build_graph()
    result = graph.invoke({"board_path": str(board_path)})
    output = {
        "current_lane": result.get("current_lane", "unknown"),
        "open_gates": result.get("open_gates", []),
        "blocked_gates": result.get("blocked_gates", []),
        "proposed_move": result.get("proposed_move"),
        "hold_signal": bool(result.get("hold_signal", False)),
    }
    if _contains_private_text(output):
        raise ValueError("Output failed private-data safety check.")
    proposed = str(output.get("proposed_move") or "").lower()
    if any(word in proposed for word in UNAUTHORIZED_ACTION_WORDS):
        raise ValueError("Output contains an unauthorized external-action trigger.")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the LangGraph Career Proof Chess board runner.")
    parser.add_argument("board", help="Path to career-proof-board-latest.json")
    args = parser.parse_args()
    print(json.dumps(run_board(args.board), indent=2))


if __name__ == "__main__":
    main()
