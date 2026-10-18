# Secure development

Use while implementing code, configuration, or infrastructure changes. The assistant selects requirements against the actual stack and trust model, implements within scope, and checks the result.

[View skill source](https://github.com/defrixx/Product-security-skills/tree/main/skills/secure-development) | [Installation instructions](../overview.en.md)

## Inputs

Provide the task, target files or repository, stack versions, exposure, data sensitivity, and existing policies. Missing context should remain an explicit assumption.

## Coverage and dependencies

Authentication and authorization, input handling, files, secrets, cryptography, APIs, dependencies, deployment, CI/CD, and Kubernetes. The catalog also covers outbound requests and SSRF, business logic, webhooks and events, key lifecycle, and OAuth/OIDC/JWT. Includes profiles for Python/FastAPI, TypeScript/Next.js, and Docker Compose/BuildKit.

Start with [requirement selection by change](https://github.com/defrixx/Product-security-skills/blob/main/skills/secure-development/references/requirements-index.md#select-by-change): file uploads, a new API, authorization changes, external URL handling, or protected-response caching. Applicability follows actual data flows and trust boundaries; one task may span several topics. Record results for each selected condition, distinguishing completed and remaining checks.

## Architecture and lifecycle selection

Architecture profiles select existing requirement IDs for local CLI/desktop, public API, hosted multi-user, webhook/worker, and agent/tool boundaries. Combine relevant profiles; do not introduce multi-user login or distributed infrastructure merely to satisfy a checklist. Profiles guide selection from existing requirements; align the proposed acceptance baseline with project policies.

For access changes, declare when revocation, transfer, unpublishing, or deletion becomes effective. Select a sequence such as allowed read, warm cache or captured job, transition, read/execute/replay, then restart and repeat. Distinguish authorization at enqueue, execution, artifact creation, and download. Inspect actual data and durable effects, and check newly authorized access. Do not assume instantaneous revocation or infer concurrent guarantees from sequential tests.

For recovery, identify independent commits for reservation, recipient effect, and caller completion. Select interruptions around relevant commits, reopen durable state, and retry with the same scoped operation identity. Check duplicate attempts, payload mismatch, cancellation, and ambiguous outcomes where present. A local rollback does not undo an external effect; define reconciliation or an explicit unresolved state using the target's actual storage/provider semantics.

> Use secure-development to implement an export job with revocable access. Select controls for our API and worker architecture, state the effective revocation contract, and verify cached downloads, delayed execution, and retry after recipient commit without duplicating the effect.

## Example request

> Use secure-development to implement this upload endpoint. Apply the requirements relevant to our stack and trust model. Report the requirement IDs, changes, positive and negative checks, and remaining gaps.

## Expected result

Changed code or an explicitly labeled candidate implementation, applied requirement IDs, verification evidence, exceptions, and unresolved conditions. Align the requirements with the project's policies.

Explain non-applicability from the actual threat model; reserve exceptions for applicable controls deliberately left unmet. Requirements marked MUST form a proposed acceptance baseline; the project team determines its adoption and corporate-policy status. Verify version-dependent settings against current primary documentation for the target stack and label unavailable verification explicitly.

Before delivery, match each verified condition to evidence for that exact property at the reported revision. For a database query, check lookup scope, input validation, and tenant membership separately. Distinguish testing a candidate patch, applying it to the target, and deployment in the report, linking each stage to its observed result.

## Files and verification

Instructions and references are bundled with the skill. Use the [report template](https://github.com/defrixx/Product-security-skills/blob/main/skills/secure-development/assets/development-report.md) to record results. [Tests](https://github.com/defrixx/Product-security-skills/tree/main/tests) are maintained in Product-security-skills.

The [requirement coverage manifest](https://github.com/defrixx/Product-security-skills/blob/main/tests/requirement_coverage.json) and [integration check documentation](https://github.com/defrixx/Product-security-skills/blob/main/tests/integration/README.md) describe tested conditions and coverage gaps. Integration checks run separately and require Docker and fixture dependencies.

## Related playbooks

- [Secure coding and code review](../../../application-security/secure-coding/code-review/playbook.en.md)
- [Secure AI-assisted development](../../../ai-security/ai-assisted-development/playbook.en.md)
- [Kubernetes cluster review](../../../platform-security/kubernetes/cluster-security-review/playbook.en.md)

## Standalone and combined use

The skill includes everything needed for standalone use. For a multi-stage task, use the [combined workflow](../workflow/overview.en.md): select the authorized actions and preserve finding IDs, revisions, and evidence when passing results forward.

## Choose another task

Each skill handles an independent task. Choose the one you need:

- [Security review](../security-review/overview.en.md)
- [Fix verification](../security-fix-verification/overview.en.md)
- [Report triage](../security-report-triage/overview.en.md)
- [Sensitive data cleanup](../sensitive-data-cleanup/overview.en.md)
