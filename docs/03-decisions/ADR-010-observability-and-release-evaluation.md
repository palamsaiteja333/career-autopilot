# ADR-010: Privacy-safe observability and evidence-based release

Date: 2026-11-25 | Status: Accepted design decision; implementation and feasibility validation pending

## Context
Need traceable model/tool/node behavior, cost and quality without leaking sensitive candidate data.

## Decision
ADOT/OpenTelemetry, CloudWatch, X-Ray and AgentCore telemetry; correlation/run/thread IDs, linked asynchronous spans, low-cardinality metrics, redacted logs. Versioned golden datasets and deterministic safety assertions; PR smoke suite and full release suite. 99.5% API SLO and approved quality targets are unmeasured.

## Alternatives considered
Raw prompt/response capture: unacceptable privacy risk. Extra paid tracing stack: defer. LLM judge only: cannot prove policy, provenance or actual side effects.

## Consequences and trade-offs
Instrumentation and redaction require explicit tests; 30-day logs/traces, no span open across days of human wait. Safety blockers cannot be waived by average model accuracy.

## Validation and revisit conditions
Trace linkage, canary PII scan, alarm simulation, quality goldens, load/restore drills, cost attribution and release evidence.

## Traceability
HLD-D08; NFR-015–020; evaluation plan v1.0. See [HLD](../02-architecture/high-level-design.md), [LLD](../02-architecture/low-level-design.md), [data model](../02-architecture/data-model.md), [threat model](../04-security/threat-model.md) and [implementation backlog](../07-planning/implementation-backlog.md). No code or infrastructure is authorized by this ADR. Material deviations require an amended/superseding ADR and owner review.
