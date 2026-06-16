# System Card — Agent Framework Proof

## System name

Agent Framework Proof

## Status

Public proof / local portfolio package.

## Intended users

- recruiters or hiring teams reviewing agent-system skills
- developers studying governed local workflows
- risk/AI-governance readers evaluating control patterns
- Bionic Banker project viewers

## Intended use

Use this repo to inspect small, testable examples of governed agent workflow patterns:

- state machine gates
- public-safe retrieval
- tool routing
- safety evaluation
- RBAC/audit simulation
- trace-shaped observability
- queue state transitions
- MCP-style registry calls
- local API wrapping

## Out-of-scope use

Do not use this repo as:

- production agent infrastructure
- enterprise IAM
- production monitoring/alerting
- a live MCP server
- a job-application bot
- a public-profile editor
- a message sender
- a funds/payment/trading system

## Capabilities

- demonstrates deterministic local workflow control
- returns structured outputs for testable modules
- blocks or labels external-action claims
- records audit rows and trace-like events
- uses public-safe corpus data for retrieval examples
- wraps selected flows behind FastAPI endpoints
- includes container and local Kubernetes packaging proof

## Non-capabilities

- no real external side effects
- no hidden account access
- no production identity system
- no production queue or broker
- no live model calls required for core tests
- no guarantee that mocked SDK-shaped flows match a vendor runtime exactly

## Inputs

- local text prompts
- public-safe corpus entries
- local artifact paths
- role/action/resource examples
- local event examples

## Outputs

- retrieval responses with citations
- safety evaluation reports
- allow/deny audit rows
- trace-shaped JSON events
- queue transition outputs
- API responses from local endpoints

## Evaluation evidence

Packaging verification:

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

## Safety controls

- public-safe corpus only
- test checks for private-data patterns
- explicit denial of high-risk external actions
- structured role/action/resource audit rows
- fallback behavior for optional vector dependency
- boundary statements in README and docs

## Failure modes

- readers may mistake local proof modules for production deployment
- dependency versions may drift
- local mocked tools may not capture all vendor runtime behavior
- public corpus may be too small for broad retrieval claims
- sample run artifacts can become stale

## Review cadence

Review this card when:

- a new framework/module is added
- a module gains network or external side effects
- tests or dependency setup changes
- public claims about production readiness change
- run artifacts are regenerated
