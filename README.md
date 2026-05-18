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
- `langchain_tool_caller.py`: LangChain tool-calling proof over local retrieval and safety-eval tools.
- `rbac_audit_sim.py`: local RBAC and audit simulation for governed AI workflow roles.
- `observability_status.py`: local runtime event summary with freshness and attention states.
- `trace_events.py`: OpenTelemetry-style JSON trace event proof for agent decisions, tool calls, evals, and gate outcomes.
- `queue_sim.py`: local queue simulation for governed workflow states, retries, audit rows, and external-action gates.
- `openai_agents_local_proof.py`: OpenAI Agents SDK-shaped local proof with Agent, Tool, and runner abstractions over mocked tools.
- `mcp_proof_server.py`: local MCP-style tool server proof with registry introspection and structured tool calls.
- `mcp_tools/`: public-safe proof lookup and safety summary tool handlers.
- `vector_retriever.py`: optional Chroma vector retrieval mode with deterministic fallback over the public-safe corpus.
- `risk_service_api.py`: local FastAPI service wrapping retrieval and safety-eval flows.
- `Dockerfile`: container package for the local FastAPI proof service.
- `k8s/`: local Kubernetes deployment, service, probes, and kustomization for the FastAPI proof service.
- `data/public_career_corpus.json`: small public-only corpus for recruiter-safe retrieval tests.
- `tests/test_langgraph_board_runner.py`: safety and behavior tests.
- `tests/test_agent_safety_eval.py`: eval harness regression tests.
- `tests/test_rag_proof_retriever.py`: retrieval and citation tests.
- `tests/test_langchain_tool_caller.py`: local LangChain tool registration, routing, and invocation tests.
- `tests/test_rbac_audit_sim.py`: role permission and audit-row tests.
- `tests/test_observability_status.py`: runtime event and freshness summary tests.
- `tests/test_trace_events.py`: trace-event structure, parent links, blocked-gate reason, and private-data guard tests.
- `tests/test_queue_sim.py`: queue state, retry, audit-row, external-action gate, and private-data guard tests.
- `tests/test_openai_agents_local_proof.py`: local Agent, Tool, runner, blocked-path, and serialization tests.
- `tests/test_mcp_proof_server.py`: MCP-style tool discovery, dispatch, error response, and serialization tests.
- `tests/test_vector_retriever.py`: deterministic retrieval, optional Chroma fallback, citation, and serialization tests.
- `tests/test_risk_service_api.py`: API contract tests.
- `tests/test_kubernetes_manifests.py`: manifest checks for local Kubernetes deployment proof.

## Run

```powershell
python -m pytest tests
python langgraph_board_runner.py "path\to\career-proof-board-latest.json"
python agent_safety_eval.py "path\to\packet-or-board-artifact.md" --allow-framework LangGraph
python rag_proof_retriever.py "LangGraph RAG safety eval CI"
python langchain_tool_caller.py "Find proof for LangGraph RAG Docker"
python rbac_audit_sim.py
python observability_status.py
python trace_events.py
python queue_sim.py
python openai_agents_local_proof.py
python mcp_proof_server.py
python vector_retriever.py
uvicorn risk_service_api:app --reload
docker build -t agent-framework-proof .
docker run --rm -p 8000:8000 agent-framework-proof
kubectl apply -k k8s
```

## FastAPI Risk Service

The local API proof wraps the retrieval and safety-eval modules behind service endpoints:

- `GET /health`: service status and version.
- `POST /retrieve`: public-safe retrieval over the project corpus with citations and claim-boundary text.
- `POST /eval`: artifact safety eval for local files and verified framework names.

Job-market signal: backend API design, Pydantic request/response contracts, testable service boundaries, and a path toward Docker packaging.

## LangChain Tool Calling

The `langchain_tool_caller.py` module registers two LangChain tools:

- `retrieve_project_proof`: calls the local RAG proof retriever.
- `evaluate_artifact_safety`: calls the local artifact safety eval harness.

The workflow uses deterministic routing instead of a paid model call. This keeps the proof free and testable while still showing the core tool-calling shape: tool registration, argument passing, invocation, result capture, and a clear safety boundary.

Job-market signal: hands-on LangChain tool abstraction, local tool orchestration, and auditable agent-system boundaries.

## RBAC And Audit Simulation

The `rbac_audit_sim.py` module models three workflow roles:

- `researcher`: can read board state and retrieve project proof.
- `reviewer`: can read board state and evaluate artifact safety.
- `applicant`: can read board state and prepare application packets.

High-risk actions such as `submit_application` and `edit_public_profile` are denied for every role in the local simulation.

Each decision creates an audit row with timestamp, role, action, resource, allow/deny result, reason, and risk label.

Job-market signal: role-scoped access, auditability, authorization boundaries, and regulated-workflow thinking. This is a local simulation only, not enterprise IAM or production authorization.

## Observability Status Proof

The `observability_status.py` module turns local runtime events into a status summary.

Each event includes:

- run id
- component
- status
- timestamp
- duration
- detail

The summary computes:

- status counts
- latest event
- freshness state
- overall state

Job-market signal: runtime visibility, freshness checks, and attention-state reporting for governed agent workflows. This is local proof only, not production monitoring, tracing, alerting, or incident response.

## Trace Events

The `trace_events.py` module produces OpenTelemetry-style JSON events for governed agent workflows. Each event includes a trace id, span id, parent span id, event type, timestamp, agent, public-safe input/output summaries, evidence references, gate status, duration, and blocked-action reason where needed. The sample output is saved at `runs/trace-events-output-2026-05-18.json`.

Job-market signal: trace-shaped observability for agent decisions, tool calls, eval results, and gate outcomes. This is local proof only, not production OpenTelemetry, monitoring, alerting, or incident response.

## Queue Simulation

The `queue_sim.py` module models local work items moving through `queued`, `running`, `blocked`, `completed`, and `rejected` states. Each work item includes an owner, action type, retry count, max retries, timestamps, audit rows, and blocked reason where required. External-action work items remain blocked behind HASH manual review. The sample output is saved at `runs/queue-sim-output-2026-05-18.json`.

Job-market signal: async-style workflow proof with state transitions, retries, auditability, and governed external-action gates. This is local proof only, not a production queue, broker, workflow engine, or authorization system.

## OpenAI Agents SDK Proof

The `openai_agents_local_proof.py` module shows an OpenAI Agents SDK-shaped workflow using local Agent, Tool, and runner abstractions. It calls mocked proof-lookup and safety-check tools, returns a structured result with `tools_called`, `safety_status`, `evidence_refs`, and a claim boundary, and saves sample output at `runs/openai-agents-local-proof-output-2026-05-18.json`.

Job-market signal: hands-on agent SDK workflow shape, tool metadata, local tool routing, blocked-path behavior, and public-safe JSON output. This is local proof only, not a production OpenAI Agents SDK deployment or live model integration.

## MCP Tool Server Proof

The `mcp_proof_server.py` module shows a local MCP-style tool boundary with registry introspection and structured calls. It exposes two tools, `proof_lookup` and `safety_summary`, returns `tool`, `params`, `result`, `boundary`, and `error` fields for every call, and saves sample output at `runs/mcp-proof-server-output-2026-05-18.json`. Tests live in `tests/test_mcp_proof_server.py`.

Job-market signal: MCP-style tool discovery, input schema metadata, local dispatch, safe error handling, and public-safe tool boundaries. This is local proof only, not a live MCP server, network service, credentialed integration, or production deployment.

## Vector Retriever

The `vector_retriever.py` module adds retrieval with citations using two modes: deterministic local retrieval over the public-safe corpus, and an optional Chroma mode when `chromadb` is available. If Chroma is missing or fails at runtime, the result falls back to `deterministic_fallback` so CI remains reliable. The sample output is saved at `runs/vector-retriever-output-2026-05-18.json`.

Job-market signal: retrieval with citations, optional vector database mode, graceful dependency fallback, and public-safe result boundaries. This is local proof only, not production RAG, hosted vector search, or a live data integration.

## Docker Package

The Docker package runs the FastAPI proof service on port `8000`.

Job-market signal: packaging a tested Python API service into a repeatable container image. The CI workflow builds the image on every push.

## Kubernetes Mini Deploy

The `k8s/` folder contains a local Kubernetes deployment and service for the FastAPI proof service.

It includes:

- one deployment for the local `agent-framework-proof:local` image
- a ClusterIP service on port `8000`
- readiness and liveness probes against `/health`
- CPU and memory requests and limits
- a kustomization entry point

Job-market signal: local orchestration literacy, health probes, resource boundaries, and service wiring. This is local proof only, not a production EKS or cloud-operations claim.

## Current Verification

Latest local verification:

- `python -m pytest tests`: test suite passes
- GitHub Actions: tests, source safety eval, and Docker build
- Live board run output: `runs/langgraph-board-runner-output-2026-05-18.json`
- Live RAG proof output: `runs/rag-proof-retriever-output-2026-05-18.json`

## Safety Boundaries

The runner does not apply to jobs, send messages, contact third parties, publish content, move funds, or update public profiles. It only reads local board JSON and returns a structured recommendation.

The test suite checks that output avoids private paths, IP addresses, internal machine names, and unauthorized external-action trigger words.

The eval harness is intentionally conservative. High-severity findings fail the run. Medium-severity findings are review prompts, usually for boundary statements or unverified framework names.

The RAG proof is intentionally small and public-safe. It demonstrates retrieval mechanics and citations; it is not a production RAG claim.
