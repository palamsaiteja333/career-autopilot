# ADR-011: Canada Central and reproducible AWS delivery

Date: 2026-11-25 | Status: Accepted design decision; implementation and feasibility validation pending

## Context
Owner chose Canada Central and low-cost serverless AWS with separate environments.

## Decision
Prefer ca-central-1, subject to actual model/service feature, privacy and budget feasibility. AWS CDK Python, GitHub Actions OIDC scoped to repo/environment, ECR versioned runtime image; synthetic local/staging first, distinct resources/roles, no always-on dev estate by default.

## Alternatives considered
Manual console provisioning: difficult to reproduce. Other AWS region/cross-region inference: not automatically permitted. Long-lived CI access keys: avoid. NAT/always-on services: defer unless justified.

## Consequences and trade-offs
CI/IaC and regional gating upfront; separate paid deployment authorization, explicit rollback and budget validation. Never silently send private data across regions.

## Validation and revisit conditions
Regional matrix and pricing model; OIDC/least privilege, repeatable deployment and rollback, artifact versioning, no secrets or personal data in public repo.

## Traceability
HLD-D04,D08; NFR-011,012,017,020. See [HLD](../02-architecture/high-level-design.md), [LLD](../02-architecture/low-level-design.md), [data model](../02-architecture/data-model.md), [threat model](../04-security/threat-model.md) and [implementation backlog](../07-planning/implementation-backlog.md). No code or infrastructure is authorized by this ADR. Material deviations require an amended/superseding ADR and owner review.
