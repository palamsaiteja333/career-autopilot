# ADR-007: Human-controlled applications and independent authorization

Date: 2026-11-25 | Status: Accepted design decision; implementation and feasibility validation pending

## Context
External job submissions are irreversible and can expose private data; original resume must remain unchanged.

## Decision
Explicit user selection, five unique new preparations per Toronto calendar day, original resume, requested letters only, consent-based answer reuse, dashboard HITL, individual exact-payload approval for 24 elapsed hours. Separate restricted executor and transactional attempt ledger; mock ATS and manual handoff MVP; live adapter disabled pending explicit permission. Unknown external result must reconcile before fresh authorization/retry.

## Alternatives considered
Auto-apply/batch approval: violates approved product behavior. Model-issued approvals: no trustworthy authority. Blind retry on timeout: duplicate risk. Always manual: safe fallback but does not demonstrate authorized execution.

## Consequences and trade-offs
More user interaction and state; no pre-approval upload/autosave, approval changes invalidate immediately, cancel cannot undo in-flight action. External exactly-once cannot be guaranteed.

## Validation and revisit conditions
Approval expiry/change/replay, concurrent quota, cancel/send race, original checksum, required unknowns, crash after send and no duplicate; EV-004–009.

## Traceability
JA-001–020; LLD section 5; Data model section 7. See [HLD](../02-architecture/high-level-design.md), [LLD](../02-architecture/low-level-design.md), [data model](../02-architecture/data-model.md), [threat model](../04-security/threat-model.md) and [implementation backlog](../07-planning/implementation-backlog.md). No code or infrastructure is authorized by this ADR. Material deviations require an amended/superseding ADR and owner review.
