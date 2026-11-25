# ADR-004: DynamoDB and S3 with separated logical domains

Date: 2026-11-25 | Status: Accepted design decision; implementation and feasibility validation pending

## Context
Key-based access patterns, durable workflows, private documents and privileged approval data; low workload and budget.

## Decision
Five logical tables: domain, execution, authorization, checkpoints, deletion. Composite keys and sparse GSIs. DynamoDB on-demand and private versioned S3. Strong base-table/conditional transactions for quotas and approval, not GSIs. Library-managed checkpoint schema pending validation; separate authoritative ledger.

## Alternatives considered
Single-table design: fewer resources but mixed permissions/lifecycles. PostgreSQL: relational constraints and flexible queries but greater operational/cost requirements. In-memory checkpoints: unsuitable for restart recovery.

## Consequences and trade-offs
More explicit access patterns and consistency protocols; no foreign keys, eventual index lag, bounded items and transactions, S3 offload and independent deletion journal. Actual checkpoint table count may differ.

## Validation and revisit conditions
Access-pattern and transaction tests, owner isolation, concurrent quota, checkpoint library and writer fencing, S3 versions, GSI lag, deletion and restore.

## Traceability
HLD-D03; Data model v1.0; NFR-007,009,010,014. See [HLD](../02-architecture/high-level-design.md), [LLD](../02-architecture/low-level-design.md), [data model](../02-architecture/data-model.md), [threat model](../04-security/threat-model.md) and [implementation backlog](../07-planning/implementation-backlog.md). No code or infrastructure is authorized by this ADR. Material deviations require an amended/superseding ADR and owner review.
