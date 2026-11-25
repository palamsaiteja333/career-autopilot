# ADR-008: Permitted sources and scheduled job discovery

Date: 2026-11-25 | Status: Accepted design decision; implementation and feasibility validation pending

## Context
Daily discovery of Canada-wide/Canada-eligible remote AI/FDE roles, verified freshness and links, maximum 10 ranked results.

## Decision
Company career pages, Greenhouse, Lever and licensed web search; known board/company catalog and source permissions. EventBridge elapsed 24-hour schedule, UTC instant and Toronto display; rolling 48-hour publication window, unknown evidence separated. Search read-only; deterministic filters/dedup/ranking with semantic fit.

## Alternatives considered
Unauthorized scraping, browser login automation or inferred dates: disallowed. Search all sites globally via ATS APIs: unsupported assumption. Fixed local cron: differs from elapsed 24h across DST.

## Consequences and trade-offs
Source coverage can be partial; actual catalog/search vendor and notification channel/anchor undecided. Return fewer than 10 rather than pad; show source failures.

## Validation and revisit conditions
Document terms, region and pricing for each adapter, 48h/DST/duplicate tests, verified links, coverage and precision/recall; no private candidate data to discovery providers.

## Traceability
JS-001–016; NFR-002,006; EV-001–003. See [HLD](../02-architecture/high-level-design.md), [LLD](../02-architecture/low-level-design.md), [data model](../02-architecture/data-model.md), [threat model](../04-security/threat-model.md) and [implementation backlog](../07-planning/implementation-backlog.md). No code or infrastructure is authorized by this ADR. Material deviations require an amended/superseding ADR and owner review.
