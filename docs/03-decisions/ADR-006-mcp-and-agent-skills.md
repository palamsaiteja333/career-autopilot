# ADR-006: Narrow MCP contracts and reviewed skills

Date: 2026-11-25 | Status: Accepted design decision; implementation and feasibility validation pending

## Context
Need reusable integrations, tool isolation and maintainable agent procedures, without giving models unrestricted actions.

## Decision
Use local MCP server/client first, then AgentCore Gateway with narrow authenticated adapters; six versioned reviewed skills with progressive disclosure. Ordinary Python for deterministic domain logic. Two retries after initial transient read-only call, bounded by deadline. Restricted submission tool programmatic only, never model-bound.

## Alternatives considered
Direct Python-only external integrations: simpler but less reusable and less MCP learning. Every function as MCP tool: unnecessary overhead. Arbitrary browser/HTTP/shell: unacceptable authority surface.

## Consequences and trade-offs
Contract testing, identity segregation, schema/version management, gateway compatibility and egress validation needed. Skills do not confer permissions.

## Validation and revisit conditions
Tool schema, allowed caller and destination tests, injection and exfiltration, gateway region/price, retry/timeout tests; verify write identity isolated.

## Traceability
HLD-D07; LLD sections 6–7; TM-03–06. See [HLD](../02-architecture/high-level-design.md), [LLD](../02-architecture/low-level-design.md), [data model](../02-architecture/data-model.md), [threat model](../04-security/threat-model.md) and [implementation backlog](../07-planning/implementation-backlog.md). No code or infrastructure is authorized by this ADR. Material deviations require an amended/superseding ADR and owner review.
