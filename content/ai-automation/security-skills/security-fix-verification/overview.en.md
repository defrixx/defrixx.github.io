# Security fix verification

The `security-fix-verification` skill checks a specified repair in a selected revision or candidate patch. It works independently: a defect description and available evidence are sufficient inputs; a report from another skill is not required.

[View skill source](https://github.com/defrixx/Product-security-skills/tree/main/skills/security-fix-verification) | [Installation instructions](../overview.en.md)

## Inputs

Provide finding IDs, the defect, expected secure behavior, and the original revision and evidence when available. Pin the checked revision, local changes, candidate or applied state, and verification scope. If the original version is unavailable, a before-fix reproduction cannot be claimed.

## Workflow

The assistant examines the repair and surrounding data flow: attacker control, entry point, guards before the sensitive operation, and possible impact. Expected and observed outcomes are compared for three groups of cases per finding:

- the original exploit or violated property;
- bypass paths and other affected handlers sharing the root cause;
- allowed operations that must continue to work.

A complete static trace can establish a code property with a stated rationale. Conclusions that depend on browser, deployment, network, or concurrency behavior need corresponding runtime checks. Component substitutions, skipped checks, and environment differences are explicit.

For AI-related repairs, test the boundary where a tool performs the action, including a direct unauthorized tool proposal and an allowed operation. Check authorization at tool execution, independently of the model's response to the original prompt. For integrity repairs, inspect affected dispatch, retry, and fallback paths and verify that rejected bytes never reach the transport. Revalidate snapshot identity after working-tree drift and invalidate evidence affected by the change.

## Per-finding verdict

| Status | Meaning |
| --- | --- |
| `fixed` | All selected affected paths and necessary cases establish the repair; allowed behavior holds and no material gap remains for the stated claim. |
| `partially_fixed` | Part of the repair is established, but another required path remains vulnerable or allowed behavior regresses. |
| `not_fixed` | The original defect or equivalent in-scope bypass remains, without an established complete repair of a distinct required portion. |
| `inconclusive` | Missing or conflicting evidence prevents the necessary conclusion. |

A repair verdict needs results for the original defect, applicable bypass paths, and allowed operations. Use `inconclusive` when necessary cases remain untested; for `partially_fixed`, identify the established portion and the remaining defect or regression in allowed behavior.

## Bypass matrix and stateful effects

Build one matrix row for each actual path with a distinct guard: finding ID, entry/input representation, actor and prerequisites, guard and repair location, allowed control, forbidden effect, original/patched observations, evidence, and next action. Select alternate routes, methods, create/update/bulk/import/export, shared callers, encodings, cache hits, jobs, redirects, retries, and fallback only where relevant to the defective control. A shared sink alone does not establish shared protection.

For lifecycle repairs, declare the effective transition boundary and exercise warm state, revocation/transfer/deletion, delayed consumption, restart, and replay as applicable. For repeated effects, interrupt around independent commits and inspect both caller state and recipient effects after retry. Observe the effect boundary, not merely an error response. Sequential cases and mocks retain their evidence limits.

A necessary untested path leaves the bounded claim inconclusive; an observed bypass is evaluated under the existing verdict rules. Record policy/configuration and state dependencies so affected cases can be rerun after drift.

> Use security-fix-verification on F-007's download repair. Build a bypass matrix for direct download, export, and the existing worker; check allowed owner access, revocation with warm cache, and replay after restart. Report actual data and durable effects, retaining unknown cases explicitly.

## Example request

> Use security-fix-verification to check F-007 at this revision. Check the original failure, relevant bypass paths, and allowed operations. Preserve the finding ID and record evidence and untested conditions. Do not change code.

## Expected result

The [report](https://github.com/defrixx/Product-security-skills/blob/main/skills/security-fix-verification/assets/verification-report.md) includes per-finding verdicts, revisions, a case matrix, observations, and remaining checks. The report records verification results and application to the target separately. Finding history preserves the original assessment and subsequent remediation.

The skill works independently from a defect description and available evidence. In the [combined workflow](../workflow/overview.en.md), it accepts results from preceding stages. Include code changes and production access explicitly in the task.

Before delivery, reconcile verdicts with recorded cases and counts at the checked revision. Keep `partially_fixed` when a relevant bypass remains alongside an established portion of the repair. Candidate state changes only after application to the named target is observed. Record who implemented and verified the change; label self-verification when the same assistant performed both.

## Related material

- [Secure development](../secure-development/overview.en.md)
- [Report triage](../security-report-triage/overview.en.md)
- [Vulnerability management](../../../review/vulnerability-management/playbook.en.md)

## Choose another task

Each skill handles an independent task. Choose the one you need:

- [Secure development](../secure-development/overview.en.md)
- [Security review](../security-review/overview.en.md)
- [Report triage](../security-report-triage/overview.en.md)
- [Sensitive data cleanup](../sensitive-data-cleanup/overview.en.md)
