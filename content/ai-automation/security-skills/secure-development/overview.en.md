# Secure development

Use while implementing code, configuration, or infrastructure changes. The assistant selects requirements against the actual stack and trust model, implements within scope, and checks the result.

[View skill source](https://github.com/defrixx/Product-security-skills/tree/main/skills/secure-development) | [Installation instructions](../overview.en.md)

## Inputs

Provide the task, target files or repository, stack versions, exposure, data sensitivity, and existing policies. Missing context should remain an explicit assumption.

## Coverage and dependencies

Authentication and authorization, input handling, files, secrets, cryptography, APIs, dependencies, deployment, CI/CD, and Kubernetes. The catalog also covers outbound requests and SSRF, business logic, webhooks and events, key lifecycle, and OAuth/OIDC/JWT. Includes profiles for Python/FastAPI, TypeScript/Next.js, and Docker Compose/BuildKit.

Start with [requirement selection by change](https://github.com/defrixx/Product-security-skills/blob/main/skills/secure-development/references/requirements-index.md#select-by-change): file uploads, a new API, authorization changes, external URL handling, or protected-response caching. Applicability follows actual data flows and trust boundaries; one task may span several topics. Record unverified conditions separately: a passing check for one condition does not establish coverage of an entire topic.

## Example request

> Use secure-development to implement this upload endpoint. Apply the requirements relevant to our stack and trust model. Report the requirement IDs, changes, positive and negative checks, and remaining gaps.

## Expected result and limits

Changed code or an explicitly labeled candidate implementation, applied requirement IDs, verification evidence, exceptions, and unresolved conditions. Align the requirements with the project's policies.

## Files and verification

Instructions and references are bundled with the skill. Use the [report template](https://github.com/defrixx/Product-security-skills/blob/main/skills/secure-development/assets/development-report.md) to record results. [Tests](https://github.com/defrixx/Product-security-skills/tree/main/tests) are maintained in the source repository.

The [requirement coverage manifest](https://github.com/defrixx/Product-security-skills/blob/main/tests/requirement_coverage.json) and [integration check documentation](https://github.com/defrixx/Product-security-skills/blob/main/tests/integration/README.md) describe tested conditions and coverage gaps. Checks against synthetic applications provide evidence for individual conditions, not assurance of a target project's security. Integration checks run separately and require Docker and fixture dependencies.

## Related playbooks

- [Secure coding and code review](../../../application-security/secure-coding/code-review/playbook.en.md)
- [Secure AI-assisted development](../../../ai-security/ai-assisted-development/playbook.en.md)
- [Kubernetes cluster review](../../../platform-security/kubernetes/cluster-security-review/playbook.en.md)
