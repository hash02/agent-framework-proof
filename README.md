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
- `agent_safety_eval.py`: policy eval harness that scans artifacts for private data, unauthorized action claims, and unverified framework claims.
- `rag_proof_retriever.py`: deterministic public-safe retrieval proof with chunking, scoring, and citations.
- `risk_service_api.py`: local FastAPI service wrapping retrieval and safety-eval flows.
- `data/public_career_corpus.json`: small public-only corpus for recruiter-safe retrieval tests.
- `tests/test_langgraph_board_runner.py`: safety and behavior tests.
- `tests/test_agent_safety_eval.py`: eval harness regression tests.
- `tests/test_rag_proof_retriever.py`: retrieval and citation tests.
- `tests/test_risk_service_api.py`: API contract tests.

## Run

```powershell
python -m pytest tests
python langgraph_board_runner.py "path\to\career-proof-board-latest.json"
python agent_safety_eval.py "path\to\packet-or-board-artifact.md" --allow-framework LangGraph
python rag_proof_retriever.py "LangGraph RAG safety eval CI"
uvicorn risk_service_api:app --reload
```

## FastAPI Risk Service

The local API proof wraps the retrieval and safety-eval modules behind service endpoints:

- `GET /health`: service status and version.
- `POST /retrieve`: public-safe retrieval over the project corpus with citations and claim-boundary text.
- `POST /eval`: artifact safety eval for local files and verified framework names.

Job-market signal: backend API design, Pydantic request/response contracts, testable service boundaries, and a path toward Docker packaging.

## Current Verification

Latest local verification:

- `python -m pytest tests`: 26 passed
- Live board run output: `runs/langgraph-board-runner-output-2026-05-18.json`
- Live RAG proof output: `runs/rag-proof-retriever-output-2026-05-18.json`

## Safety Boundaries

The runner does not apply to jobs, send messages, contact third parties, publish content, move funds, or update public profiles. It only reads local board JSON and returns a structured recommendation.

The test suite checks that output avoids private paths, IP addresses, internal machine names, and unauthorized external-action trigger words.

The eval harness is intentionally conservative. High-severity findings fail the run. Medium-severity findings are review prompts, usually for boundary statements or unverified framework names.

The RAG proof is intentionally small and public-safe. It demonstrates retrieval mechanics and citations; it is not a production RAG claim.
