# ADR-009: Default encryption, optional MFA and revocable signed URLs

Date: 2026-11-25 | Status: Accepted design decision; implementation and feasibility validation pending

## Context
Private resume and candidate data; owner explicitly selected optional MFA, default managed encryption and short-lived signed URLs; immediate retrieval revocation and <=30-day backups remain mandatory.

## Decision
Cognito optional MFA with recommendation to enable; sensitive-action reauth design; least-privilege IAM identities, S3 SSE-S3 and DynamoDB AWS-owned keys, TLS. Signed URL maximum five minutes initially, exact object/version and action, validated storage/credential denial of existing links. Independent deletion journal, purge active data within seven days and restore write-disable. Preserve approved retention.

## Alternatives considered
Required MFA: stronger login security but owner selected optional. Customer-managed KMS: more control and cost/complexity; deferred. Authenticated broker: fallback for review if URL revocation fails. PITR alone: deletion creates possible 35-day system backup, violates <=30-day policy.

## Consequences and trade-offs
Password-only accounts have elevated risk, bearer links cannot be revoked by DB flag alone, no key-level customer control. No exception to retention or immediate access revocation. Do not enable real private data until controls verified; existing downloaded data cannot be recalled.

## Validation and revisit conditions
Optional MFA and reauth, unauthorized owner/role, URL revoke including old version/concurrent request, backup retention and PITR deletion behavior (test synthetic resources), S3 version purge, deleted-data restore drill. Block if unresolved.

## Traceability
Data model v1.0; threat model v1.0; NFR-011–014. See [HLD](../02-architecture/high-level-design.md), [LLD](../02-architecture/low-level-design.md), [data model](../02-architecture/data-model.md), [threat model](../04-security/threat-model.md) and [implementation backlog](../07-planning/implementation-backlog.md). No code or infrastructure is authorized by this ADR. Material deviations require an amended/superseding ADR and owner review.
