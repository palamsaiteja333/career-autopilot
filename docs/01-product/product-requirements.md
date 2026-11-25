# Product requirements document (PRD)

Version: 0.4 | Date: 2026-11-25 | Status: approved requirements baseline; integration feasibility and measurement pending

## 1. Objective
Reduce repetitive job search and application work without sacrificing relevance, accuracy, privacy or user control. Build an extensible platform for future career agents and an end-to-end engineering learning case study.

## 2. Users and jobs to be done
Initial user: an individual technical job seeker. When searching, find active opportunities matching role, location and work arrangement. When applying, reuse verified information, prepare accurate materials, ask for missing answers and track the outcome. When returning after an interruption, resume safely without losing work.

## 3. MVP scope

### Discovery
Accept natural-language and structured preferences; search permitted sources on demand and on a configurable schedule; normalize postings and preserve provenance, location, remote eligibility, timestamps and original links; deduplicate; assess relevance against the candidate profile with evidence; rank results; flag unavailable or unverified postings; display and notify about results.

Agreed discovery defaults: AI Engineer, Forward Deployed Engineer, Applied AI Engineer, Agentic AI Engineer, AI Software Engineer and AI Agents Engineer; Canada-wide and Canada-eligible remote; company career pages, Greenhouse, Lever and web search; rolling 48-hour freshness; every 24 hours; at most 10 verified ranked results per run; both on-demand natural-language and saved-preference searches. See [Job Search Agent functional requirements](job-search-agent-requirements.md).

### Candidate profile
Allow the user to upload and version resumes and maintain verified experience, preferences and approved answers. Store answer provenance and scope. Unknown, expired or sensitive answers must not be inferred. The user can update or delete profile information.

### Application assistance
Select a job explicitly, retrieve the original approved resume unchanged, generate a truthful cover letter only on request, map supported form questions to candidate facts, identify required unknowns, pause for input, validate completeness, show exact materials and destination for approval, and allow rejection/cancellation. Submit only through an authorized integration after explicit approval; otherwise provide a complete manual handoff. Never mark a handoff as submitted without user confirmation or reliable evidence.

Agreed application defaults: user-selected jobs only, original resume, cover letter on request, ask for missing answers and offer consent-based reuse, individual approval, at most five new preparations per day, dashboard-only application notifications. See [Job Application Agent functional requirements](job-application-agent-requirements.md).

### Workflow and dashboard
Persist workflow state, pending approvals, search results and application status. Resume after service restarts, recover safely from tool/model failures, detect duplicate attempts and reconcile unknown external outcomes. Provide user-facing history, notifications and traceable decisions.

## 4. Out of scope
Unauthorized website automation, bulk unsolicited applications, CAPTCHA bypass, inferred legal/work eligibility, unapproved external submission, live LinkedIn messaging/posting, multi-user SaaS, mobile apps and unrelated personal agents. Mock ATS automation is in scope for learning and testing; live submission is conditional on access and permission.

## 5. Approved release targets

| Measure | Approved target and method |
|---|---|
| Relevance | >=80% precision@10 on user-reviewed search results; report sample size and missing results separately. |
| Effort reduction | >=70% reduction in active discovery time against a measured manual baseline across comparable searches. |
| Field accuracy | >=90% correct supported fields with verified available answers, measured against labeled mock ATS cases. |
| Mandatory unknowns | 100% escalation in acceptance cases. |
| Truthfulness | Zero unsupported candidate claims in release evaluation cases. |
| Approval | 100% of external submissions have valid approval for exact destination and payload version in tests. |
| Duplicate submissions | Zero duplicates in retry/crash/concurrent approval tests; ambiguous external responses require reconciliation. |

These are approved design targets, not achieved results or production guarantees. See [non-functional requirements v1.0](non-functional-requirements.md) and [evaluation plan v1.0](evaluation-plan.md) for metric definitions, datasets and release gates. Approved operating defaults: single user, USD 50/month cloud and paid integrations target, 120 s search p95, 99.5% core API availability SLO, America/Toronto timezone for quota and schedule configuration. Measurement remains pending. Safety invariants are release blockers even when the aggregate accuracy target is met.

## 6. Risks and constraints
Source permissions and geographic eligibility can be ambiguous. Job descriptions are untrusted and may contain prompt injections. External systems can change forms or return ambiguous responses. Model costs, latency, regional availability, retention and personally identifiable information must be managed. Public GitHub stores synthetic data only.

## 7. Open decisions
Choose first authorized source adapters, discovery notification channel, schedule anchor time, approval lifetime, answer scope and implementation of approved retention/deletion policy, candidate schema and regional deployment. Confirm live submission permission before enabling any real adapter. Validate project-name availability before commercial branding.

## 8. Future roadmap
Networking and recruiter communication, professional branding/content, interview preparation and career intelligence. Keep extension interfaces generic but defer new agents until the MVP is measured and reliable.

## 9. Release criteria
Discovery and mock/assisted application workflow pass end-to-end and adversarial acceptance tests. Human approval and restart recovery are demonstrated. The deployed environment has authentication, least privilege, privacy-safe monitoring, cost alarms and an operational runbook. Unsupported live integrations remain disabled.
