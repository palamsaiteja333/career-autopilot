# Market and competitive analysis

Desk research: 2026-11-25. Based on public first-party product documentation and repository descriptions, not hands-on testing. Capabilities can change; no claim is made about competitors' private architecture, market share, prices, performance or comparative security.

| Product | Publicly described capabilities | Implication for CareerAutopilot |
|---|---|---|
| [CareerOps](https://github.com/career-ops-hq/career-ops) | Local AI CLI workflow for discovering/scoring jobs, tailoring materials, tracking and assisted applications; user submits. | Strong reference for skills, evidence-based matching and user ownership. |
| [JobOps](https://jobops.app/) | Open-source search workspace, configurable discovery, resume tailoring and application tracking. | A centralized job workspace and tracking are baseline expectations, not unique differentiators. |
| [Simplify](https://simplify.jobs/) | Commercial job matching, browser autofill, application tracking and advertised Autopilot submission for supported applications. | Compare usability and repetitive form reduction; do not assume access to the same integrations. |

## Positioning hypothesis
The intended distinction is a transparent, independently implemented AWS-native learning and self-hostable career workflow platform: durable LangGraph orchestration, versioned skills, MCP tool boundaries, explicit approval, evaluation and operational telemetry. These are design goals, not proven market advantages or assertions that competitors lack these features.

## Integration feasibility
- [Greenhouse Job Board API](https://docs.greenhouse.io/job-board): job reads are public; submitting an application requires authentication. Start with permitted reads and employer-hosted application links. Do not assume employer credentials are available.
- [LinkedIn prohibited software](https://www.linkedin.com/help/linkedin/answer/a1341387): unauthorized scraping and automated activity are restricted. Start with manual handoffs; future messaging/content publishing requires a supported integration and user approval.
- Other job sources and browser adapters require separate terms, rate-limit and access review. Use a synthetic mock ATS for automated submission and failure testing.

## Next research
Validate a representative set of Canadian AI/FDE roles against permitted sources. Measure baseline search and application time; compare relevance and coverage. Review API terms and costs, source freshness semantics and trademark/name availability. Record independent product design rather than copying competitor code or branding.
