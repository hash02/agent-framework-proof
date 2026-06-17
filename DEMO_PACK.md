# Agent Framework Proof Demo Pack

## What this demonstrates

Agent Framework Proof is a public-safe local proof stack for governed AI-agent workflows. It shows how an agent system can be designed around evidence, gates, audit rows, traces, queues, retrieval, and tool boundaries before it is connected to real external systems.

The package demonstrates seven control patterns:

1. **Gate before action** — workflows check allowed actions before producing a recommendation.
2. **Retrieve with citations** — answers cite a small public-safe corpus instead of relying on unsupported claims.
3. **Tool boundary** — local tools are registered, described, called, and tested with structured inputs and outputs.
4. **Role/audit decision** — role, action, resource, allow/deny, reason, and risk label are recorded as audit rows.
5. **Trace event shape** — decisions, tools, evaluations, and gates emit trace-like JSON events.
6. **Queue state control** — queued work can move through running, completed, blocked, or rejected states with retry metadata.
7. **Service wrapper** — retrieval and safety checks are exposed through a small local FastAPI proof service.

## Who should inspect it

- AI-governance reviewers who want to see control patterns instead of abstract claims.
- Fintech, risk, and compliance engineering teams evaluating agent workflow safety.
- Recruiters or technical reviewers looking for evidence of hands-on agent-system work.
- Developers who want a small test-backed example of agent control boundaries.

## Commands to run

Install and test in an isolated Python environment:

```bash
uv venv .venv
. .venv/bin/activate
uv pip install -r requirements.txt
python -m pytest -q
```

Run individual proof modules:

```bash
python rag_proof_retriever.py "LangGraph RAG safety eval CI"
python langchain_tool_caller.py "Find proof for LangGraph RAG Docker"
python rbac_audit_sim.py
python trace_events.py
python queue_sim.py
python openai_agents_local_proof.py
python mcp_proof_server.py
python vector_retriever.py
```

Run the local API proof:

```bash
uvicorn risk_service_api:app --reload
```

## Current verification

Latest local test command:

```bash
python -m pytest -q
```

Observed result:

```text
70 passed, 1 warning in 0.48s
```

Warning scope: dependency deprecation warning from the FastAPI/Starlette test client path. It does not indicate a failing project test.

## Evidence map

| Evidence | What to inspect | Boundary |
|---|---|---|
| `README.md` | module map, run commands, verification, boundaries | summary only |
| `docs/architecture.md` | system shape, inputs, outputs, trust boundaries | local proof architecture |
| `docs/cards/system-card.md` | intended use, non-capabilities, controls, failure modes | public proof card |
| `docs/cards/data-card.md` | corpus and retrieval-data boundary | public-safe sample data only |
| `docs/adr/0001-public-packaging-boundary.md` | why claims stay bounded | packaging decision record |
| `tests/` | regression proof for modules and boundaries | test-backed, not production certification |
| `runs/` | sample JSON outputs for selected modules | point-in-time artifacts |

## What is not claimed

This package does **not** claim:

- production agent infrastructure;
- enterprise identity and access management;
- production monitoring, alerting, or incident response;
- a live MCP server;
- a hosted vector database;
- live model integration;
- job application automation;
- public profile editing;
- messaging, publishing, trading, payment, or account authority.

External-action examples stay blocked or labeled for human review. The project is a local, deterministic proof environment for control patterns, not a production automation system.

## Suggested review path

1. Read `docs/cards/system-card.md` for intended use and non-capabilities.
2. Run `python -m pytest -q` to verify the proof suite.
3. Run `python trace_events.py` and inspect the JSON trace shape.
4. Run `python queue_sim.py` and inspect blocked external-action handling.
5. Run `python mcp_proof_server.py` and inspect local tool discovery/dispatch.
6. Read `docs/adr/0001-public-packaging-boundary.md` before quoting any public claim.
