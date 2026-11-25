# ADR-003: Transactional outbox and at-least-once dispatch

Date: 2026-11-25 | Status: Accepted design decision; implementation and feasibility validation pending

## Context
A database write followed by separate queue publish can lose accepted work. SQS and stream events can duplicate.

## Decision
Atomically persist business acceptance, quota when applicable, command and outbox. DynamoDB Streams relay to SQS Standard + DLQ; periodic sweeper repairs missing publications and expired leases. Dispatcher claims fenced command, awaits bounded runtime segment, acknowledges only durable outcome.

## Alternatives considered
Direct dual write: lost-job failure window. Step Functions as primary workflow engine: duplicates LangGraph control flow. FIFO queue: ordering/dedup window does not guarantee external exactly-once; consider only if required.

## Consequences and trade-offs
Additional outbox and reconciliation records; at-least-once delivery requires durable command IDs, conditional claims, retries and crash recovery. No unbounded worker waiting for HITL.

## Validation and revisit conditions
Crash after acceptance/before publish, duplicate publish/delivery, lost ack, DLQ redrive, stale worker, scheduler duplicate slot, reconciler repair and timeout/visibility compatibility.

## Traceability
HLD-D06; LLD section 4; NFR-006–009. See [HLD](../02-architecture/high-level-design.md), [LLD](../02-architecture/low-level-design.md), [data model](../02-architecture/data-model.md), [threat model](../04-security/threat-model.md) and [implementation backlog](../07-planning/implementation-backlog.md). No code or infrastructure is authorized by this ADR. Material deviations require an amended/superseding ADR and owner review.
