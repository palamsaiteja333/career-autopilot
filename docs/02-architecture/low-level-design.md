# Low-Level Design (LLD) — workflow contracts and shared services

Version: 1.0 | Date: 2026-11-25 | Status: owner-approved design baseline, subject to feasibility testing; no implementation
Parent: [HLD v1.0](high-level-design.md) · [Agent workflows](agent-workflows.md) · [NFR](../01-product/non-functional-requirements.md) · [Evaluation plan](../01-product/evaluation-plan.md) · [CA-005](https://github.com/palamsaiteja333/career-autopilot/issues/5)

## 1. Module boundaries

| Logical module | Responsibility | Depends on |
|---|---|---|
| API / authentication | FastAPI REST contracts, identity, owner checks, idempotent acceptance, dashboard status and HITL endpoints | Application services, repositories |
| Application services | Candidate profile, jobs, quota, draft, approval, cancellation, notification and submission ledger | Domain policies, repositories |
| Command ingress / outbox | Atomically persist accepted command and business changes, relay durable events to SQS | DynamoDB, SQS |
| Dispatcher | Claim lease, select registered workflow/version, invoke bounded AgentCore segment, acknowledge durable outcome | Command repository, runtime client |
| Workflow registry | Map workflow type/version to graph, state schema, skills and tool allowlist | Search and application graphs |
| Agent workflows | Explicit StateGraph nodes, edges, interrupts, budget and result orchestration | Domain services, model and MCP interfaces |
| Model adapter | Bedrock inference, structured response validation, Guardrails, usage/time budgets | Bedrock |
| Tool adapter | MCP discovery and invocation, typed results/errors, scoped authorization | AgentCore Gateway, tool backends |
| Skills registry | Load reviewed skill metadata and selected immutable SKILL.md instructions | Versioned deployment bundle |
| Persistence | DynamoDB business state, graph checkpointer, private S3 objects | AWS SDK; no model control |
| Reconciler | Recover outbox/leases, checkpoint projection gaps and unknown external outcomes | Repositories, allowed status tools |
| Telemetry | Correlated metrics, redacted logs, traces and cost attribution | ADOT, CloudWatch, X-Ray |

Domain and policy functions must not depend on a foundation model or specific cloud provider. AWS adapters implement ports; local development uses in-memory or durable local test adapters, with real AWS integration tests later. One source repository, independently deployed API/runtime/tool artifacts. Do not expose the agent runtime directly to the public dashboard.

## 2. Conceptual REST interfaces (not OpenAPI or implementation)

All routes except health require authenticated owner context; owner identity derived from validated token. Mutation requests have idempotency keys; version-sensitive mutations require expected resource version. Duplicate same-key/same-body returns existing outcome; same key with different body conflicts. Return minimal data, safe error code and correlation ID.

| Method/path | Input | Output / behavior |
|---|---|---|
| GET /health | No candidate data | Minimal health indicator; protected detailed readiness separately |
| GET/PUT /v1/preferences | Preference changes and expected version for writes | Current saved search config/version; schedule cadence remains 24h by default |
| POST /v1/profile/resumes/upload-intent | File metadata | Owner-bound short-lived upload target; size/type limits |
| POST /v1/profile/resumes/{id}/confirm | Upload/version reference | Validate object, scan status, checksum; approved original version only after user selection |
| GET/PATCH /v1/profile | Verified facts or edits | Versioned profile; provenance; explicit consent for reuse |
| DELETE /v1/profile | Confirmed deletion request | Accepted deletion job, block further retrieval |
| POST /v1/search-runs | Manual query or saved preferences | 202 + run ID; no synchronous inference |
| GET /v1/search-runs/{id} | Run ID | Status, coverage, counts, ranked job refs and waiting task if applicable |
| GET /v1/jobs/{id} | Job ID | Verified link, evidence, freshness and match details |
| POST /v1/applications | Explicit selected job ID | 202 + application/run ID; atomic daily quota; duplicate returns existing draft |
| GET /v1/applications/{id} | Application ID | Status, draft, pending task or confirmation; owner-only documents via short-lived access |
| GET /v1/tasks | Filter/status | Pending clarification/input/review/reconciliation inbox |
| POST /v1/tasks/{id}/answers | Answer(s), expected task version, explicit per-answer reuse consent | 202 + resume command; no automatic submission |
| POST /v1/applications/{id}/cover-letter | Explicit request or user-provided letter ref | 202 + draft revision command |
| POST /v1/applications/{id}/review | Decision, exact payload version/hash, expected version | Edit/reject/approve individually; approval ledger and command atomic |
| POST /v1/workflows/{id}/cancel | Expected version | Cancel if before send; in-flight external action remains subject to reconciliation |
| POST /v1/applications/{id}/reconcile | Evidence or manual confirmation, expected version | Record provider-verified vs user-confirmed outcome separately; no blind send |
| GET /v1/notifications | Cursor/status | In-app notices, deduplicated |
| POST /v1/notifications/{id}/read | Notice ID | Idempotently mark read |

Errors: 400 malformed input; 401 missing/invalid authentication; 403 denied action; 404 missing/non-owned resource without existence leakage; 409 version conflict, changed approval or idempotency mismatch; 422 unresolved semantic input; 429 quota or bounded admission limit; 503 service unavailable when acceptance not durable. A successful 202 guarantees a persisted command, not external success. No REST endpoint grants arbitrary tool execution.

## 3. State contracts (conceptual fields, no Python schema yet)

State is typed and versioned. Checkpoints carry bounded values or references; authoritative profile, quotas, approvals and submissions remain in business repositories. No credentials or whole resumes in state. All timestamps stored as UTC instants; timezone America/Toronto for quota and display, 24-hour elapsed schedule. Explicit provenance for uncertain data.

| Shared execution state | Meaning |
|---|---|
| owner_id, workflow_type, run_id, thread_id | Trusted scoped identity and stable graph thread |
| application_id (optional), command_id | Business identity and current logical action |
| graph_version, state_schema_version, checkpoint_version, business_version | Compatibility and transition markers |
| lease_epoch, invocation_id | Fence stale workers; not long-term workflow identity |
| configuration_snapshot_ref, model_config_version, skill_versions | Reproducibility |
| started_at, segment_deadline, remaining_cost/token/tool budgets | Bounded execution; human wait excluded from active duration |
| status, pending_task_ref, cancellation_version | Control state and durable interrupt reference |
| step_results / artifact_refs | Keyed bounded results, no raw document blobs |
| error_refs, usage_summary, correlation_id | Redacted outcomes and cost attribution |

Search-specific state: trigger, effective SearchCriteria, preference version, run-start freshness anchor, source plan/budgets, per-source result refs and pagination status, canonical job refs, eligibility/verification evidence refs, excluded/unverified refs, candidate-profile version, fit assessment refs, ordered ranked IDs, coverage and counts. Parallel result reducers merge by source/task identity with attempt/version checks, not append-only message lists. Application-specific state: selected job/destination, quota reservation ref, original resume version/hash, verified profile version, form schema/version, answer/provenance refs, unresolved questions, requested letter version, draft version, frozen payload manifest/hash, review task/approval reference, adapter capability, submission attempt ref and outcome evidence. Never trust a checkpoint approval flag as authorization.

## 4. Command processing and checkpoint consistency

Command envelope: schema version, command ID, type (start_search, start_application, resume_input, revise_draft, review_decision, cancel, reconcile), owner/run/application/thread refs, expected business version, pinned graph version, payload reference, accepted_at, correlation ID, schedule slot or idempotency key. SQS messages contain only identifiers and versions; private payloads remain in scoped storage.

1. Accept mutation using one DynamoDB transaction: validate expected version and authorization, reserve quota if new application, write business state + idempotency record + outbox command. Durable acceptance precedes 202.
2. Streams relay publishes SQS; keep outbox record until publish and processing status are reconciled. A periodic sweeper repairs missing dispatch. At-least-once events can duplicate.
3. Dispatcher validates command currentness, takes a conditional lease with monotonically increasing epoch and bounded expiry; checks cancel status. Only one active segment per thread. Duplicate terminal or stale commands acknowledge without executing. A busy command is deferred/retried within bounded policy.
4. Invoke AgentCore with trusted envelope, not arbitrary user instructions. Runtime checks lease/version at mutating boundaries. Use stable LangGraph thread ID, new invocation/session identity per segment as needed, and durable checkpointer. New graph start or resume uses the correct pinned graph version. A stale worker cannot commit business transition; checkpoint writes also need fencing or a single-writer guarantee verified for the chosen checkpointer. Do not permit a second writer until previous invocation termination or safe fenced checkpoint behavior is established.
5. Define each durable transition by deterministic transition ID, expected business version, checkpoint marker and result reference. A pending task/approval transition can exist before or after checkpoint commit; persist intent and reconcile projection by inspecting actual checkpoint/interrupt, never blindly replay an external effect. Do not expose an actionable task until both durable records agree. Resume commands are accepted only against consistent task/thread state; user answer and command are durably saved once. If consistency cannot be established, quarantine for recovery.
6. Persist terminal or waiting outcome and acknowledge SQS only after durable outcome; replay safe tasks with idempotency. If worker loses contact with runtime, do not assume runtime stopped. Reconcile lease, checkpoint and attempt state; block unsafe new writes. Runtime deadline, SDK read timeout, worker timeout and SQS visibility must be compatible; validate before deployment.

LangGraph interrupts can replay their node from the beginning; make pre-interrupt effects idempotent and keep submit in a separate node/tool. Multiple answers in one task are validated together; use distinct task IDs for later question rounds. Do not wrap interrupt control flow in broad exception handlers that swallow it. Business status and checkpoint position may differ briefly but must converge; formal data access patterns and recovery protocol follow CA-006.

## 5. State transitions and approval invariants

| Current | Allowed next (representative) | Condition |
|---|---|---|
| DRAFT | AWAITING_INPUT, AWAITING_APPROVAL, MANUAL_HANDOFF, FAILED, CANCELLED | Explicit selected job and reserved quota; safe unsupported-form handoff labeled incomplete |
| AWAITING_INPUT | DRAFT, CANCELLED | Authenticated task response or cancellation; no quota increment |
| AWAITING_APPROVAL | DRAFT, SUBMITTING, MANUAL_HANDOFF, REJECTED, CANCELLED | Edits invalidate approval; individual exact-payload authorization; manual handoff sends nothing |
| SUBMITTING | SUBMITTED, UNKNOWN, FAILED | Confirmed result, ambiguous outcome, or definitive pre-send failure |
| UNKNOWN | SUBMITTED, FAILED, AWAITING_APPROVAL | Reliable reconciliation; confirmed no send needed before fresh approval and retry |
| MANUAL_HANDOFF | SUBMITTED, CANCELLED | User/provider confirmation labeled; cancellation only of internal pending tracking, not reversal |
| FAILED | DRAFT or AWAITING_APPROVAL | Safe explicitly retriable case; new approval where needed |
| SUBMITTED / REJECTED / CANCELLED | Terminal for this workflow | New attempt requires deliberate policy-reviewed path; submitted duplicate blocked |

Approval record binds owner, application/job, destination and form version, reviewed payload version and canonical manifest hash, original resume and letter hashes, approval timestamp/expiry, decision and revocation version. Server derives manifest, not model or client. Approved approval expiry: 24 elapsed hours from explicit approval. Any material change or expired/revoked approval invalidates. Re-read job/form/policy before send. Before network action, submit adapter atomically checks approval, cancellation and current versions, reserves one attempt and transitions to in-flight; this is the last cancellable boundary. An in-flight attempt uses provider idempotency if supported; otherwise one send attempt, unknown outcome on ambiguity. If process crashes after marking in-flight but before external request, uncertainty is still reconciled rather than assuming no send. User must see UNKNOWN and any evidence. External exactly-once is not guaranteed. Never provide a generic retry button for an unknown send.

## 6. MCP contracts (logical tool names, not schemas or deployed endpoints)

All tools return typed structured result or error with tool/version, request ID, observation timestamp, source evidence refs, outcome and redacted diagnostic code. Authorization context injected by trusted caller/gateway, not model arguments. Tool names are logical aliases; actual Gateway target-prefixed names and protocol support must be verified. Input schemas forbid unknown parameters, enforce bounds, allowlisted source identities/destinations and SSRF-safe redirects. Use versioned schemas and contract tests.

| Tool | Inputs | Outputs | Access |
|---|---|---|---|
| search_web | Validated public query, page/cap, freshness hints | Search hit refs, source URL, pagination/coverage | Discovery read; licensed provider only; no profile PII |
| search_greenhouse | Known permitted board IDs, query/filter, page/cap | Posting records, provider IDs, date evidence, coverage | Discovery read; no employer credentials by default |
| search_lever | Known permitted site IDs, query/filter, page/cap | Posting records, provider IDs and coverage | Discovery read |
| search_company_jobs | Approved company catalog IDs, role terms, page/cap | Job observations and coverage | Discovery read; no unauthorized scraping |
| fetch_job | Scoped existing job ref or validated approved URL | Normalized content/evidence, availability, destination | Discovery/application read; untrusted text |
| verify_job_link | Scoped job ref and expected identity | Active/expired/unverified, canonical destination and evidence | Discovery read; HTTP status alone insufficient |
| inspect_application_form | Scoped application/job ref, permitted adapter | Form schema, required fields, conditional rules, unsupported capability | Application read; no candidate data sent before approval |
| submit_approved_application | Application ref, approval ref, attempt ref | Confirmation, definitive no-send failure or UNKNOWN | Restricted execution service only; not exposed to model as callable tool; server checks full policy |
| lookup_submission_status | Scoped application/attempt ref | Confirmed, definitively not submitted, unknown, evidence type | Restricted reconciliation read; authorized adapter only |

No arbitrary HTTP, browser control, shell, direct database writes, raw profile export or generic submission tool. Model may propose bounded read tool requests only where a node explicitly permits them; deterministic executor validates arguments. Submission tool invoked programmatically through the restricted MCP client/identity by JA-N12, never bound to the model. AgentCore Gateway target/identity segregation or separate gateways if necessary; same runtime deployment must not give inference nodes access to write capability. Validate independent adapter authorization even when gateway policy exists. Learn local MCP server + client and deploy narrow read Lambda targets or remote MCP server via Gateway; choose concrete topology after compatibility and price checks.

| Error category | Handling |
|---|---|
| INVALID_ARGUMENT / UNSUPPORTED | No automatic retry; validate or manual handoff |
| UNAUTHORIZED / POLICY_DENIED | Fail closed; no model override |
| NOT_FOUND / EXPIRED | Mark unavailable; no submission |
| RATE_LIMITED / TRANSIENT | Bounded retry with jitter for reads, respect Retry-After and remaining deadline |
| TIMEOUT / UNAVAILABLE | Partial search or visible recoverable error; external write timeout => UNKNOWN |
| BUDGET_EXCEEDED / CANCELLED | Stop optional work; preserve status and recovery |
| UNKNOWN_OUTCOME | Reconcile; never auto-retry external action |

Approved retry policy: up to 2 retry attempts after initial transient read call (3 total), capped jittered backoff and provider Retry-After; stop early on budget/deadline. Model malformed output gets one schema-correction attempt, then unresolved/visible failure; no endless agent loop. Source timeouts, concurrency and token limits benchmarked in staging.

## 7. Skills and model invocation

| Skill | Activating node | Context and output |
|---|---|---|
| job-discovery | JS-N02 | Public query/preferences → structured criteria; no unrestricted search |
| job-matching | JS-N07 / N09 | Job text + minimum verified skill facts → role/eligibility evidence, fit/gaps |
| application-form-analysis | JA-N04 / N05 | Form schema and question text → field semantics/conditions |
| candidate-answer-mapping | JA-N05 | Allowed verified facts + field constraints → proposed values, fact IDs, unresolved |
| cover-letter-writing | JA-N07 only on request | Approved facts/job → grounded draft, evidence |
| application-verification | JA-N08 optional quality check | Draft evidence → findings; deterministic validator remains final |

Load skill metadata at startup, full reviewed instructions only at eligible node, references on demand from bundled allowlist. No remote arbitrary skill download, no executable scripts in initial skills, no permission granted by skill metadata. Record exact versions in run metadata. Use structured Bedrock outputs with bounded schema validation and model-call attribution. Choose model by offline evaluation and Canada Central processing availability; no model family fixed yet. Guardrails inspect relevant untrusted inputs/outputs and redact/minimize context; structured outputs are validated, never assumed true. Domain validators independently enforce source evidence, exact candidate facts, approval, quota and tool permissions.

## 8. Observability and test traceability

Instrument request acceptance, outbox publish, queue dispatch, graph node, model call, MCP call, checkpoint, task/approval and submission attempt as spans or linked traces. Use correlation/run/thread IDs, node ID, tool name, model/skill version, durations, token usage, cost estimates, retry count, outcome and policy reason; no raw prompt, resume, form answer, screenshot or credential. Record wait duration separately from active execution, measure end-to-end queue latency and avoid high-cardinality metric dimensions. Example spans: api.accept_application → command.dispatch → graph.JA-N05 → model.map_fields → checkpoint.save → task.await_input. Resume uses linked trace; do not keep an active span open for days.

| Verification focus | Requirement references |
|---|---|
| Role/geography/freshness/duplicates, active links and partial failure | JS-003–014; EV-001–002 |
| User selection, quota and original resume | JA-001–005; EV-006,009 |
| Human interrupt and scoped reusable answers | JA-006–010; EV-004–005,009 |
| Exact approval, cancellation, duplicate and unknown send | JA-011–017; EV-007–009 |
| Tool injection, privacy and authorization | JS-015, JA-019; NFR-011–014; EV-007 |
| Cost, latency, telemetry and restore | NFR-001–008,010,015–020; EV-010 |

## 9. Open decisions and references

Approved on 2026-11-25: node and state contracts, REST interfaces, skill and MCP boundaries, independent guardrails, recovery design, 24-hour individual approval expiry, two retries after the initial transient read-only call, and initial LLM batches of up to 10 jobs / 15 questions. All other proposed details accepted subject to feasibility testing. Approved DynamoDB keys/access patterns/transactions and backup/deletion are in [data model v1.0](data-model.md); [threat model v1.0](../04-security/threat-model.md) specifies approved security boundaries. Signed URL revocation and 30-day backup retention remain blocking deployment gates. Checkpoint fencing, source catalog, licensed search, actual model and pricing, AgentCore invocation/checkpointer compatibility and region remain validation gates. No implementation, API schema, actual tool calls, model calls or test results yet.

References: [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts), [durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution), [graph API](https://docs.langchain.com/oss/python/langgraph/graph-api), [AgentCore Gateway MCP targets](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-MCPservers.html), [AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/), [Agent Skills](https://agentskills.io/specification). Framework capabilities do not imply this proposed design has been tested.
