# Functional requirements

Version 0.1 | Draft | MoSCoW: Must / Should. IDs remain stable for traceability.

| ID | Priority | Requirement | Acceptance criterion |
|---|---|---|---|
| FR-001 | Must | Authenticate the candidate and isolate profile/workflow access. | Unauthenticated requests and cross-profile access are denied. |
| FR-002 | Must | Manage versioned resume and verified candidate facts. | Edits create a new version; facts retain provenance. |
| FR-003 | Must | Capture configurable role, location, remote eligibility and freshness filters. | Canada-eligible remote is distinguished from remote limited to other countries. Unknown remains explicit. |
| FR-004 | Must | Search permitted sources on demand and normalize results. | Each record includes a source, original link, observation time and availability status. |
| FR-005 | Must | Deduplicate jobs within and across runs. | Repeated provider ID or canonical link is not stored as another job; ambiguous matches are not merged silently. |
| FR-006 | Must | Rank jobs with evidence-backed explanations and hard eligibility filters. | Ineligible roles are excluded from eligible results; unverified criteria are labeled. |
| FR-007 | Should | Run configurable scheduled searches and notify about new matches. | A scheduled run delivers results or a visible failure without repeated notifications for the same event. |
| FR-008 | Must | Select a job and prepare grounded application materials. | All factual claims map to verified profile facts; unsupported claims are blocked. |
| FR-009 | Must | Map supported form questions and identify missing or ambiguous answers. | Mandatory unknowns trigger an explicit request, not a guessed value. |
| FR-010 | Must | Persist and resume human input workflows. | After restart the same workflow can resume with authenticated answers. |
| FR-011 | Must | Review and approve exact application payload and destination. | Modified or expired approval cannot authorize a later changed payload. |
| FR-012 | Must | Support manual handoff and mock ATS submission. | Handoff is not marked submitted until confirmed; mock submission requires approval. |
| FR-013 | Should | Enable authorized live adapters only after permissions are verified. | An unsupported or disallowed destination is blocked; no live adapter is required for initial mock demonstration. |
| FR-014 | Must | Prevent duplicate external actions and reconcile ambiguous outcomes. | A timeout after send enters unknown/reconciliation state; no blind retry. |
| FR-015 | Must | Track job and application statuses, audit history and cancellation. | Users can distinguish draft, awaiting input, awaiting approval, handoff, submitting, unknown, submitted, failed and cancelled. |
| FR-016 | Must | Enforce tool and business policies independently of model instructions. | Malicious content cannot authorize disclosure or bypass approval. |
| FR-017 | Must | Provide privacy-safe operational visibility. | Correlated runs report status, latency, token/cost estimates, tool errors and approval events without raw private payloads. |
| FR-018 | Must | Allow profile/document deletion and workflow cancellation subject to stated retention. | Deleted profile data is not retrieved in later work; retained audit metadata follows documented policy. |

Next: review priorities, design APIs and state transitions, and define measurable non-functional targets.
