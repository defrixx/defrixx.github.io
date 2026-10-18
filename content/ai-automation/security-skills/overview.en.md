# Security Skills and Tools

We develop Product Security Skills alongside the playbooks to help apply security requirements during development, review, report triage, fix verification, and preparation of material for sharing. The packages include assistant instructions, reference material, report templates, and local helpers for selected operations.

Five standalone skills can be used individually or combined in a [shared workflow](workflow/overview.en.md). The separate [prompt-integrity tool](../prompt-integrity/overview.en.md) integrates with an application to check static instruction integrity before model dispatch. The separate [model-security-eval tool](../model-security-eval/overview.en.md) checks local model behavior after updates and provides a blocking CI verdict. [prompt-guard](../prompt-guard/overview.en.md) checks untrusted input context and model outputs with separate policies, applies authorized replacements and validates structured responses and tool arguments before release or execution.

| Task | Skill | Result |
| --- | --- | --- |
| Write or change code | [Secure development](secure-development/overview.en.md) | Changed code or an explicitly labeled candidate implementation, applied requirement IDs, and verification evidence. The report separately records exceptions, assumptions, and conditions that could not be verified. |
| Assess a PR or repository | [Security review](security-review/overview.en.md) | Findings with exploitation prerequisites, impact, confidence, and fix-verification criteria. A coverage table separates confirmed results from hypotheses and untested areas, even when no vulnerabilities are found. |
| Prepare a folder for sharing | [Sensitive data cleanup](sensitive-data-cleanup/overview.en.md) | An inventory of findings without exposing original sensitive values; a separate processed copy when cleanup is requested. Records replacements, omitted files, errors, and processing coverage, and follow-up actions for discovered credentials. |
| Triage a scanner report | [Security report triage](security-report-triage/overview.en.md) | Raw-signal accounting, applicability checks, justified duplicate grouping, and an action queue. |
| Verify a specified repair | [Security fix verification](security-fix-verification/overview.en.md) | Per-finding verdicts covering the original failure, bypass paths, and allowed operations. |

## How to use

1. Open the [skills repository](https://github.com/defrixx/Product-security-skills) and choose a directory under `skills/`.
2. Copy the entire directory into your assistant's skills location, preserving its internal layout.
3. Specify the skill name, task, and scope in your request. If automatic discovery is unavailable, point the assistant to `SKILL.md`.

The instructions are in English. The assistant needs file access; installation depends on the host application. Each skill page lists requirements for its optional helpers.

For repeatable installation, select and record the source commit before copying the package, review its instructions and optional scripts, and retain that revision with assessment evidence. Review updates before replacing the installed copy. Preserve the repository's MIT license notice when redistributing a standalone skill.

Each skill directory contains its required instructions, references, and templates; sibling skills are not required. For a combined task, copy the selected skills and name the stages to perform. The assistant carries out the selected stages according to the user's task. Installation of `prompt-integrity` is covered on the tool page.

## Connection to the playbooks

Playbooks define review criteria; skills turn them into a sequence of actions for a specific project. Results connect requirements, findings, changes, and checks so developers and reviewers can continue the work. Source and [tests](https://github.com/defrixx/Product-security-skills/tree/main/tests) live in Product-security-skills.

## Evidence and evaluations

Each skill includes a final evidence check that connects the assessed property, project revision, and observed result. The report templates include a common action ledger that preserves finding IDs, historical assessments, separate implementation and verification states, and unresolved work. See the [shared workflow](workflow/overview.en.md) for handoff rules.

Optional [behavioral evaluations](https://github.com/defrixx/Product-security-skills/blob/main/evals/README.md) compare synthetic tasks with and without skill instructions. Their runner and tests live in `evals/`, outside the copied skill packages. Evaluation artifacts remain local and are not included in a fresh clone.

## Current workflow coverage

Architecture profiles guide review and control selection. PR reviews compare security guarantees before and after the change; business-logic and concurrency prompts lead to mechanism-specific decisive checks. Fix verification uses a bypass matrix and relevant lifecycle/recovery cases. Report triage traces advisory applicability through the dependency, build, delivered artifact, and vulnerable functionality. Cleanup adds component accounting and linked-replacement checks without extending built-in format support.
