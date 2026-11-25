# ADR-005: Bedrock model adapter, bounded inference and evaluation

Date: 2026-11-25 | Status: Accepted design decision; implementation and feasibility validation pending

## Context
Job relevance and ambiguous form mapping require semantic reasoning; quota, approvals and sorting do not.

## Decision
Use Bedrock through typed model adapter, evidence-grounded structured outputs and Guardrails; deterministic policies for hard constraints. Initial batches up to 10 jobs/15 questions; one schema correction, shared token/tool/time/cost budgets. Model choice deferred to evaluation and regional availability.

## Alternatives considered
Model per posting/question: high call count. Entire workflow as one prompt: poor observability and authorization. Fixed premium model: potentially unnecessary spend. Local inference: alternative outside chosen cloud baseline.

## Consequences and trade-offs
More validation and golden datasets; no invented qualifications. Budget USD 50/month, variable targets USD 0.25 search/USD 0.50 application; alerts are not hard billing caps. Defer exact model and prices.

## Validation and revisit conditions
EV-001–010, regional processing, measured quality/latency/cost and no prohibited side effects; reduce optional work rather than weaken safety.

## Traceability
NFR-017,018; agent workflows v1.0; evaluation plan v1.0. See [HLD](../02-architecture/high-level-design.md), [LLD](../02-architecture/low-level-design.md), [data model](../02-architecture/data-model.md), [threat model](../04-security/threat-model.md) and [implementation backlog](../07-planning/implementation-backlog.md). No code or infrastructure is authorized by this ADR. Material deviations require an amended/superseding ADR and owner review.
