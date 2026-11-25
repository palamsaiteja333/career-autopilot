# Product vision

Status: initial baseline | 2026-11-25

## Problem
Job seekers spend time finding eligible roles, evaluating descriptions, repeating form answers, adapting resumes and tracking applications. Generic automation can waste effort on irrelevant roles or introduce incorrect claims and unauthorized actions.

## Vision
CareerAutopilot is a personal career workspace powered by specialized agents that discover opportunities and prepare high-quality applications while keeping the candidate in control. In the long term it can support professional networking, content and career development through reusable platform capabilities.

## Primary persona
A technical professional looking for AI engineering, applied AI, agentic systems and forward deployed engineering roles. The first release supports a single candidate with configurable location, remote eligibility, seniority and role preferences. Canada and Canada-eligible remote jobs are the initial search focus, not a hard-coded product constraint.

## Value proposition
Find fewer, better opportunities; prepare truthful applications faster; preserve user control and provide reliable status and evidence. Prioritize relevance and accuracy rather than application volume.

## Product principles
- The user owns their candidate profile and approves consequential actions.
- No unsupported qualifications, eligibility assertions or guessed mandatory answers.
- Public read access is not equivalent to permission to submit or automate a website.
- Unknown eligibility or submission status remains explicitly unknown until resolved.
- New agents reuse shared identity, skills, tools, workflows, approvals and telemetry without requiring an autonomous supervisor initially.
- Design for a real deployed application, while keeping the initial release single-user and cost-conscious.

## Delivery sequence
1. Discovery: search, normalize, deduplicate, score and track.
2. Applications: grounded materials, form mapping, durable approvals, manual handoff and authorized integrations.
3. Future: professional networking, content and interview preparation, subject to permissions.

Discovery and application assistance together constitute the MVP. A live automated submission adapter is conditional on a verified permission model; a mock ATS and assisted handoff are sufficient to demonstrate the initial workflow safely.
