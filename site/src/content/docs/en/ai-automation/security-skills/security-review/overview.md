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

Threat modeling, vulnerability discovery, reachability and prerequisite checks, attack analysis, and prioritized findings. The optional `scripts/pr_context.py` records local Git context; it does not scan for vulnerabilities. It requires Python 3.9+ and Git.

The helper also needs POSIX no-follow output support. Its PR comparison uses merge-base-to-head semantics; uncommitted and untracked content is recorded as dirty state but is not included in that diff. Review selected working-tree changes separately. Missing or ambiguous history produces an incomplete result rather than a fallback assessment of the current directory.

## Example request

> Use security-review on this PR with the supplied base/head commits. Distinguish introduced issues from existing ones. Report confirmed findings, hypotheses, evidence, and untested areas without changing the code.

## Expected result and limits

Findings include prerequisites, impact, confidence, remediation, and fix-verification criteria. Scanner output stays a hypothesis until validated. Review alone does not authorize code fixes, external attacks, PR comments, or publication.

The report includes a flow coverage table: entry point, sensitive operation, protections checked and their observed outcomes, evidence, and untested conditions. Static analysis, executed checks, and checks using mocked components are labeled separately. Keep the table even when no vulnerabilities are confirmed: it records assessed scope and remaining gaps, not a security guarantee.

Classify a finding as introduced or pre-existing only after comparing the same issue at recorded revisions. With a single snapshot, historical provenance remains unknown; a content hash does not establish age. Remediation must preserve the stated security invariant. Keep suggestions, candidate patches, and changes observed in the target distinct.

## Files and verification

Instructions and references are bundled with the skill. Use the [report template](https://github.com/defrixx/Product-security-skills/blob/main/skills/security-review/assets/review-report.md) to record results. [Tests](https://github.com/defrixx/Product-security-skills/tree/main/tests) are maintained in the source repository.

## Related playbooks

- [Secure coding and code review](/en/application-security/secure-coding/code-review/playbook/)
- [Threat modeling](/en/review/threat-modeling/playbook/)
- [Vulnerability management](/en/review/vulnerability-management/playbook/)

## Standalone and combined use

The skill works without sibling packages. In the [combined workflow](/en/ai-automation/security-skills/workflow/overview/), it performs a selected stage while preserving finding IDs, revisions, and evidence. The task defines authorized actions; preceding outputs do not automatically expand that scope.
