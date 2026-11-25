# Functional requirements

Version 0.3 | Both MVP agent specifications finalized; technical design pending | MoSCoW: Must / Should. IDs remain stable for traceability.

| ID | Priority | Requirement | Acceptance criterion |
|---|---|---|---|
| FR-001 | Must | Authenticate the candidate and isolate profile/workflow access. | Unauthenticated requests and cross-profile access are denied. |
| FR-002 | Must | Manage versioned resume and verified candidate facts. | Edits create a new version; facts retain provenance. |
| FR-003 | Must | Capture configurable role, location, remote eligibility and freshness filters. | Canada-eligible remote is distinguished from remote limited to other countries. Unknown remains explicit. |
| FR-004 | Must | Search permitted sources on demand and normalize results. | Each record includes a source, original link, observation time and availability status. |
| FR-005 | Must | Deduplicate jobs within and across runs. | Repeated provider ID or canonical link is not stored as another job; ambiguous matches are not merged silently. |
| FR-006 | Must | Rank jobs with evidence-backed explanations and hard eligibility filters. | Ineligible roles are excluded from eligible results; unverified criteria are labeled. |
| FR-007 | Must | Run configurable scheduled searches (default every 24 hours) and notify about new matches. | A scheduled run delivers results or a visible failure without repeated notifications for the same event. |
| FR-008 | Must | Prepare explicitly selected jobs only (max five new preparations daily), using the original approved resume and cover letters only on request. | Original attachment is unchanged, factual claims are verified, and quota and selection are enforced. |
| FR-009 | Must | Map supported form questions and identify missing or ambiguous answers; offer consent-based answer reuse. | Mandatory unknowns trigger an explicit dashboard request, not a guessed value; reusable answers require consent and valid scope. |
| FR-010 | Must | Persist and resume human input workflows. | After restart the same workflow can resume with authenticated answers. |
| FR-011 | Must | Review and individually approve exact application payload and destination. | Modified or expired approval cannot authorize a later changed payload; no batch approval. |
| FR-012 | Must | Support manual handoff and mock ATS submission. | Handoff is not marked submitted until confirmed; mock submission requires approval. |
| FR-013 | Should | Enable authorized live adapters only after permissions are verified. | An unsupported or disallowed destination is blocked; no live adapter is required for initial mock demonstration. |
| FR-014 | Must | Prevent duplicate external actions and reconcile ambiguous outcomes. | A timeout after send enters unknown/reconciliation state; no blind retry. |
| FR-015 | Must | Track job and application statuses, audit history and cancellation. | Users can distinguish draft, awaiting input, awaiting approval, handoff, submitting, unknown, submitted, failed and cancelled. |
| FR-016 | Must | Enforce tool and business policies independently of model instructions. | Malicious content cannot authorize disclosure or bypass approval. |
| FR-017 | Must | Provide privacy-safe operational visibility. | Correlated runs report status, latency, token/cost estimates, tool errors and approval events without raw private payloads. |
| FR-018 | Must | Allow profile/document deletion and workflow cancellation subject to stated retention. | Deleted profile data is not retrieved in later work; retained audit metadata follows documented policy. |

## Detailed agent requirements

- [Job Search Agent v1.0](job-search-agent-requirements.md): agreed defaults, JS-001–016, evidence and eligibility rules, result contract and acceptance scenarios. Extends FR-002–007, FR-015–018.
- [Job Application Agent v1.0](job-application-agent-requirements.md): agreed defaults, JA-001–020, consent, quota, approval, handoff and recovery rules, and acceptance scenarios. Extends FR-001–002, FR-008–018.

Next: define measurable non-functional targets and evaluation plan, then design APIs and state transitions.
