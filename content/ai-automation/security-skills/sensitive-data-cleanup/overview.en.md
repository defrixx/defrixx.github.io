# Sensitive data cleanup

Use to inspect a folder or prepare a separate copy for sharing. The assistant classifies candidate sensitive values and uses a bounded local helper where applicable.

[View skill source](https://github.com/defrixx/Product-security-skills/tree/main/skills/sensitive-data-cleanup) | [Installation instructions](../overview.en.md)

## Inputs

Provide the source folder, exclusions, sensitivity policy, and a fresh output destination outside the source tree. Choose scan-only, text cleanup, or JPEG/PNG metadata-only cleanup.

## Coverage and dependencies

UTF-8 text, JSON, JSONL, and CSV cleanup; a separate mode removes JPEG/PNG metadata while preserving encoded pixels. `scripts/cleanup.py` requires Python 3.9+, the standard library, and POSIX filesystem operations. Read its helper contract before use.

## Example request

> Use sensitive-data-cleanup to prepare this folder for sharing in a new sibling directory. Preserve originals. Report replacements, omitted files, errors, and residual uncertainty without exposing original sensitive values.

## Expected result and limits

A separate cleaned copy when requested, a redacted inventory, and coverage limits. Unsupported or failed files are omitted and reported. Image content is not redacted; removing metadata can change displayed orientation or color. Cleanup does not revoke leaked credentials or remove Git history and backups, and does not guarantee exhaustive personal-data discovery or a runnable copy.

A detector match does not by itself confirm sensitive data: classify the value using context and the selected policy. An omitted or unsupported file remains a coverage gap even when no matches are found in processed files.

## Files and verification

Instructions and references are bundled with the skill. Use the [report template](https://github.com/defrixx/Product-security-skills/blob/main/skills/sensitive-data-cleanup/assets/cleanup-report.md) to record results. [Tests](https://github.com/defrixx/Product-security-skills/tree/main/tests) are maintained in the source repository.

## Related playbooks

- [Secrets management with Vault](../../../platform-security/secrets/vault/playbook.en.md)
- [Secure AI-assisted development](../../../ai-security/ai-assisted-development/playbook.en.md)
