---
title: "Security Skills"
description: "Instructions for an AI assistant: workflows, reference material, and report templates. Local Python helpers support selected operations."
sidebar:
  order: 10
---
Instructions for an AI assistant: workflows, reference material, and report templates. Local Python helpers support selected operations.

| Task | Skill | Result |
| --- | --- | --- |
| Write or change code | [Secure development](/Product-security-playbook/en/ai-automation/security-skills/secure-development/overview/) | Implementation against applicable requirements and verification results |
| Assess a PR or repository | [Security review](/Product-security-playbook/en/ai-automation/security-skills/security-review/overview/) | Confirmed findings, hypotheses, and remediation guidance |
| Prepare a folder for sharing | [Sensitive data cleanup](/Product-security-playbook/en/ai-automation/security-skills/sensitive-data-cleanup/overview/) | A separate cleaned copy and processing report |

## How to use

1. Open the [skills repository](https://github.com/defrixx/Product-security-skills) and choose a directory under `skills/`.
2. Copy the entire directory into your assistant's skills location, preserving its internal layout.
3. Specify the skill name, task, and scope in your request. If automatic discovery is unavailable, point the assistant to `SKILL.md`.

The instructions are in English. The assistant needs file access; installation depends on the host application. Each skill page lists requirements for its optional helpers.

## Connection to the playbooks

Playbooks define review criteria; skills help apply them to a specific task. Source and [tests](https://github.com/defrixx/Product-security-skills/tree/main/tests) live in the separate repository. Review proposed changes and finding evidence before accepting the result.
