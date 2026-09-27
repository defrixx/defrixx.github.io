# Secure development

Use while implementing code, configuration, or infrastructure changes. The assistant selects requirements against the actual stack and trust model, implements within scope, and checks the result.

[View skill source](https://github.com/defrixx/Product-security-skills/tree/main/skills/secure-development) | [Installation instructions](../overview.en.md)

## Inputs

Provide the task, target files or repository, stack versions, exposure, data sensitivity, and existing policies. Missing context should remain an explicit assumption.

## Coverage and dependencies

Authentication and authorization, input handling, files, secrets, cryptography, APIs, dependencies, deployment, CI/CD, and Kubernetes. Includes profiles for Python/FastAPI, TypeScript/Next.js, and Docker Compose/BuildKit.

## Example request

> Use secure-development to implement this upload endpoint. Apply the requirements relevant to our stack and trust model. Report the requirement IDs, changes, positive and negative checks, and remaining gaps.

## Expected result and limits

Changed code or an explicitly labeled candidate implementation, applied requirement IDs, verification evidence, exceptions, and unresolved conditions. Align the requirements with the project's policies.

## Files and verification

Instructions and references are bundled with the skill. Use the [report template](https://github.com/defrixx/Product-security-skills/blob/main/skills/secure-development/assets/development-report.md) to record results. [Tests](https://github.com/defrixx/Product-security-skills/tree/main/tests) are maintained in the source repository.

## Related playbooks

- [Secure coding and code review](../../../application-security/secure-coding/code-review/playbook.en.md)
- [Secure AI-assisted development](../../../ai-security/ai-assisted-development/playbook.en.md)
- [Kubernetes cluster review](../../../platform-security/kubernetes/cluster-security-review/playbook.en.md)
