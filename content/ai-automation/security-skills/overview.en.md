# Security Skills

Instructions for an AI assistant: workflows, reference material, and report templates. Local Python helpers support selected operations.

| Task | Skill | Result |
| --- | --- | --- |
| Write or change code | [Secure development](secure-development/overview.en.md) | Changed code or an explicitly labeled candidate implementation, applied requirement IDs, and verification evidence. The report separately records exceptions, assumptions, and conditions that could not be verified. |
| Assess a PR or repository | [Security review](security-review/overview.en.md) | Findings with exploitation prerequisites, impact, confidence, and fix-verification criteria. A coverage table separates confirmed results from hypotheses and untested areas, even when no vulnerabilities are found. |
| Prepare a folder for sharing | [Sensitive data cleanup](sensitive-data-cleanup/overview.en.md) | An inventory of findings without exposing original sensitive values; a separate processed copy when cleanup is requested. Records replacements, omitted files, errors, and coverage limits; cleanup does not revoke exposed credentials. |

## How to use

1. Open the [skills repository](https://github.com/defrixx/Product-security-skills) and choose a directory under `skills/`.
2. Copy the entire directory into your assistant's skills location, preserving its internal layout.
3. Specify the skill name, task, and scope in your request. If automatic discovery is unavailable, point the assistant to `SKILL.md`.

The instructions are in English. The assistant needs file access; installation depends on the host application. Each skill page lists requirements for its optional helpers.

## Connection to the playbooks

Playbooks define review criteria; skills help apply them to a specific task. Source and [tests](https://github.com/defrixx/Product-security-skills/tree/main/tests) live in the separate repository. Review proposed changes and finding evidence before accepting the result.
