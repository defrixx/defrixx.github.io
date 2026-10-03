# Security Skills and Tools

Instructions for an AI assistant: workflows, reference material, and report templates. Local Python helpers support selected operations.

Five standalone skills can be used individually or combined in a [shared workflow](workflow/overview.en.md). The separate [prompt-integrity tool](../prompt-integrity/overview.en.md) integrates with an application to check static instruction integrity before model dispatch.

| Task | Skill | Result |
| --- | --- | --- |
| Write or change code | [Secure development](secure-development/overview.en.md) | Changed code or an explicitly labeled candidate implementation, applied requirement IDs, and verification evidence. The report separately records exceptions, assumptions, and conditions that could not be verified. |
| Assess a PR or repository | [Security review](security-review/overview.en.md) | Findings with exploitation prerequisites, impact, confidence, and fix-verification criteria. A coverage table separates confirmed results from hypotheses and untested areas, even when no vulnerabilities are found. |
| Prepare a folder for sharing | [Sensitive data cleanup](sensitive-data-cleanup/overview.en.md) | An inventory of findings without exposing original sensitive values; a separate processed copy when cleanup is requested. Records replacements, omitted files, errors, and coverage limits; cleanup does not revoke exposed credentials. |
| Triage a scanner report | [Security report triage](security-report-triage/overview.en.md) | Raw-signal accounting, applicability checks, justified duplicate grouping, and an action queue. |
| Verify a specified repair | [Security fix verification](security-fix-verification/overview.en.md) | Per-finding verdicts covering the original failure, bypass paths, and allowed operations. |

## How to use

1. Open the [skills repository](https://github.com/defrixx/Product-security-skills) and choose a directory under `skills/`.
2. Copy the entire directory into your assistant's skills location, preserving its internal layout.
3. Specify the skill name, task, and scope in your request. If automatic discovery is unavailable, point the assistant to `SKILL.md`.

The instructions are in English. The assistant needs file access; installation depends on the host application. Each skill page lists requirements for its optional helpers.

Each skill directory contains its required instructions, references, and templates; sibling skills are not required. For a combined task, copy the selected skills and name the stages to perform. No separate workflow execution engine is included. Installation of `prompt-integrity` is covered on the tool page.

## Connection to the playbooks

Playbooks define review criteria; skills help apply them to a specific task. Source and [tests](https://github.com/defrixx/Product-security-skills/tree/main/tests) live in the separate repository. Review proposed changes and finding evidence before accepting the result.

## Evidence and evaluations

Each skill requires an evidence check before delivery. Claims must match the exact property, revision, and output actually checked. The report templates include a common action ledger that preserves finding IDs, historical assessments, separate implementation and verification states, and unresolved work. See the [shared workflow](workflow/overview.en.md) for handoff rules.

Optional [behavioral evaluations](https://github.com/defrixx/Product-security-skills/blob/main/evals/README.md) compare synthetic tasks with and without skill instructions. Their runner and tests live in `evals/`, outside the copied skill packages. Completed model responses and passing harness tests do not establish accurate security conclusions. Evaluation artifacts remain local and are not included in a fresh clone.
