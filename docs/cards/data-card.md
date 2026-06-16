# Data Card — Agent Framework Proof Public Corpus and Run Artifacts

## Data sources

This repo uses local, public-safe examples only:

- `data/public_career_corpus.json`
- sample board/artifact inputs used by tests
- generated sample outputs under `runs/`
- local role/action/resource examples in the simulation modules

## Purpose

The data exists to demonstrate retrieval, safety evaluation, auditability, trace events, and workflow boundaries without exposing private operational data.

## Intended use

- local tests
- recruiter-safe portfolio demonstrations
- Bionic Banker project packaging
- examples of governed agent workflow documentation

## Unsafe use

Do not treat this data as:

- a production knowledge base
- a private career vault
- a full audit log
- a complete governance dataset
- a live agent memory system
- a regulated evidence archive

## Schema / shape

The data includes small JSON/text records for:

- public-safe proof corpus entries
- cited retrieval snippets
- safety-eval outputs
- audit rows
- trace events
- queue state transitions
- API request/response examples

## Privacy boundary

The repo must not include:

- private paths
- private IPs or hostnames
- personal inbox/message data
- account credentials
- API keys or tokens
- private job/application details
- unpublished operating notes
- real external-action records

## Quality checks

Packaging verification:

```bash
python -m pytest -q
```

Observed result:

```text
70 passed, 1 warning
```

The test suite includes checks for public-safe outputs, blocked actions, serialization, citation behavior, and manifest/service contracts.

## Known limitations

- corpus is intentionally small
- generated run artifacts can become stale
- local examples are not production telemetry
- deterministic retrieval proves mechanics, not broad semantic quality
- optional vector mode is not required for CI or public claims

## Update policy

Update this card when:

- new corpora are added
- sample artifacts are regenerated
- schema changes
- private/public boundaries change
- retrieval or eval behavior changes
