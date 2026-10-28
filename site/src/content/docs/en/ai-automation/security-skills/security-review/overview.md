---
title: "Security review"
description: "Use for a security assessment of a pull request or repository. The workflow traces data across trust boundaries, validates hypotheses, assesses impact, and prepares a remediatio..."
sidebar:
  order: 30
---
Use for a security assessment of a pull request or repository. The workflow traces data across trust boundaries, validates hypotheses, assesses impact, and prepares a remediation report.

[View skill source](https://github.com/defrixx/Product-security-skills/tree/main/skills/security-review) | [Installation instructions](/en/ai-automation/security-skills/overview/)

## Inputs

Provide exact base/head revisions for a PR, or a repository revision and working-tree state. Define included components, exclusions, and available configuration and runtime evidence.

## Coverage and dependencies

Threat modeling, vulnerability discovery, reachability and prerequisite checks, attack analysis, and prioritized findings. The optional `scripts/pr_context.py` records local Git context for the assistant's subsequent code analysis. It requires Python 3.9+ and Git.

The helper also needs POSIX no-follow output support. Its PR comparison uses merge-base-to-head semantics; uncommitted and untracked content is recorded as dirty state but is not included in that diff. Review selected working-tree changes separately. Missing or ambiguous history produces an incomplete result rather than a fallback assessment of the current directory.

## Architecture, change impact, and decisive checks

Select architecture profiles from observed interfaces and actors: local CLI/desktop, public API, hosted multi-user service, webhook/worker, or agent/tool workflow. Combine profiles for hybrid systems. Profiles guide investigation of the product's actual components; approved project policies determine corporate requirements.

For a PR, compare the old and new actor-to-effect paths, including identity, parsing, guards, configuration, and consumers. An unchanged privileged helper can become newly exposed through a new route. Record the changed guarantee and comparison evidence before assigning introduced, pre-existing, or unknown provenance.

For business logic, identify the authoritative state, permitted transition, and durable effect. Mark invariants as specified, inferred, or unresolved. Investigate client-controlled values, skipped steps, partial updates, replay, stale permissions, and ambiguous outcomes. Distinguish memory data races, logic races, and TOCTOU; inspect actual atomicity and independent commits. Concurrency checks use controlled interleavings and count durable effects, alongside an allowed control.

Choose complementary analyzers from the actual languages, lockfiles, and deployment artifacts. Record versions and rules, inspect hooks/plugins and execution effects, and use authorized isolated checks. Validate scanner signals in code context and record analysis results separately from execution errors. Include analyzer installation and transmission of source or package inventories explicitly in the task scope.

When classification is needed, verify that the root cause matches the selected CWE definition and name the OWASP edition. CVSS v4.0 scores require a verified calculator, vector, scenario, and metric rationale; an uncomputed score stays explicit. Severity, confidence, and remediation priority remain separate, and release thresholds require authorized project policy.

Select decisive checks by mechanism: check whether the forbidden effect occurs at the relevant file, network, data, or tool boundary, and show that an allowed operation succeeds. For stateful paths, include revocation, delayed work, restart, and repeated effects as applicable. Record expected/observed outcomes and what would leave the result inconclusive.

> Use security-review on this PR that exposes a shared export helper through a new API. Compare base/head authorization guarantees, inspect alternate callers and cached exports after revocation, and select decisive checks. Separate confirmed findings from hypotheses and report CWE/CVSS only where supported.

## Example request

> Use security-review on this PR with the supplied base/head commits. Distinguish introduced issues from existing ones. Report confirmed findings, hypotheses, evidence, and untested areas without changing the code.

## Expected result

Findings include prerequisites, impact, confidence, remediation, and fix-verification criteria. The assistant validates scanner signals against code and available execution evidence. Review delivers a report; fixes, external checks, PR comments, and publication follow an explicitly defined action scope.

The report includes a flow coverage table: entry point, sensitive operation, protections checked and their observed outcomes, evidence, and untested conditions. Static analysis, executed checks, and checks using mocked components are labeled separately. Keep the table even when no vulnerabilities are confirmed: it records assessed scope and remaining gaps.

Classify a finding as introduced or pre-existing only after comparing the same issue at recorded revisions. Use change history to establish when an issue arose and content hashes to compare snapshot contents. Remediation must preserve the stated security invariant. Keep suggestions, candidate patches, and changes observed in the target distinct.

## Files and verification

Instructions and references are bundled with the skill. Use the [report template](https://github.com/defrixx/Product-security-skills/blob/main/skills/security-review/assets/review-report.md) to record results. [Tests](https://github.com/defrixx/Product-security-skills/tree/main/tests) are maintained in Product-security-skills.

## Related playbooks

- [Secure coding and code review](/en/application-security/secure-coding/code-review/playbook/)
- [Threat modeling](/en/review/threat-modeling/playbook/)
- [Vulnerability management](/en/review/vulnerability-management/playbook/)

## Standalone and combined use

The skill includes everything needed for standalone use. For a multi-stage task, use the [combined workflow](/en/ai-automation/security-skills/workflow/overview/): select the authorized actions and preserve finding IDs, revisions, and evidence when passing results forward.

## Choose another task

Each skill handles an independent task. Choose the one you need:

- [Secure development](/en/ai-automation/security-skills/secure-development/overview/)
- [Fix verification](/en/ai-automation/security-skills/security-fix-verification/overview/)
- [Report triage](/en/ai-automation/security-skills/security-report-triage/overview/)
- [Sensitive data cleanup](/en/ai-automation/security-skills/sensitive-data-cleanup/overview/)
