# Week 2 Day 1 — Python engineering foundation

Status: first local-only scaffold; IMP-002 remains open pending lock/install and review.

## Decisions

Python 3.13 minor pinned in .python-version; project metadata constrains the interpreter to 3.13.x. Lambda supports Python 3.13, but AgentCore dependency/platform compatibility must be verified later. Use uv for environment and dependency resolution, Hatchling for package build, and a src layout so tests exercise imports from the package rather than accidentally importing loose repository files. Start with zero application dependencies; add Pydantic on domain day, FastAPI on API day and LangGraph/Bedrock only when needed. Dev groups configure pytest, Ruff and mypy; these are not runtime dependencies. No secrets or AWS credentials in .env.example. No actual dotenv reader yet.

## Local commands (from repository root)

1. `uv python install 3.13` (if missing)
2. `uv lock` (network or suitable package cache required on first run; review and commit uv.lock)
3. `uv sync --locked`
4. `uv run --locked career-autopilot`
5. `uv run --locked pytest -q`
6. `uv run --locked ruff check .`
7. `uv run --locked mypy src tests`

## Module boundaries (planned; only package and smoke entry point exist now)

| Package | Responsibility |
|---|---|
| domain | Pure domain entities and deterministic policies; no AWS/LLM |
| application | Use cases and ports, orchestration of domain operations |
| api | FastAPI routes and request/identity boundary |
| workflows | LangGraph nodes, state and workflow registry |
| adapters | Local and future AWS/model/MCP persistence adapters |
| telemetry | Privacy-safe tracing and metrics |

Dependencies point inward: API and adapters depend on application/domain abstractions, domain does not import SDKs. Shared services are logical modules, not separate microservices. Create packages when their first functionality is implemented. Skills, frontend, infrastructure and eval fixtures are added in later modules; synthetic only.

## Verification

The identical initial main module and smoke test were run in the assistant's isolated Python 3.13.5 environment using `PYTHONPATH=src python -m pytest -q` (1 passed), and the module printed the local banner. This was not a packaged install or the user's Mac. `uv lock --offline` failed because mypy was not cached; no resolved lockfile or clean uv install, Ruff or mypy execution is claimed. The PR remains draft, and #9 stays open until these checks pass with registry access. No application agent, FastAPI routes, AWS clients, deployment or real data exists. References: [uv project layout](https://docs.astral.sh/uv/concepts/projects/layout/), [uv lock/sync](https://docs.astral.sh/uv/concepts/projects/sync/), [Lambda runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html).
