# Non-functional requirements (NFR)

Version: 0.1 | Date: 2026-11-25 | Status: proposed design targets, pending owner review and measurement

Parent: [PRD](product-requirements.md) · [Job Search Agent](job-search-agent-requirements.md) · [Job Application Agent](job-application-agent-requirements.md) · [Evaluation plan](evaluation-plan.md) · [CA-003](https://github.com/palamsaiteja333/career-autopilot/issues/3)

## 1. Workload and assumptions

The MVP is a single-candidate, authenticated application, not a commercial multi-tenant SaaS. Agreed product workload: one scheduled discovery per 24 hours plus on-demand searches, rolling 48-hour lookback, up to 10 ranked results, at most 5 new application preparations per candidate per local calendar day. Human waits can last days. No bulk applications. Authorized source rate limits take precedence.

Proposed planning workload: 30 scheduled + 10 manual discovery runs and 30 application preparations in a 30-day month; up to 5 new preparations/day and an initial load test of 2 simultaneous search runs and 5 concurrent preparation requests from the single owner. Additional synthetic requests can test saturation and quota rejection; this is not a promise to support multiple users. A search may inspect up to 100 normalized candidate postings initially (configurable; source budgets/pagination deferred); any truncated coverage is reported. Measure actual volumes, token use and source coverage before increasing limits.

## 2. Measurement definitions

- SLI: measured service indicator; SLO: internal objective; SLA: contractual commitment (none for MVP).
- p95: 95th percentile of recorded observations; report sample size and p50/p95/p99 where sufficient data. Do not claim percentiles from tiny samples.
- API latency: authenticated request arrival to response, measured separately from asynchronous workflow execution.
- Search latency: accepted run to durable terminal result (completed/partial/failed), includes queue, source and inference time. Report successful/partial/failed populations separately; timeouts cannot be hidden.
- Application active latency: sum of automated processing and queue time to first human-actionable state or completed draft; excludes time waiting for human input/approval. Measure subsequent resume segments and submission separately. Mock and live adapter performance reported separately.
- Availability: proportion of valid core API requests served successfully over rolling 30 days; include service-caused timeout/5xx; exclude deliberate user errors and expected quota/authorization rejections. Track scheduled search delivery and external source failures separately; report planned downtime and low sample count.
- RTO is the targeted time to restore service after an incident; RPO is the targeted maximum acceptable historical data loss for disaster restore, not permission to lose acknowledged in-flight approvals.

## 3. Requirements and provisional targets

| ID | Category | Proposed target / constraint | Verification |
|---|---|---|---|
| NFR-001 | API responsiveness | p95 <= 500 ms for ordinary dashboard reads and asynchronous request acceptance; exclude document transfer, report separately. | Load test against deployed staging API. |
| NFR-002 | Discovery latency | p95 <= 120 s for successful/partial search at reference workload; bounded overall execution <= 300 s before a visible partial/failed result. | Timed runs with controlled and permitted live sources, record coverage. |
| NFR-003 | Application latency | p95 <= 90 s automated time to first actionable state or draft in supported mock ATS; <= 300 s per automated segment before a visible recoverable failure/timeout. | Timed labeled mock scenarios, exclude human wait explicitly. |
| NFR-004 | Concurrency/backpressure | Accept two concurrent search runs and five concurrent valid preparation requests within quota; bound active workers and queued work; reject excess with visible reason; one logical submission per application. | Concurrent synthetic test; verify quotas and no silent drops. |
| NFR-005 | Core availability | 99.5% rolling 30-day request-based objective for authenticated core API; no commercial SLA. | Synthetic health checks and request SLI; report failures and sample count. |
| NFR-006 | Scheduled delivery | >=99% scheduled runs reach a visible result or explicit failure within 15 minutes of scheduled time over rolling 30 days; separately report successful/partial/failed discovery rates. | Scheduler-event-to-terminal-status measurement; report exact counts for low volume. |
| NFR-007 | Durable workflow | Zero lost acknowledged approvals, answers and checkpoints in tested process/container restart scenarios; interrupted drafts recover within 60 s of service recovery and resume request, excluding external waits. | Kill/restart at boundaries and verify state/provenance; no blind resend. |
| NFR-008 | Retry and failure isolation | Bounded retries with exponential backoff/jitter for transient read-only operations, source-specific timeouts and rate limits; do not retry ambiguous external writes. | Inject timeouts, throttling and 5xx; check partial results and unknown outcome. |
| NFR-009 | Business correctness | No duplicate submitted applications, unapproved sends, unsupported candidate claims or unauthorized tools in release scenarios; quota enforced atomically. | Adversarial and concurrency tests, all safety gates must pass. |
| NFR-010 | Recovery | Proposed single-region backup/restore RTO <= 4 hours, RPO <= 24 hours for recoverable persisted data. Ordinary restart guarantees NFR-007 are stricter; after disaster restore disable submissions until approvals, external outcomes and duplicates are reconciled. | Restore drill and reconciliation checklist; regional outage is not a guaranteed recovery scenario. |
| NFR-011 | Authentication/authorization | All private profile, workflow, document and approval operations authenticated and owner-scoped; least privilege for tools and infrastructure; separate environments. | Unauthorized, cross-owner synthetic and privilege tests. |
| NFR-012 | Data protection | TLS in transit, managed encryption at rest, secret manager, no credentials in repo; no raw candidate payloads or secrets in operational telemetry. | Configuration review, log scans, synthetic canary secrets and security tests. |
| NFR-013 | AI/tool safety | Treat external content as untrusted; model guardrails plus deterministic policy, argument validation, permitted destinations and human approval. | Prompt injection and exfiltration tests; zero prohibited side effects. |
| NFR-014 | Retention/deletion | Proposed: profile/resume while user retains it; search metadata 90 days; operational logs/traces 30 days; minimum necessary application/audit metadata 180 days; backups <=30 days. On deletion, revoke live retrieval immediately and purge active private data within 7 days; backup expiry per policy and prevent deleted data resurrection. | Synthetic deletion/restore tests; review policy before live data. |
| NFR-015 | Observability | Every accepted workflow gets correlation/run IDs, terminal or waiting status, source/tool outcomes, duration, usage/cost estimates and approval events; no raw PII. Trace critical paths in staging; production sampling decisions deferred. | Inspect correlated traces, logs, metrics and dashboards; simulate failure alarms. |
| NFR-016 | Alerting | Detect persistent core health failures, scheduled-run miss, unknown submission outcome, failed queue work and budget thresholds; target alert visible within 5 min of metric/event availability for critical operational events. | Controlled incident drills; alert delivery channel and thresholds finalized in operations design. |
| NFR-017 | Cost efficiency | Proposed recurring cloud and paid integration budget target USD 50/month for reference workload; per-run variable cost target <= USD 0.25 discovery, <= USD 0.50 application preparation (including attributable model, paid tools and variable runtime). | Tag and reconcile spend; report per-run estimates, monthly actuals, fixed costs and attribution uncertainty. |
| NFR-018 | Cost controls | Meter tokens/tool calls and cap workflow execution; alerts at 50/80/100% monthly budget; pause new optional paid work at estimated ceiling, retain dashboard, recovery and safety controls. Budget alerts are not a hard billing cap and usage may lag. | Simulated budget thresholds; no approval bypass or loss of state. |
| NFR-019 | Extensibility | New agent can register its workflow, skills and permitted tools using shared identity, persistence, approvals and telemetry without modifying existing agent business logic. | Architecture review and later third-agent test fixture. |
| NFR-020 | Maintainability | Version prompts, skills, schemas and decisions; reproducible environments; automated unit/integration/evaluation and security checks before release; rollback/runbook documented. | CI evidence, dependency review and rollback drill. |

## 4. Cost planning

Illustrative planning arithmetic, not a price quote: 40 discovery runs x USD 0.25 + 30 preparations x USD 0.50 = USD 25 variable target, leaving USD 25 for fixed/shared services at the USD 50 monthly target. This may be infeasible for always-on hosting, paid search or browser tools; validate region-specific pricing and actual usage during architecture design. Maximum daily usage is not the normal workload and can exceed this estimate; enforce per-run and monthly controls, not automatic unbounded spending. No AWS spend is authorized or incurred by this document.

## 5. Release gates and open decisions

See [evaluation plan](evaluation-plan.md) for AI quality and safety metrics. Performance, availability, cost and recovery objectives are provisional until measured. Safety invariants are mandatory, not relaxed by average quality. If a target is missed, investigate, record evidence and either fix or obtain explicit documented acceptance for a revised non-safety target before release.

Open decisions: owner approval of targets, timezones, notification channels, source coverage/pagination, model selection, regional data handling, retention and approval expiry, actual hosting costs, backup/recovery design and telemetry sampling. No infrastructure or SLA is created by this specification.
