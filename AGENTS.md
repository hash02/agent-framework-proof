# AGENTS.md

## Project

Agent Framework Proof is a public, recruiter-safe collection of local agent-system proof modules. It demonstrates governed workflows, retrieval with citations, safety evaluation, RBAC/audit rows, trace-shaped observability, queue state, MCP-style tools, and a FastAPI wrapper.

## Stack

- Python 3.11+
- pytest
- LangGraph
- LangChain Core
- FastAPI / Uvicorn
- Docker and local Kubernetes manifests for packaging proof

## Commands

Create an isolated environment:

```bash
uv venv .venv
. .venv/bin/activate
uv pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest -q
```

Run selected demos:

```bash
python rag_proof_retriever.py "LangGraph RAG safety eval CI"
python langchain_tool_caller.py "Find proof for LangGraph RAG Docker"
python rbac_audit_sim.py
python observability_status.py
python trace_events.py
python queue_sim.py
python openai_agents_local_proof.py
python mcp_proof_server.py
python vector_retriever.py
```

Run the local API:

```bash
uvicorn risk_service_api:app --reload
```

Build the container:

```bash
docker build -t agent-framework-proof .
```

## Repository map

- `langgraph_board_runner.py` — governed board-runner proof with gate checks.
- `agent_safety_eval.py` — scans artifacts for private data, unauthorized action claims, and unverified framework claims.
- `rag_proof_retriever.py` — deterministic public-safe retrieval with citations.
- `langchain_tool_caller.py` — local LangChain tool registration and routing.
- `rbac_audit_sim.py` — role permissions and audit-row simulation.
- `observability_status.py` — local event freshness/status summary.
- `trace_events.py` — trace-shaped JSON events for decisions, tools, evals, and gates.
- `queue_sim.py` — local work-item state transitions and external-action gates.
- `openai_agents_local_proof.py` — Agent/Tool/runner-shaped local proof with mocked tools.
- `mcp_proof_server.py` and `mcp_tools/` — MCP-style local tool registry and calls.
- `risk_service_api.py` — FastAPI proof service.
- `data/public_career_corpus.json` — public-safe retrieval corpus.
- `tests/` — regression tests.
- `k8s/` — local Kubernetes deployment proof.
- `docs/` — packaging, architecture, cards, and ADRs.

## Agent rules

- Keep this repo public-safe and recruiter-safe.
- Do not add private paths, IP addresses, machine names, personal inbox data, API keys, tokens, or hidden operational notes.
- Do not claim production deployment, enterprise IAM, production monitoring, live MCP service, live model integration, or real external-action authority unless implemented and verified.
- Keep examples local, deterministic, and auditable.
- If a module gains external side effects, document the new trust boundary and add tests before publicizing it.
- If public positioning changes, update README, architecture, system card, and ADR together.

## Testing expectations

Before reporting done:

```bash
python -m pytest -q
```

Observed packaging baseline:

```text
70 passed, 1 warning
```

## Public boundary

This repository demonstrates workflow shapes and control patterns. It does not apply to jobs, send messages, contact third parties, publish content, update public profiles, move funds, access real accounts, or operate production infrastructure.

## Definition of done

- tests pass in an isolated environment
- docs/cards updated for behavior changes
- public claims remain bounded
- no private/internal data added
