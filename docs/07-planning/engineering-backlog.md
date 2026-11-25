# Engineering backlog and milestones

Status: proposed GitHub tracking plan. These are issue drafts, not created GitHub issues or milestones. No due dates are committed; progress is based on acceptance criteria.

## Milestones

| Milestone | Exit criteria |
|---|---|
| M1 — Product & System Design (Week 1) | Product baseline, functional and non-functional requirements, architecture, data model, threat model and ADRs reviewed. |
| M2 — Engineering Foundation | Local service skeleton, tests, CI and AWS sandbox with initial telemetry. |
| M3 — Job Discovery MVP | Grounded ranked search with permitted sources, deduplication, MCP and skills. |
| M4 — Application Assistance MVP | Grounded documents, mock ATS, durable human input/approval, reconciliation and assisted handoff. |
| M5 — AWS Release & Operations | Deployed authenticated system, evaluations, alarms, budget, operational runbook and release checks. |

## M1 issue drafts

### CA-001 — Initialize public repository and product documentation
Labels: documentation

- Establish README, product vision, competitive research and PRD baseline; preserve privacy and avoid implementation code.
- Acceptance: documents are committed, links resolve and public content contains synthetic examples only.

### CA-002 — Review functional requirements and user stories
Labels: documentation

- Review FR-001 through FR-018 and US-01 through US-10; confirm MVP vs conditional live adapter.
- Acceptance: requirements are prioritized, traceable and have observable acceptance criteria.

### CA-003 — Define non-functional requirements and evaluation plan
Labels: documentation

- Set measurable latency, availability, cost, privacy, retention, RTO/RPO and evaluation targets based on intended workload.
- Acceptance: define measurement boundaries, test datasets and release gates; do not invent achieved metrics.

### CA-004 — Design high-level architecture
Labels: documentation

- Compare AgentCore runtime and API hosting alternatives, model/tool boundaries, queues, state, deployment and telemetry.
- Acceptance: Mermaid component and request-flow diagrams with failure paths and service rationale.

### CA-005 — Design agent lifecycles and interfaces
Labels: documentation

- Define inputs, outputs, LangGraph nodes, skills, MCP tool contracts, conditional routes and human interrupts.
- Acceptance: trace discovery and application scenarios including cancellation, changed approval and unknown submission outcome.

### CA-006 — Design data model and threat model
Labels: documentation

- Identify access boundaries, profile/document versioning, job identity, workflow state, approval ledger, deletion and attack surfaces.
- Acceptance: documented data ownership, encryption, authorization, privacy-safe telemetry and threat mitigations.

### CA-007 — Record architecture decisions and prioritize implementation backlog
Labels: documentation

- Write ADRs for orchestration, runtime, state, source integration, tool authorization and observability; capture alternatives and trade-offs.
- Acceptance: implementation backlog is sequenced with dependencies and testable definitions of done.

## GitHub setup notes

Create the personal public repository `career-autopilot` with a Python gitignore and MIT license if desired. Commit these documents on the default branch or a documentation branch with a pull request. Create the milestone entries in Issues > Milestones and create M1 issues from the drafts above. Leave CA-001 open until the documentation is actually committed and reviewed. No real candidate information belongs in issues, docs or fixtures.
