# Architecture Decision Records

Version: 1.0 | Date: 2026-11-25 | Status: records accepted Days 1–6 design decisions; validation remains pending.

ADRs explain context, decision, alternatives, consequences, validation and revisit conditions. Accepted means approved design intent, not tested capability or spend approval. Unresolved feasibility is tracked in the [implementation backlog](../07-planning/implementation-backlog.md). Keep history: supersede an accepted ADR when a material change is approved rather than silently rewriting the original.

| ADR | Decision |
|---|---|
| [ADR-001](ADR-001-serverless-api.md) | Serverless API and dashboard |
| [ADR-002](ADR-002-langgraph-agentcore-runtime.md) | Explicit LangGraph workflows on AgentCore Runtime |
| [ADR-003](ADR-003-durable-dispatch-and-idempotency.md) | Transactional outbox and at-least-once dispatch |
| [ADR-004](ADR-004-persistence-and-checkpointing.md) | DynamoDB and S3 with separated logical domains |
| [ADR-005](ADR-005-bedrock-models-and-budget.md) | Bedrock model adapter, bounded inference and evaluation |
| [ADR-006](ADR-006-mcp-and-agent-skills.md) | Narrow MCP contracts and reviewed skills |
| [ADR-007](ADR-007-human-approval-and-submission.md) | Human-controlled applications and independent authorization |
| [ADR-008](ADR-008-permitted-discovery-and-scheduling.md) | Permitted sources and scheduled job discovery |
| [ADR-009](ADR-009-security-privacy-and-retention.md) | Default encryption, optional MFA and revocable signed URLs |
| [ADR-010](ADR-010-observability-and-release-evaluation.md) | Privacy-safe observability and evidence-based release |
| [ADR-011](ADR-011-region-and-delivery.md) | Canada Central and reproducible AWS delivery |
| [ADR-012](ADR-012-defer-memory-and-rag.md) | Defer AgentCore Memory and dedicated RAG |

Day 7 review: [CA-007](https://github.com/palamsaiteja333/career-autopilot/issues/7). No implementation code.
