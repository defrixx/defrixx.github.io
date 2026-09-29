# Review and Governance

Start with an architecture review or threat model. Use the relevant playbooks for release decisions and handling discovered vulnerabilities.

| Task | Document | Review scope |
| --- | --- | --- |
| Review an architecture | [Architecture review](./architecture/checklist.en.md) | System boundaries, data flows, and architectural decisions |
| Build a threat model | [Threat modeling](./threat-modeling/playbook.en.md) | Threat scenarios for a system or change |
| Prepare a release | [Release governance](./release-governance/playbook.en.md) | Release criteria and residual risk decisions |
| Manage vulnerabilities | [Vulnerability management](./vulnerability-management/playbook.en.md) | Triage, prioritization, and remediation tracking |

## How to plan the review

- For a new service, start with architecture review to define system boundaries and the data flows under review. Continue with threat modeling to examine abuse scenarios within those boundaries.
- For a change to an existing service, select the affected parts of the architecture and threat model. Use the table above to reach the relevant document without repeating the whole section.
- Before a release, use release governance. If the task is to handle findings that already exist, start with vulnerability management.

## When to use other sections

For code, API, and web application reviews, use [application security](../application-security/overview.en.md). Kubernetes and Vault reviews are covered in [platform security](../platform-security/overview.en.md).
