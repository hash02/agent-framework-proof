# Agent Framework Proof

Small, recruiter-safe framework proof modules for HASH's AI finance and agent-system portfolio.

## LangGraph Board Runner

A LangGraph state machine that reads the Career Proof Chess board, checks gate status, and proposes the next safe local move within policy constraints.

Pattern:

1. Shared state
2. Gate check
3. Conditional branch
4. Structured output

Use case: governed agent workflows in regulated decision environments.

Status: personal-scale proof, not production enterprise deployment.

## Files

- `langgraph_board_runner.py`: LangGraph runner with `read_board`, `check_gates`, `propose_move`, and `blocked_state` nodes.
- `tests/test_langgraph_board_runner.py`: safety and behavior tests.

## Run

```powershell
python -m pytest tests
python langgraph_board_runner.py "path\to\career-proof-board-latest.json"
```

## Current Verification

Latest local verification:

- `python -m pytest tests`: 6 passed
- Live board run output: `runs/langgraph-board-runner-output-2026-05-18.json`

## Safety Boundaries

The runner does not apply to jobs, send messages, contact third parties, publish content, move funds, or update public profiles. It only reads local board JSON and returns a structured recommendation.

The test suite checks that output avoids private paths, IP addresses, internal machine names, and unauthorized external-action trigger words.
