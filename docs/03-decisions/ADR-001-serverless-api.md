# ADR-001: Serverless API and dashboard

Date: 2026-11-25 | Status: Accepted design decision; implementation and feasibility validation pending

## Context
One owner, 40 reference searches/month, USD 50 monthly target, API p95 500 ms; agent runs may take minutes.

## Decision
React/TypeScript on private S3 origin + CloudFront, Cognito and API Gateway HTTP API, FastAPI on Lambda using an ASGI adapter. API returns durable 202 acceptance and dashboard polls status. No continuously running API container.

## Alternatives considered
ECS Fargate + ALB: persistent processes and streaming but recurring idle costs. Synchronous API-to-agent calls: simpler but expose HTTP timeout and recovery risks. WebSockets/SSE deferred until needed.

## Consequences and trade-offs
Low idle cost, independently deployable API, but cold starts, Lambda limits and polling load must be measured. Upload/download via approved scoped short-lived signed URLs.

## Validation and revisit conditions
Cold/warm p95 <=500 ms for ordinary reads and accepted commands, auth and durable 202 tests, regional pricing and invocation limits. Revisit hosting only via reviewed ADR.

## Traceability
HLD-D01; NFR-001,005,017. See [HLD](../02-architecture/high-level-design.md), [LLD](../02-architecture/low-level-design.md), [data model](../02-architecture/data-model.md), [threat model](../04-security/threat-model.md) and [implementation backlog](../07-planning/implementation-backlog.md). No code or infrastructure is authorized by this ADR. Material deviations require an amended/superseding ADR and owner review.
