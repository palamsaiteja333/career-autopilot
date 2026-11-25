# Job Search Agent — Functional requirements

Version: 1.0 | Date: 2026-11-25 | Status: agreed search defaults; implementation not started

Parent: [PRD](product-requirements.md) · [Functional requirements](functional-requirements.md) · [User stories](user-stories.md) · [CA-002](https://github.com/palamsaiteja333/career-autopilot/issues/2)

## 1. Purpose and scope

Find current, relevant opportunities with direct job/application links, reduce repetitive discovery work, and provide evidence for the candidate to choose which jobs to apply for. This agent is read-only with respect to external job platforms. Application preparation and submission belong to a separate workflow.

## 2. Agreed default configuration

| Setting | Default |
|---|---|
| Target roles | AI Engineer; Forward Deployed Engineer (FDE); Applied AI Engineer; Agentic AI Engineer; AI Software Engineer; AI Agents Engineer |
| Geography | Canada-wide, including Canadian onsite/hybrid jobs, and remote jobs explicitly eligible for Canada-based candidates |
| Sources | Company career pages, Greenhouse, Lever, web search |
| Freshness | Last 2 days (rolling 48 hours) |
| Scheduled discovery | Every 24 hours |
| Maximum ranked results | 10 per run |
| Execution modes | Both natural-language on-demand requests and saved preferences (including scheduled execution) |

All defaults are configurable. An explicit on-demand override affects only that run unless the user elects to save it. No salary, seniority, employment type or employer filter is assumed. Schedule time, timezone and notification channel are configuration decisions, not yet selected.

## 3. Functional requirements

| ID | Priority | Requirement | Observable acceptance criterion | Parent |
|---|---|---|---|---|
| JS-001 | Must | Save and edit the search configuration, including all six role families, geography, sources, freshness, cadence and result cap. | A new profile starts with the defaults in section 2; edits affect later scheduled runs. | FR-003 |
| JS-002 | Must | Interpret natural-language search requests and merge explicit overrides with saved preferences. | “Remote FDE jobs in Canada” narrows that run; saved settings remain unchanged. Ambiguous conflicting criteria request clarification. | FR-003 |
| JS-003 | Must | Discover postings through permitted company career pages, Greenhouse, Lever and web search. | Each configured source category can be attempted using an authorized integration; unavailable sources are reported, not silently ignored. | FR-004, FR-016 |
| JS-004 | Must | Normalize postings and preserve original source, timestamps, job identity and direct application URL. | Every ranked record has a title, employer, location/work arrangement, original source URL, observation timestamp and verified destination URL. | FR-004 |
| JS-005 | Must | Match the six role families using titles and actual responsibilities, including sensible aliases and seniority variants. | A Forward Deployed AI Engineer may match FDE; a generic unrelated software engineer is not included solely because a description mentions AI. | FR-003, FR-006 |
| JS-006 | Must | Verify Canada geographic eligibility separately from candidate work authorization. | Canada onsite/hybrid and explicitly Canada-eligible remote roles qualify; US-only remote roles are excluded; ambiguous remote restrictions go to unverified results. No legal status is inferred. | FR-003, FR-006 |
| JS-007 | Must | Enforce a rolling 48-hour freshness window at run start using source-supported posting timestamps. | An active job posted 47 hours ago qualifies; one posted 49 hours ago does not. Missing/ambiguous publication dates are labeled unverified; crawl/first-seen/update timestamps are not treated as original publication without evidence. | FR-003, FR-004 |
| JS-008 | Must | Verify that a job is active and that its destination resolves to the matching posting or application page. | A generic careers homepage, expired job, or mismatched redirect is not ranked as a verified opportunity; temporarily inaccessible listings are labeled unverified. | FR-004, FR-006 |
| JS-009 | Must | Deduplicate within and across runs using stable provider identity and canonical destination, with conservative cross-source matching. | A company posting also surfaced by web search appears once, retains provenance, and is not silently merged with a distinct requisition. | FR-005 |
| JS-010 | Must | Evaluate role relevance and candidate fit using job description evidence and verified profile facts. | Explanations identify matches, gaps and unknowns without invented experience; if no resume/profile is available, role-only ranking is explicitly labeled. | FR-002, FR-006 |
| JS-011 | Must | Rank eligible, active, fresh unique opportunities and return at most 10. | With 15 eligible postings, return the top 10; with 4, return 4. Never pad with expired, irrelevant or unverified jobs. | FR-006 |
| JS-012 | Must | Execute saved searches every 24 hours, support on-demand searches, persist search history and expose run status. | A scheduled run uses saved settings, each manual run has a distinct identity, repeated triggers for the same schedule slot do not create duplicate logical runs. | FR-007, FR-015 |
| JS-013 | Must | Deliver a daily run summary and notify about new matches without repeat notifications. | Repeat sightings are marked previously seen; already submitted jobs are excluded from new recommendations; a no-results run reports zero; delivery failure is visible. | FR-005, FR-007, FR-015 |
| JS-014 | Must | Expose source failures and incomplete coverage, and preserve valid partial results. | One failed source produces a partial run with source error status; all failed sources produce failed status, not a successful zero-result search. | FR-004, FR-017 |
| JS-015 | Must | Treat posting content as untrusted and enforce read-only tools, permitted sources and privacy boundaries. | Embedded instructions requesting credentials, profile disclosure or submission do not trigger external actions; private profile data is not sent to discovery providers. | FR-016, FR-018 |
| JS-016 | Must | Make run decisions and source outcomes auditable with privacy-safe metadata. | Each run has a correlation ID, configuration snapshot, counts and exclusion reasons, source statuses, latency and model usage/cost estimates where available. No raw private data appears in logs. | FR-017 |

## 4. Search eligibility and ranking

Apply hard filters before ranking: role relevance, geography, freshness, active verified destination and prior submitted application state. Unknown geography, freshness or availability must not be promoted into the verified top 10. Keep separately labeled unverified observations available for inspection; they do not count toward the cap. Previously discovered but unapplied active jobs can recur in ranked results and must be marked as seen; new-match notifications are sent only once per relevant event.

Rank the remaining jobs by evidence-backed role/responsibility fit and verified skills/experience alignment; use newer posting time as a tie-breaker, then stable job identity for reproducibility. Show match reasons and meaningful gaps. Exact weights, score calibration and minimum relevance thresholds will be decided during design/evaluation rather than claimed as validated.

For postings with dates but no precise time, rank only when the available date evidence establishes the entire possible publication interval falls within the configured window; otherwise flag uncertainty. Use UTC internally for comparisons and present times in the user's configured timezone. Future-dated or contradictory timestamps require verification.

## 5. Result contract (conceptual, not an API schema)

A ranked opportunity includes: stable job ID; employer; title; location and work arrangement; Canada eligibility evidence; posting timestamp and precision; observed/last verified time; source and provenance; original link and verified job/application link; role family; match rationale and gaps; freshness/availability status; seen/application status; rank and optional calibrated score. Salary and employment type are included only when available; missing information remains unknown.

A search run includes: run ID, trigger type, effective configuration/version, start and finish time, overall status (completed/partial/failed/cancelled), per-source outcomes, discovered/deduplicated/excluded/unverified counts, ranked results, notification status, correlation ID. Zero matches is a valid completed outcome only when coverage succeeded; partial results explicitly identify gaps.

## 6. User stories and acceptance scenarios

| ID | User story | Acceptance scenario | Requirements |
|---|---|---|---|
| JS-US-01 | As a candidate, I want to find the six target role families in Canada or remotely from Canada. | Given AI/FDE jobs in Toronto, Canada-eligible remote and US-only remote, rank the first two if other filters pass and exclude the third. | JS-001–006 |
| JS-US-02 | I want recently posted jobs with working links. | Given jobs aged 47h, 49h, undated and expired, only the verified active 47h posting qualifies. | JS-007–008 |
| JS-US-03 | I want a short, meaningful list rather than duplicates. | Given 15 eligible distinct jobs and several repeated copies, rank at most 10 unique jobs with explanations and links. | JS-009–011 |
| JS-US-04 | I want automatic daily discovery and the ability to search immediately. | Given a saved daily search and a one-off natural-language request, both execute; the one-off override does not change the schedule defaults. | JS-001–002, JS-012–013 |
| JS-US-05 | I want to know when coverage is incomplete. | Given Lever times out while another source succeeds, show valid partial results and the failed source. If all sources fail, show failed status. | JS-014, JS-016 |
| JS-US-06 | I want my candidate information to remain private and recommendations truthful. | Given a malicious posting requesting a resume upload or fabricated skill, no such action succeeds and the match rationale stays grounded. | JS-010, JS-015–016 |

## 7. MVP acceptance checklist

- [ ] All six role families and both execution modes covered by synthetic tests.
- [ ] Canada eligibility, freshness, verified links and duplicates tested across all configured source categories; authorized integration coverage documented.
- [ ] At most 10 ranked results with direct links; fewer results and zero-results cases tested.
- [ ] Daily schedule, on-demand overrides, trigger deduplication and new-match notification behavior tested.
- [ ] Partial failures, all-source failure, missing resume, unknown timestamps and prompt injection tested.
- [ ] Precision@10 evaluated against candidate-reviewed labels; PRD target remains provisional (>=80%, report sample size and returned-result count).
- [ ] No private candidate data in the public repository, source requests or raw telemetry.

## 8. Design decisions deferred

Actual source adapters, search provider and licensing, company discovery/catalog strategy, query expansion, source pagination and budgets, scheduling timezone/start time, notification channel, scoring weights, persistence, workflow nodes, MCP contracts, AWS service choices and operational SLOs. The four source categories are agreed; their specific access methods and availability must be verified before live integration. No live search, schedule, infrastructure or implementation has been created by this document.
