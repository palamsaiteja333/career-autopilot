# CareerAutopilot

**Your career. On autopilot. In your control.**

An open-source, production-oriented agentic AI career automation platform for discovering relevant jobs, preparing accurate applications and managing the career journey with human oversight.

> Status: product discovery / design. No application code or deployed infrastructure yet.

## Initial product

- Discover and rank AI Engineer, Forward Deployed Engineer and related opportunities, including Canada-wide and Canada-eligible remote roles.
- Prepare application materials grounded in a verified candidate profile.
- Pause for missing information and require explicit approval before authorized external submission.
- Track outcomes, recover from failures and retain an auditable execution history.

Future modules may support recruiter communication, professional content and interview preparation.

## Proposed technology

Python, FastAPI, Pydantic, LangGraph, MCP, versioned agent skills, Amazon Bedrock and AgentCore, DynamoDB, S3, AWS CDK, GitHub Actions, OpenTelemetry and CloudWatch. Specific hosting, persistence and security choices will be validated through architecture decision records (ADRs).

## Documentation

| Document | Status |
|---|---|
| [Product vision](docs/01-product/product-vision.md) | Baseline |
| [Market and competitive analysis](docs/01-product/competitive-analysis.md) | Initial research |
| [Product requirements (PRD)](docs/01-product/product-requirements.md) | v0.2 baseline; targets provisional |
| [Functional requirements](docs/01-product/functional-requirements.md) | v0.2; discovery defaults finalized |
| [User stories](docs/01-product/user-stories.md) | v0.2; discovery stories expanded |
| [Job Search Agent requirements](docs/01-product/job-search-agent-requirements.md) | v1.0; agreed defaults |
| [Milestones and issue backlog](docs/07-planning/engineering-backlog.md) | Proposed |

## Development principles

Design before implementation; use deterministic logic where possible; make model decisions evidence-grounded; use least privilege; test failure recovery; instrument from the start. Keep the public repository free of actual resumes, candidate answers, credentials, application payloads and private traces. Use synthetic fixtures only. No unauthorized scraping, CAPTCHA bypass, or bulk application spam.

## Learning objectives

Document architectural trade-offs, agent lifecycles, durable state, tool authorization, human approvals, evaluations, AWS deployment and operations alongside the product. The project is intended as a practical learning and portfolio case study, not a claim of production readiness.

## License

This project is licensed under the MIT License; see [LICENSE](LICENSE).
