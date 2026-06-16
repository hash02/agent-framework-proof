# Agent Framework Proof Architecture

## Purpose

Agent Framework Proof packages a set of small, local modules that show how governed AI workflows can be made auditable before they are connected to real external systems.

The repo is a proof environment, not a production agent platform.

## Core pattern

```text
public-safe input
   ↓
retrieval / policy / role / gate check
   ↓
structured local output
   ↓
audit row / trace event / safety boundary
```

## Main modules

| Module | Role |
|---|---|
| `langgraph_board_runner.py` | state machine with gate checks and safe next-move output |
| `agent_safety_eval.py` | artifact safety evaluation for private data and unauthorized claims |
| `rag_proof_retriever.py` | deterministic retrieval over a public-safe corpus |
| `langchain_tool_caller.py` | local tool registration and routing with LangChain Core |
| `rbac_audit_sim.py` | role-scoped permissions and audit rows |
| `observability_status.py` | event freshness and local runtime status summary |
| `trace_events.py` | trace-shaped JSON event records |
| `queue_sim.py` | work-item state transitions, retry counts, and external-action gates |
| `openai_agents_local_proof.py` | SDK-shaped Agent/Tool/runner workflow with mocked tools |
| `mcp_proof_server.py` | local MCP-style registry and structured tool calls |
| `vector_retriever.py` | deterministic retrieval with optional Chroma fallback |
| `risk_service_api.py` | FastAPI wrapper around retrieval and safety-eval flows |

## Inputs

- public-safe corpus records
- local board/artifact files
- local prompts/queries for retrieval
- local role/action/resource requests
- local runtime event examples

## Outputs

- cited retrieval results
- safety evaluation summaries
- role allow/deny audit rows
- trace-shaped JSON records
- queue transition records
- API responses from local FastAPI endpoints
- sample run artifacts under `runs/`

## Trust boundaries

The system does **not**:

- submit applications
- send messages
- contact third parties
- publish content
- move money
- update public profiles
- access private accounts
- operate production infrastructure
- provide enterprise IAM, monitoring, queueing, RAG, or MCP guarantees

External-action examples stay blocked behind human review.

## Verification

Packaging baseline:

```bash
uv venv .venv
. .venv/bin/activate
uv pip install -r requirements.txt
python -m pytest -q
```

Observed result:

```text
70 passed, 1 warning
```

## Known limitations

- The repo is intentionally local and small.
- Some modules mimic production shapes but do not replace production services.
- The retrieval corpus is public-safe and limited.
- Optional vector mode falls back to deterministic retrieval.
- API service is a local proof, not authenticated production infrastructure.
