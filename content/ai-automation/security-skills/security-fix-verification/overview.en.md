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

For AI-related repairs, test the boundary where a tool performs the action, including a direct unauthorized tool proposal and an allowed operation. A model refusing the original prompt does not establish that tool authorization is repaired. For integrity repairs, inspect affected dispatch, retry, and fallback paths and verify that rejected bytes never reach the transport. Revalidate snapshot identity after working-tree drift and invalidate evidence affected by the change.

## Per-finding verdict

| Status | Meaning |
| --- | --- |
| `fixed` | All selected affected paths and necessary cases establish the repair; allowed behavior holds and no material gap remains for the stated claim. |
| `partially_fixed` | Part of the repair is established, but another required path remains vulnerable or allowed behavior regresses. |
| `not_fixed` | The original defect or equivalent in-scope bypass remains, without an established complete repair of a distinct required portion. |
| `inconclusive` | Missing or conflicting evidence prevents the necessary conclusion. |

Unknown coverage alone means insufficient evidence, not partial repair. An absent scanner signal, a closed ticket, or a test that failed to start does not prove remediation. Denying every operation is not a repair when allowed behavior must be preserved.

## Example request

> Use security-fix-verification to check F-007 at this revision. Check the original failure, relevant bypass paths, and allowed operations. Preserve the finding ID and record evidence and untested conditions. Do not change code.

## Expected result and limits

The [report](https://github.com/defrixx/Product-security-skills/blob/main/skills/security-fix-verification/assets/verification-report.md) includes per-finding verdicts, revisions, a case matrix, observations, and remaining checks. A successfully verified candidate remains a candidate; verification does not mean it was applied. Historical confirmation at the old revision remains in the record after remediation.

The skill needs no sibling skills and does not itself authorize code changes or production access. In the [combined workflow](../workflow/overview.en.md), it accepts results from preceding stages. Implementation and verification by the same assistant are labeled self-verification.

Before delivery, reconcile verdicts with recorded cases and counts at the checked revision. Keep `partially_fixed` when a relevant bypass remains alongside an established portion of the repair. Candidate state changes only after application to the named target is observed. Label self-verification only when the checking assistant actually implemented the assessed change; a supplied patch or fixture does not establish authorship.

## Related material

- [Secure development](../secure-development/overview.en.md)
- [Report triage](../security-report-triage/overview.en.md)
- [Vulnerability management](../../../review/vulnerability-management/playbook.en.md)
