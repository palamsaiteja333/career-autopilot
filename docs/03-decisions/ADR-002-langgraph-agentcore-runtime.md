# ADR-002: Explicit LangGraph workflows on AgentCore Runtime

Date: 2026-11-25 | Status: Accepted design decision; implementation and feasibility validation pending

## Context
Two known workflows need branching, typed state, interrupts and resume across independent invocations.

## Decision
Use explicit versioned StateGraph workflows, deterministic registry/dispatch, 11 search and 14 application nodes, AgentCore Runtime in preferred Canada Central. No supervisor LLM. Persist stable graph thread separately from temporary runtime session.

## Alternatives considered
LLM supervisor: flexible but unnecessary cost/authority surface. Strands or custom loop: valid alternatives but explicit graph and interrupt learning prioritized. Lambda-only graph worker: fallback if runtime compatibility/cost fails. Fargate: persistent container alternative.

## Consequences and trade-offs
Transparent routing and durable HITL; requires versioned graph compatibility, bounded segment timeouts, fenced checkpoint writes and runtime invocation tests. A new agent registers contracts rather than rewriting existing workflows.

## Validation and revisit conditions
Invoke/resume across separate sessions, interrupt replay, stale worker and checkpoint fencing, p95 targets, 300s segment bound, region/privacy and cost. No silent hosting/region fallback.

## Traceability
HLD-D02; LLD sections 1,3,4; NFR-002,003,007,019. See [HLD](../02-architecture/high-level-design.md), [LLD](../02-architecture/low-level-design.md), [data model](../02-architecture/data-model.md), [threat model](../04-security/threat-model.md) and [implementation backlog](../07-planning/implementation-backlog.md). No code or infrastructure is authorized by this ADR. Material deviations require an amended/superseding ADR and owner review.
