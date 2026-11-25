# Engineering backlog and milestones

Status: seven M1 GitHub issues created; native GitHub milestone objects still pending manual creation. No due dates are committed; progress is based on acceptance criteria.

## Milestones

| Milestone | Exit criteria |
|---|---|
| M1 — Product & System Design (Week 1) | Product baseline, functional and non-functional requirements, architecture, data model, threat model and ADRs reviewed. |
| M2 — Engineering Foundation | Local service skeleton, tests, CI and AWS sandbox with initial telemetry. |
| M3 — Job Discovery MVP | Grounded ranked search with permitted sources, deduplication, MCP and skills. |
| M4 — Application Assistance MVP | Grounded documents, mock ATS, durable human input/approval, reconciliation and assisted handoff. |
| M5 — AWS Release & Operations | Deployed authenticated system, evaluations, alarms, budget, operational runbook and release checks. |

## M1 issues

### [CA-001 — Initialize public repository and product documentation](https://github.com/palamsaiteja333/career-autopilot/issues/1)
Labels: documentation

- Establish README, product vision, competitive research and PRD baseline; preserve privacy and avoid implementation code.
- Acceptance: documents are committed, links resolve and public content contains synthetic examples only.

### [CA-002 — Review functional requirements and user stories](https://github.com/palamsaiteja333/career-autopilot/issues/2)
Labels: documentation

- Review FR-001 through FR-018 and US-01 through US-10; confirm MVP vs conditional live adapter.
- Acceptance: requirements are prioritized, traceable and have observable acceptance criteria.

### [CA-003 — Define non-functional requirements and evaluation plan](https://github.com/palamsaiteja333/career-autopilot/issues/3)
Labels: documentation

- Set measurable latency, availability, cost, privacy, retention, RTO/RPO and evaluation targets based on intended workload.
- Acceptance: define measurement boundaries, test datasets and release gates; do not invent achieved metrics.
- Draft deliverables: [NFR v0.1](../01-product/non-functional-requirements.md) and [evaluation plan v0.1](../01-product/evaluation-plan.md). Owner review of numerical targets pending.

### [CA-004 — Design high-level architecture](https://github.com/palamsaiteja333/career-autopilot/issues/4)
Labels: documentation

- Compare AgentCore runtime and API hosting alternatives, model/tool boundaries, queues, state, deployment and telemetry.
- Acceptance: Mermaid component and request-flow diagrams with failure paths and service rationale.

### [CA-005 — Design agent lifecycles and interfaces](https://github.com/palamsaiteja333/career-autopilot/issues/5)
Labels: documentation

- Define inputs, outputs, LangGraph nodes, skills, MCP tool contracts, conditional routes and human interrupts.
- Acceptance: trace discovery and application scenarios including cancellation, changed approval and unknown submission outcome.

### [CA-006 — Design data model and threat model](https://github.com/palamsaiteja333/career-autopilot/issues/6)
Labels: documentation

- Identify access boundaries, profile/document versioning, job identity, workflow state, approval ledger, deletion and attack surfaces.
- Acceptance: documented data ownership, encryption, authorization, privacy-safe telemetry and threat mitigations.

### [CA-007 — Record architecture decisions and prioritize implementation backlog](https://github.com/palamsaiteja333/career-autopilot/issues/7)
Labels: documentation

- Write ADRs for orchestration, runtime, state, source integration, tool authorization and observability; capture alternatives and trade-offs.
- Acceptance: implementation backlog is sequenced with dependencies and testable definitions of done.

## GitHub setup notes

The personal public repository, MIT license, Python gitignore and initial documentation are present on `main`. The seven M1 issues have been created; CA-002 is closed and CA-003 has draft deliverables pending target review. Create native milestone entries in Issues > Milestones and assign issues #1–#7 to M1. Leave CA-001 open until the documentation is reviewed. No real candidate information belongs in issues, docs or fixtures.
