# Security report triage

The `security-report-triage` skill interprets an existing scanner report: account for signals, check applicability, and prepare an action queue. It works independently, including without source code; unsupported assumptions then remain hypotheses.

[View skill source](https://github.com/defrixx/Product-security-skills/tree/main/skills/security-report-triage) | [Installation instructions](../overview.en.md)

## Inputs

Provide the report, its origin and scanner version if known, the claimed scan revision, the actual project revision, and local changes. Define the assessment scope and available evidence. Missing source is not fetched automatically.

## Workflow

The assistant accounts for every raw result, examines execution paths and guards, and seeks counterevidence. Confirmed findings, hypotheses, disproved signals, excluded results, and unprocessed results are recorded separately. Duplicates are grouped only when a common root cause and repair boundary are established; mappings to the original signals are retained.

Priority follows supported impact and exposure. Scanner severity, confidence, and the resulting priority remain separate.

For AI-related signals, distinguish prompt tampering, model proposals, and effects actually performed by a tool or data sink. Passing prompt-integrity verification does not disprove tool abuse, and an adversarial model response alone does not confirm an unauthorized effect. Trace the request, authorization gate, and destination before changing the finding's assessment.

## Local SARIF processing

The bundled normalizer supports a bounded subset of SARIF 2.1.0. It requires Python 3.9+ and POSIX filesystem operations. From the copied skill directory:

```sh
python3 scripts/normalize_sarif.py --input /path/to/report.sarif --output /path/to/new-run --target-root /path/to/target
```

Choose a fresh output directory with an existing trusted parent. Supply `--target-root` when source is available to keep output outside the assessed tree. The script creates `normalized.json` and `normalization-summary.json`, preserving the original report. A `RUNNING` marker means processing is incomplete.

Exit code `0` means extraction completed within the supported subset, `2` means partial output, unknown scanner invocation completeness, or unsupported fields, and `1` means a fatal error. These codes do not confirm a vulnerability or its repair.

The normalizer never opens report-supplied paths or links. Arbitrary strings, messages, and snippets are omitted; identifiers become opaque labels. Source and the original report require separate inspection within the agreed scope. Size and format limits are documented in the [SARIF intake contract](https://github.com/defrixx/Product-security-skills/blob/main/skills/security-report-triage/references/sarif-subset.md).

Opaque labels are per-input identifiers, not stable cross-run identities or content hashes. Preserve run/result ordinals for comparison with the original report; do not group findings across reports by these labels alone. Missing result arrays and unknown invocation completion do not establish a successful scan with zero findings.

## Example request

> Use security-report-triage on this SARIF report and the current project revision. Account for every raw signal, separate confirmed findings from hypotheses and disproved results, and justify duplicate grouping and priorities. Do not change code.

## Expected result and limits

The [report](https://github.com/defrixx/Product-security-skills/blob/main/skills/security-report-triage/assets/triage-report.md) includes an action queue, raw-signal and unique-finding counts, evidence, errors, and coverage gaps. Normalization does not replace vulnerability validation. Ordinary prose reports can use manual signal mapping with an explicit coverage statement.

Triage alone does not include scanner execution, running report-suggested commands, changing code, or creating external tickets. Continue through implementation and verification using the [combined workflow](../workflow/overview.en.md).

Before delivery, distinguish content identity from historical provenance: matching hashes do not establish report authorship or when a defect arose. Keep absent history unknown and retain unresolved signals in the action queue. A proposed repair, an observed applied change, and a verified fix remain separate states.

## Related material

- [Security review](../security-review/overview.en.md)
- [Fix verification](../security-fix-verification/overview.en.md)
- [Vulnerability management](../../../review/vulnerability-management/playbook.en.md)
