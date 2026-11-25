# User stories and acceptance scenarios

v0.3. Both MVP agent story sets finalized. All examples are synthetic.

| Story | As a candidate, I want... | Acceptance scenarios | Requirements |
|---|---|---|---|
| US-01 | To set role and geographic preferences so results are eligible. | Given Canada-wide and Canada-eligible remote criteria, when search runs, a confirmed US-only role is excluded and unknown eligibility is marked. | FR-003, FR-006 |
| US-02 | To discover ranked opportunities without duplicates. | Given repeated source records, when searching twice, each canonical job is listed once with original link and matching evidence. | FR-004–006 |
| US-03 | To receive new opportunities automatically. | Given a schedule, when a new match appears, receive one notification; failures are visible. | FR-007 |
| US-04 | To use my original approved resume without invented experience. | Given a job requiring an unfamiliar tool, the original attachment remains unchanged; any requested cover letter and form answers contain no fabricated experience. | FR-002, FR-008 |
| US-05 | To provide missing answers later. | Given a missing mandatory question, when the workflow pauses and the process restarts, I can answer and resume safely. | FR-009–010 |
| US-06 | To control what is sent and where. | Given a completed draft, when approving, the payload version and destination are recorded; modifying either requires fresh approval. | FR-011–013 |
| US-07 | To avoid applying twice. | Given an ambiguous submission timeout, when retry is requested, the system reconciles the outcome before allowing another send. | FR-014–015 |
| US-08 | To see what happened and stop work. | Given a pending application, when cancelled, subsequent submission is blocked; already completed external actions are not falsely reported as reversed. | FR-015 |
| US-09 | To keep my data safe. | Given a malicious job description requesting resume exfiltration, when processed, no unauthorized tool invocation succeeds. | FR-001, FR-016, FR-018 |
| US-10 | To understand and debug the system. | Given a failed tool call, when viewing the workflow, the status and correlation ID identify the failure without exposing private content. | FR-017 |

Release testing should include happy paths, malformed source data, prompt injection, missing answers, expired approvals, concurrent requests and crashes before/after external side effects.

## Detailed discovery stories

See [Job Search Agent v1.1](job-search-agent-requirements.md#6-user-stories-and-acceptance-scenarios) for JS-US-01–06, covering the agreed Canada-wide/remote, six-role, 48-hour, daily top-10 search defaults, incomplete coverage and privacy. These extend US-01–03, US-09 and US-10.

## Detailed application stories

See [Job Application Agent v1.2](job-application-agent-requirements.md#6-user-stories-and-acceptance-scenarios) for JA-US-01–08, covering explicit selection, five daily preparations, original resume, cover letter on request, missing answers and consent, individual approval, safe submission/handoff, recovery, dashboard notifications and privacy. These extend US-04–10.
