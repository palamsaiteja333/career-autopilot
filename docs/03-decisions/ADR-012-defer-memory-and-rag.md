# ADR-012: Defer AgentCore Memory and dedicated RAG

Date: 2026-11-25 | Status: Accepted design decision; implementation and feasibility validation pending

## Context
MVP has a verified structured candidate profile, immutable documents and graph checkpoints; no concrete semantic retrieval/long-term conversation requirement.

## Decision
Use DynamoDB verified facts and scoped reusable answers, S3 document refs and LangGraph checkpoints. Defer AgentCore Memory, vector DB and RAG until a concrete measured use case.

## Alternatives considered
Add managed memory or vector retrieval immediately: educational value but more storage, permissions, cost, deletion and correctness complexity.

## Consequences and trade-offs
Simpler source of truth and retention. Future agent modules may require retrieval; introduce through a new reviewed ADR and evals, never treat unverified memory as candidate truth.

## Validation and revisit conditions
Profile retrieval and HITL reuse work without RAG; review retrieval need and privacy before enabling future memory.

## Traceability
HLD-D05; FR-002,010,018. See [HLD](../02-architecture/high-level-design.md), [LLD](../02-architecture/low-level-design.md), [data model](../02-architecture/data-model.md), [threat model](../04-security/threat-model.md) and [implementation backlog](../07-planning/implementation-backlog.md). No code or infrastructure is authorized by this ADR. Material deviations require an amended/superseding ADR and owner review.
