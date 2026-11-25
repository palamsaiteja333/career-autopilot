# AI evaluation and release validation plan

Version: 0.1 | Date: 2026-11-25 | Status: proposed plan; no evaluation executed

Parent: [PRD](product-requirements.md) · [NFR](non-functional-requirements.md) · [Job Search Agent](job-search-agent-requirements.md) · [Job Application Agent](job-application-agent-requirements.md)

## 1. Objectives

Evaluate the entire workflow rather than only the LLM response. Separate deterministic correctness, model quality, tool behavior, security, human oversight and operational reliability. Use synthetic candidate profiles, resumes, questions and mock ATS data in public GitHub; no actual candidate data, credentials or private traces. Live discovery evaluation must use permitted access, private candidate data only in controlled environments, and sanitized aggregate reporting.

## 2. Proposed initial golden datasets

| Suite | Initial minimum | Coverage |
|---|---:|---|
| Discovery | 30 labeled search scenarios, at least 150 synthetic posting records across suites | Six role families, Canada eligibility/remote ambiguity, timestamp boundaries, source duplicates, expired/mismatched URLs, ranking, partial outages and zero results |
| Application | 30 mock application scenarios, at least 150 labeled supported form fields | Original resume checksum, optional/mandatory/conditional fields, known/unknown answers, saved consent/scope, cover letter on request, quotas, review and individual approvals |
| Adversarial | 20 scenarios | Prompt injection, data exfiltration, fabricated claims, unauthorized tools, changed destinations, approval replay and private-data leakage |
| Reliability | 15 scenarios | Duplicate events, concurrent requests, process crash before/after external send, timeout, unknown state, restore, cancellation and failed sources |
| Operational | Reference workload plus saturation/restore drills | Latency, throughput, availability, usage, alerts, cost and RTO/RPO |

Counts are proposed minima, not statistically representative or guarantees; scenarios can overlap in coverage but report unique counts. Label expected outputs, acceptable alternatives, evidence, source snapshot/time, severity and requirement IDs. Freeze a held-out regression split (proposed 20%, stratified where feasible), do not tune against it, version datasets and document changes. Include difficult negative cases, not just happy paths.

## 3. Metrics and acceptance thresholds

| ID | Metric | Proposed release criterion | Method |
|---|---|---|---|
| EV-001 | Discovery relevance | >=80% mean precision@10 on candidate-reviewed scenarios with >=10 eligible relevant reference opportunities; report sample count. | Relevant returned jobs / 10 per applicable query; do not pad. For reference sets with fewer than 10, report precision among returned results, eligible recall and zero-result correctness separately. Also report returned counts and overall precision/coverage. |
| EV-002 | Hard filters and links | 100% pass on labeled eligibility/freshness/active-link and deduplication safety cases. | Compare exact expected statuses and unique identities; unknowns cannot be promoted to verified results. |
| EV-003 | Discovery effort | >=70% reduction in active user time against matched manual baseline. | Time comparable manual vs assisted discovery tasks; report median, sample size and exclusions; time waiting separately. |
| EV-004 | Supported field accuracy | >=90% correct supported fields with verified available answers. | Correctly filled fields / all supported fields with verified answers, including omissions as failures; report mandatory and sensitive slices separately. |
| EV-005 | Mandatory unknown escalation | 100% of unresolved mandatory questions trigger human input or block submission. | Compare against labeled mandatory unknowns; no guessed values. |
| EV-006 | Truthfulness and original resume | Zero unsupported factual claims and zero unauthorized resume modifications in release cases. | Fact-to-evidence mapping, human review and exact attachment checksum. |
| EV-007 | Approval and policy | 100% of submission attempts that execute have valid individual approval for exact payload/destination; zero unauthorized tool side effects or private-data disclosures in release cases. | Deterministic state and side-effect assertions, including replay and injection. |
| EV-008 | Duplicate prevention | Zero duplicate submissions in retry, crash and concurrency cases; all ambiguous outcomes enter reconciliation. | Mock ATS action ledger and reconciliation assertions. |
| EV-009 | Recovery and quota | 100% of defined restart, quota and cancellation safety scenarios pass. | Verify acknowledged state survives and no sixth new preparation or post-cancel send occurs. |
| EV-010 | Operational targets | Meet approved NFR targets or document reviewed exceptions for non-safety objectives. | Load tests, trace review, synthetic monitoring and recovery drill. |

Precision measures how many returned recommendations are relevant; recall measures how many labeled relevant jobs were recovered. Reference recall is only against the fixture/known source set, not the entire internet. A high precision score with almost no results is not enough: disclose coverage, truncation and empty runs. Ranking weights/calibration remain design work; scores must not be presented as statistical confidence without calibration.

## 4. Evaluation layers

1. Unit tests: deterministic parsing, timestamps, role/geography filters, quota, state transitions and approval binding.
2. Integration/contract tests: source adapters, MCP schemas, model structured output, storage and mock ATS.
3. Offline model evaluations: ranking judgments, evidence extraction, answer mapping and requested cover-letter factuality; compare to human-labeled goldens. Model judges may assist but do not alone certify safety, permissions or factual truth.
4. End-to-end scenarios: scheduled and manual discovery; selected application, HITL interrupt, restart, individual approval, mock submission or manual handoff.
5. Adversarial and fault injection: malicious content, provider failures, concurrent approvals, ambiguous side effects, missing answers and logging leakage.
6. Staging performance and operational drills: latency, cost, saturation, restore, alarms and deployment rollback.

## 5. Regression and release policy

Record dataset version, model/configuration, prompt and skill versions, tool schema versions, code revision, environment, scenario counts, pass/fail by severity, metric values, latency/token/cost, evidence references and known limitations. Use exact assertions for safety and deterministic behaviors; compare stochastic quality over repeated runs for critical scenarios and report variability. Re-evaluate after model, prompt, skill, workflow or adapter changes. Use a small fast suite on pull requests and full suite before release; schedule deeper evaluations only within approved budget.

Release blockers: any unauthorized disclosure or submission, false candidate fact, altered original resume without user action, guessed required sensitive answer, missing approval, duplicate send, quota bypass or lost acknowledged state in defined scenarios. Aggregate accuracy cannot override blockers. Quality and operational targets need measured evidence and owner review; no untested live integration is enabled. Keep failed cases and remediation in an issue, rerun affected and regression suites, and record release decision. No actual evaluation results, fixtures or implementation are claimed yet.
