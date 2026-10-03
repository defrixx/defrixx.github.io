# Combined skill workflow

Each of the five skills works independently. For an end-to-end task, combine report triage or code review, implementation, fix verification, and optional cleanup of selected delivery material.

This is an assistant workflow with compatible stage outputs. There is no separate automation engine or requirement to run every skill. [prompt-integrity](../../prompt-integrity/overview.en.md) integrates separately with an application and does not orchestrate this workflow.

## Choose the stages

| Stage task | Skill | Output passed forward |
| --- | --- | --- |
| Interpret an existing scanner report | [security-report-triage](../security-report-triage/overview.en.md) | Accounted raw signals, findings, evidence, and an action queue. |
| Assess a PR or repository | [security-review](../security-review/overview.en.md) | Confirmed findings, hypotheses, and repair criteria. |
| Implement selected repairs | [secure-development](../secure-development/overview.en.md) | Candidate or applied changes, the resulting revision, and check results. |
| Verify specified repairs | [security-fix-verification](../security-fix-verification/overview.en.md) | Per-finding verdicts covering original, bypass, and allowed cases. |
| Prepare selected material for sharing | [sensitive-data-cleanup](../sensitive-data-cleanup/overview.en.md) | A separate processed copy and a report of replacements, omissions, and limits. |

Report triage and code review are alternative entry points. You can start directly with implementation of a known finding or verification of an existing repair. Delivery cleanup is optional and does not change the original report's evidence.

## Passing results between stages

The [finding handoff contract](https://github.com/defrixx/Product-security-skills/blob/main/skills/security-report-triage/references/handoff-contract.md) is bundled as a local copy in each new skill. Equivalent fields in an ordinary report are sufficient for manual work; JSON is optional.

Stages preserve the origin assessment ID together with the finding ID, evidence references, revision and local changes, task scope, assumptions, and limits. Merged findings retain old IDs as aliases; split findings link their new IDs to the original.

| Field | What it records |
| --- | --- |
| `assessment_status` | Confirmation, hypothesis, or disproof at the original revision. |
| `severity` and `confidence` | Impact and evidence confidence independently. |
| `implementation_state` | Unknown, not started, candidate, or applied repair. |
| `verification_status` | Not checked, or a `fixed`, `partially_fixed`, `not_fixed`, or `inconclusive` verdict at the checked revision. |

An applied change does not automatically become `fixed`. A confirmed vulnerability at the old revision remains in history after successful remediation. Missing information means unknown, not passed.

The standalone report templates share an action ledger. Carry it forward with the original finding IDs, historical assessments, evidence, implementation state, verification verdict, and remaining work. Lead the final report with unresolved actions; producing a patch does not close a finding. Record self-verification only when the same assistant actually implemented and checked the change.

## Example combined task

> Use security-report-triage on the attached SARIF and current revision. Use secure-development to repair confirmed findings in the agreed components, then verify them with security-fix-verification. Preserve IDs, original evidence, and separate assessment, implementation, and verification statuses. Perform changes and checks locally; record untested conditions in the final report.

For code assessment without an existing report, replace the first stage with `security-review`. Explicitly add `sensitive-data-cleanup` for selected final material when needed.

## Resumption and task boundaries

Within an already authorized combined task, the assistant proceeds through selected stages without requesting permission again for each step. Standalone triage or verification does not automatically authorize implementation. Publication, external writes, and installation are outside the default workflow.

On resumption, compare input fingerprints, revisions, working snapshot, scope, and completed stages. Recheck affected evidence after drift. Resolve contradictions using revision-specific observations or retain an explicit inconclusive state. Implementation and verification by one assistant are labeled self-verification.

## Validation in the source project

The repository includes structural checks for standalone packages, helper and handoff-contract tests, and synthetic combined-workflow examples. The regression runner also discovers the separate `evals/tests/` suite without a model server. Optional [behavioral evaluations](https://github.com/defrixx/Product-security-skills/blob/main/evals/README.md) compare selected synthetic scenarios with and without skill instructions. Harness success does not establish model compliance or the reliability of assistant decisions on arbitrary projects. Coverage and limits are described in the [test guide](https://github.com/defrixx/Product-security-skills/blob/main/tests/README.md); application integration checks run separately. Evaluation tools and local artifacts are not part of copied skills.
