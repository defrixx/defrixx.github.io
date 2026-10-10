---
title: "Review and Governance"
description: "Start with an architecture review or threat model. Use the relevant playbooks for release decisions and handling discovered vulnerabilities."
sidebar:
  order: 5
---
Start with an architecture review or threat model. Use the relevant playbooks for release decisions and handling discovered vulnerabilities.

| Task | Document | Review scope |
| --- | --- | --- |
| Review an architecture | [Architecture review](/en/review/architecture/checklist/) | Trust boundaries, data flows, critical components, and control applicability. Includes recording findings, residual risk decisions, and the final architecture review verdict. |
| Build a threat model | [Threat modeling](/en/review/threat-modeling/playbook/) | Assets, actors, entry points, and abuse scenarios for a system or change. Connects threats to controls, verification, owners, and unresolved questions. |
| Prepare a release | [Release governance](/en/review/release-governance/playbook/) | Protected branches and environments, CI/CD checks, deployment approvals, and release evidence. Covers blocking conditions, exceptions, risk acceptance, and escalation. |
| Manage vulnerabilities | [Vulnerability management](/en/review/vulnerability-management/playbook/) | Validation of vulnerability applicability, exploitability, and product impact; remediation priority and deadlines. Also covers release blocking, exceptions, reassessment, and closure evidence. |

## How to plan the review

- For a new service, start with architecture review to define system boundaries and the data flows under review. Continue with threat modeling to examine abuse scenarios within those boundaries.
- For a change to an existing service, select the affected parts of the architecture and threat model. Use the table above to reach the relevant document without repeating the whole section.
- Before a release, use release governance. If the task is to handle findings that already exist, start with vulnerability management.

## When to use other sections

For code, API, and web application reviews, use [application security](/en/application-security/overview/). Kubernetes and Vault reviews are covered in [platform security](/en/platform-security/overview/).

For an external researcher report, use the intake and coordinated-disclosure process in section 2.1 of [vulnerability management](/en/review/vulnerability-management/playbook/).
