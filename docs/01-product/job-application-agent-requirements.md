# Job Application Agent — Functional requirements

Version: 1.2 | Date: 2026-11-25 | Status: agreed product defaults; implementation not started

Parent: [PRD](product-requirements.md) · [Functional requirements](functional-requirements.md) · [User stories](user-stories.md) · [CA-002](https://github.com/palamsaiteja333/career-autopilot/issues/2)

## 1. Purpose and scope

Prepare accurate applications for opportunities explicitly selected by the candidate, using the original approved resume and verified candidate information. Ask for missing answers, allow the candidate to save reusable answers by consent, and require individual review and approval before any authorized submission. Support mock ATS and manual handoff in the MVP; live submission is conditional on platform authorization.

## 2. Agreed defaults

| Setting | Default |
|---|---|
| Preparation trigger | Only jobs explicitly selected by the candidate |
| Resume | Original approved uploaded resume, unchanged |
| Cover letter | Generate only on explicit user request |
| Missing information | Ask the candidate; offer to save verified answers for future use |
| Submission approval | Review and explicitly approve each application individually |
| Daily preparation limit | 5 unique new application preparations per candidate |
| Notifications | In-app dashboard only |

No bulk or automatic preparation based on a matching score. No automatic resume tailoring, cover letter generation, email/SMS/Telegram notification, or batch approval. Settings may be revisited through future product decisions; individual approval and truthful answers are MVP safety invariants.

## 3. Functional requirements

| ID | Priority | Requirement | Observable acceptance criterion | Parent |
|---|---|---|---|---|
| JA-001 | Must | Start preparation only after authenticated explicit selection of a job. | Scheduled discovery and a high match score never start an application; repeated selection opens existing active draft. | FR-001, FR-008 |
| JA-002 | Must | Enforce at most five distinct new preparations per candidate per configured calendar day, including concurrent requests. | A sixth new preparation is blocked; retries, reopening, and resuming an existing draft do not consume new slots. | FR-008, FR-015 |
| JA-003 | Must | Revalidate selected job, destination and application status before preparation and again before submission. | Closed, mismatched or unverifiable destinations and previously submitted jobs cannot be automatically submitted; unavailable integrations offer safe handoff where appropriate. | FR-008, FR-012, FR-014 |
| JA-004 | Must | Retrieve the user-approved original resume version without rewriting, tailoring or modifying the uploaded file. | Attachment identity and checksum match the selected uploaded version; absent or outdated approval requests user selection. | FR-002, FR-008 |
| JA-005 | Must | Generate a cover letter only after explicit user request and ground factual claims in verified profile evidence. | No letter is generated on selection alone; a required letter prompts the user to request generation or supply their own before completion. | FR-008, FR-009 |
| JA-006 | Must | Identify supported application fields, conditional pages, required/optional status, validation constraints and declarations from permitted integrations or user-supplied form data. | Required and conditional questions are tracked; unsupported forms route to assisted/manual handoff without bypassing platform controls. | FR-009, FR-012, FR-013 |
| JA-007 | Must | Map known answers to current, verified candidate facts and approved answers with provenance and applicable scope. | Matching experience or contact facts populate supported fields; conflicting, stale or context-incompatible answers are not guessed. | FR-002, FR-009 |
| JA-008 | Must | Pause for missing, ambiguous, conflicting or sensitive information and display actionable questions in the dashboard. | Missing mandatory salary or work-authorization answers generate pending input; workflow cannot proceed past the required gate until resolved. | FR-009, FR-010, FR-015 |
| JA-009 | Must | Offer explicit, optional saving of user-confirmed answers with scope and provenance. | User may answer once or consent to reuse; employer-specific, sensitive or time-dependent answers are not silently generalized; later edits/deletion prevent stale reuse. | FR-002, FR-018 |
| JA-010 | Must | Persist draft and interruption state and resume authenticated workflows after restart. | A restarted service restores the same application, pending questions, approved resume version and progress without creating a duplicate draft. | FR-010, FR-014 |
| JA-011 | Must | Validate completeness, field formats, attachment constraints, factual grounding and required declarations before review. | Invalid or unanswered mandatory fields prevent ready-for-approval; optional unanswered fields may remain blank when allowed. | FR-008, FR-009, FR-011 |
| JA-012 | Must | Present an individual review of exact intended payload, resume version, optional cover letter, answers, declarations and destination; allow edits, rejection or cancellation. | User can inspect all submitted values before approval; an edited payload is revalidated. | FR-011, FR-015 |
| JA-013 | Must | Bind explicit individual approval to candidate, application, payload version, attachments and destination; invalidate on modification, expiry or revocation. | Approval for one job cannot authorize another; a changed field or destination requires a new approval; batch approval is unsupported. | FR-011, FR-016 |
| JA-014 | Must | Support approved mock ATS submission and manual handoff with clear outcome semantics. | Mock submit requires valid approval; manual handoff provides materials and destination, and is not marked submitted without candidate confirmation or reliable evidence. | FR-012, FR-015 |
| JA-015 | Should | Enable live submission only through a verified authorized adapter and valid approval; enforce domain, credential and action policies independent of the model. | Unauthorized adapter, CAPTCHA, unsupported login or permission failure routes to human/manual handoff, not circumvention. No live adapter is required for mock MVP. | FR-013, FR-016 |
| JA-016 | Must | Prevent duplicate external actions and reconcile ambiguous submission outcomes. | Concurrent approval requests or crash after send cannot produce blind resubmission; unknown outcome blocks another send until reconciled. | FR-014 |
| JA-017 | Must | Track application progress, outcomes, confirmation and user cancellation; distinguish external effects from internal state. | Dashboard distinguishes draft, awaiting input, awaiting approval, handoff, submitting, unknown, submitted, failed, rejected and cancelled; cancellation does not claim to undo completed external submission. | FR-015 |
| JA-018 | Must | Deliver dashboard-only notifications for pending questions, approval, quota, errors and outcomes. | Pending items remain visible after restart; repeated events do not duplicate notices; no email/SMS/Telegram notification is sent. | FR-015, FR-017 |
| JA-019 | Must | Protect candidate data and treat external content as untrusted. | Prompt injection cannot authorize resume disclosure, arbitrary uploads, false answers, or submission; sensitive facts are limited to explicitly permitted destinations. | FR-001, FR-016, FR-018 |
| JA-020 | Must | Maintain privacy-safe audit and operational evidence. | Record application ID, correlation ID, state transitions, version references, approval and submission outcomes, tool errors, latency and model cost estimates without raw private payloads in logs. | FR-017 |

## 4. Business rules and application lifecycle

Selection → quota and duplicate check → validate opportunity → load original approved resume/profile → inspect supported application questions → populate known answers → interrupt for unresolved questions or user-requested document preparation → validate → individual review → explicit approval → authorized submission or manual handoff → outcome/reconciliation → track.

### Daily quota

Proposed interpretation: count the first accepted preparation of each unique application in the candidate's configured local calendar day, not submissions or attempts. Reserve the slot atomically before work begins; accepted preparations count even if later cancelled or failed. Reopening/resuming the same draft, retries, and duplicate clicks do not consume another slot. A sixth new preparation is rejected with a visible quota notice; it is not silently queued or auto-started tomorrow. Existing drafts may still be reviewed, resumed or submitted with valid approval after the quota is reached. Default timezone: America/Toronto; use local calendar-day boundaries including 23/25-hour DST days, and UTC instants for stored events.

### Candidate facts and documents

The original resume is immutable for a preparation; user may explicitly select another approved original version, invalidating any previous approval. Do not infer legal status, sponsorship, credentials, compensation, demographic or other sensitive declarations from resume/context. Sensitive, legally significant or context-specific answers require direct confirmation when appropriate; optional voluntary self-identification is left blank or answered only at the user's direction. Offer save-for-future only with explicit consent and appropriate scope/validity; do not persist passwords or one-time codes as reusable answers. A required cover letter remains unresolved until the user requests one or supplies it. No fabrication or automatic tailoring. Before approval, external form discovery must be read-only or use authorized, non-transmitting draft operations; do not upload resume or send candidate data to an external destination before approval (including autosaving forms). If a destination cannot be safely inspected, use user-supplied questions/manual handoff.

### Approval and recovery

Approved expiry: individual approval is valid for at most 24 elapsed hours from its recorded grant time, unless revoked or invalidated earlier. Expiry is checked immediately before dispatch; renewal requires a fresh explicit individual approval.

Approval is not general delegation. Bind it to exact reviewed payload, attachment versions, employer/destination and application identity. Recheck policy, current job and approval immediately before sending. Rejection/cancellation before execution blocks sending. If a form changes or requires a new question, return to input/review. After uncertain external send, record unknown outcome and reconcile through reliable authorized evidence or human confirmation; retry only when safe and still authorized. Manual handoff is not submission. CAPTCHA and unsupported forms require human action.

## 5. Conceptual input/output contract (not API schema)

Input: candidate identity, explicit selected job ID and destination, current verified profile/version, approved original resume/version, application preferences and any existing draft. External forms and job content are untrusted.

Output: application ID, job ID, status, quota status, resume reference/checksum, optional cover letter reference, supported questions and answer provenance, unresolved questions, validation findings, reviewed payload version/destination, approval status, execution mode, outcome/confirmation reference, timeline and correlation ID. User-facing views require authorization; logs contain references and redacted metadata, not raw resume, answers or secrets.

## 6. User stories and acceptance scenarios

| ID | User story | Acceptance scenario | Requirements |
|---|---|---|---|
| JA-US-01 | I want to choose which jobs are prepared and control the workload. | A daily search returns ten jobs but starts none automatically; five selected preparations succeed and a sixth is blocked, including simultaneous requests. | JA-001–003 |
| JA-US-02 | I want my original resume used and a cover letter only when I ask. | The resume attachment matches its original checksum; no letter exists until requested; a required letter pauses the draft. | JA-004–005 |
| JA-US-03 | I want verified answers reused and missing information asked of me. | Known facts populate fields; an unknown mandatory answer creates a dashboard task; a saved answer is reused only if I consented and its scope is valid. | JA-006–010 |
| JA-US-04 | I want to review each application before anything is sent. | The agent displays exact materials and destination, accepts an individual approval, and requires reapproval after an edit. | JA-011–013 |
| JA-US-05 | I want safe application execution where supported. | Approved mock submission succeeds; unsupported live site produces manual handoff without a false submitted state or unauthorized action. | JA-014–015 |
| JA-US-06 | I want protection against duplicate submissions and lost progress. | Restart restores pending state; timeout after send becomes unknown; duplicate requests cannot resend until reconciliation. | JA-010, JA-016–017 |
| JA-US-07 | I want to see pending tasks and application progress in one place. | Dashboard displays questions, approval requests, quota and final outcomes; no external notification is sent. | JA-017–018 |
| JA-US-08 | I want my personal information and qualifications protected. | Malicious content cannot upload data or fabricate a claim; logs show correlation IDs without exposing private answers. | JA-007, JA-019–020 |

## 7. MVP acceptance checklist

- [ ] Explicit selection only; five-per-day quota, concurrent selections, duplicates, retries and day rollover covered.
- [ ] Original resume unchanged; missing resume and required cover letter cases covered; no automatic tailoring or letter generation.
- [ ] Supported form mapping, optional/mandatory and conditional questions, verified answer provenance, consent and stale-answer scenarios covered.
- [ ] Human interruption, restart/resume, individual approval, changed payload/destination, expiry, rejection and cancellation tested.
- [ ] Mock ATS and manual handoff end-to-end tested; live adapters disabled until permission verified.
- [ ] Crash before/after submission, ambiguous outcomes, duplicate actions and reconciliation tested.
- [ ] Dashboard-only notification persistence/deduplication and privacy-safe audit verified.
- [ ] PRD field accuracy, mandatory escalation, truthfulness and approval targets evaluated on synthetic test data; safety invariants are release blockers.

## 8. Decisions deferred

Answer retention/scope policy, form adapter contracts and authorization, live platform support, dashboard UX, document format, persistence, LangGraph graph/checkpoints, MCP tools/skills, AWS infrastructure, implementation and verification of approved latency/cost and operational SLOs. The quota accounting, safe pre-approval inspection and answer-scope rules above are proposed operational interpretations of agreed preferences, not measured behavior. No real resume, candidate answers, live applications, scheduled jobs or implementation code are included.
