# ADR-0001: Package Agent Framework Proof as a governed-workflow portfolio asset

## Status

Accepted

## Date

2026-06-16

## Context

The repository contains many small proof modules showing modern agent-system patterns: LangGraph state machines, LangChain tool calls, MCP-style tools, retrieval, safety evaluation, RBAC, trace events, queues, FastAPI, Docker, and Kubernetes manifests.

The risk is overclaiming. These are local proofs, not production infrastructure.

## Decision

Package the repository as a public, recruiter-safe governed-workflow proof.

The public framing is:

```text
public-safe input -> policy/retrieval/role/gate check -> structured output -> audit/trace/boundary
```

The public boundary is:

```text
local proof only; no external action authority; no production deployment claim
```

## Alternatives considered

### Package as an enterprise agent platform

Rejected. The modules demonstrate architecture literacy, but they are not a deployed enterprise platform with production IAM, monitoring, incident response, or security operations.

### Package as a generic AI-agent demo

Rejected. Generic agent framing misses the strongest value: governed workflows, safety checks, audit rows, and clear trust boundaries.

### Hide framework names

Rejected. Framework names such as LangGraph, LangChain Core, FastAPI, Docker, Kubernetes, and MCP-style tooling are useful proof points when tied to local/tested boundaries.

## Consequences

Positive:

- clearer recruiter-facing value
- safer public positioning
- reusable Bionic project-card language
- better docs for future agent-assisted edits

Risks:

- readers may over-read the repo as production-ready
- dependencies can drift
- generated run artifacts can become stale
- local proof modules may not match vendor runtimes exactly

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
