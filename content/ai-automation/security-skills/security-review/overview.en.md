# Security review

Use for a security assessment of a pull request or repository. The workflow traces data across trust boundaries, validates hypotheses, assesses impact, and prepares a remediation report.

[View skill source](https://github.com/defrixx/Product-security-skills/tree/main/skills/security-review) | [Installation instructions](../overview.en.md)

## Inputs

Provide exact base/head revisions for a PR, or a repository revision and working-tree state. Define included components, exclusions, and available configuration and runtime evidence.

## Coverage and dependencies

Threat modeling, vulnerability discovery, reachability and prerequisite checks, attack analysis, and prioritized findings. The optional `scripts/pr_context.py` records local Git context; it does not scan for vulnerabilities. It requires Python 3.9+ and Git.

## Example request

> Use security-review on this PR with the supplied base/head commits. Distinguish introduced issues from existing ones. Report confirmed findings, hypotheses, evidence, and untested areas without changing the code.

## Expected result and limits

Findings include prerequisites, impact, confidence, remediation, and fix-verification criteria. Scanner output stays a hypothesis until validated. Review alone does not authorize code fixes, external attacks, PR comments, or publication.

## Files and verification

Instructions and references are bundled with the skill. Use the [report template](https://github.com/defrixx/Product-security-skills/blob/main/skills/security-review/assets/review-report.md) to record results. [Tests](https://github.com/defrixx/Product-security-skills/tree/main/tests) are maintained in the source repository.

## Related playbooks

- [Secure coding and code review](../../../application-security/secure-coding/code-review/playbook.en.md)
- [Threat modeling](../../../review/threat-modeling/playbook.en.md)
- [Vulnerability management](../../../review/vulnerability-management/playbook.en.md)
