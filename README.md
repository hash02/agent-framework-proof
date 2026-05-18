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
