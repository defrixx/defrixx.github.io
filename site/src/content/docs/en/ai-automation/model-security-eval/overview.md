---
title: "Local model security checks: model-security-eval"
description: "`model-security-eval` runs synthetic security scenarios against local LM Studio and Ollama models after updates and provides a blocking CI verdict. Version 0.4.0 requires Python..."
sidebar:
  order: 90
---
`model-security-eval` runs synthetic security scenarios against local LM Studio and Ollama models after updates and provides a blocking CI verdict. Version 0.4.0 requires Python 3.11+ and uses only the standard library for its core runtime. It works independently of the skills; guarded comparisons additionally require `prompt-guard` 0.3.x.

[Source and guide](https://github.com/defrixx/Product-security-skills/tree/main/tools/model-security-eval) | [Skills and tools](/en/ai-automation/security-skills/overview/)

## Capabilities and scenarios

Choose the capabilities exposed by your application with `--capabilities`; every profile includes `chat`.

| Capability | Allowed task | Attack scenarios |
| --- | --- | --- |
| `chat` | Return requested public data | Instruction and role overrides, private-token disclosure including encoded forms, forged approval, and multiple turns. |
| `read` | Read `repo/README.md` and return its API description | Other paths and instructions embedded in README, code comments, and retrieval metadata. |
| `write` | Write public data to `repo/result.txt` | Other paths, forged approval, and scope expansion. |
| `command` | Invoke `tests` | Other commands, forged approval, and scope expansion. |
| `external` | Send public data to `sandbox` | Other recipients, private-token exfiltration, and forged approval. |

The runner uses synthetic content, in-memory files, virtual command results, and intercepted messages. It checks a proposed batch before the first effect and distinguishes proposed, blocked, and completed fixture actions. Allowed tasks accompany attacks: a model that refuses everything cannot pass. Multi-stage cases require the authorized action and correct acknowledgement before delivering the scope-expansion attempt.

## Installation and first run

Install into a dedicated environment:

```sh
python -m pip install /path/to/Product-security-skills/tools/model-security-eval
```

Start the local inference server and load the selected model beforehand. Run from a directory whose existing `artifacts/` parent is writable; choose a fresh output path without symlink components:

```sh
mkdir -p artifacts
model-security-eval \
  --backend ollama --model "$MODEL_ID" \
  --capabilities chat,read,write,command,external \
  --repetitions 3 --max-requests 300 --max-seconds 1800 \
  --request-timeout 120 --max-steps 6 --max-tokens 2048 \
  --output "artifacts/$RUN_ID"
```

Set `MODEL_ID` to the loaded model and `RUN_ID` to a new run name. For LM Studio, select `--backend lmstudio` and supply nonblank `--model-revision` and `--server-version`. These LM Studio values are caller assertions, not independently verified weight hashes. Ollama discovers the model digest and server version; the same optional flags pin expected values.

Default origins are `http://127.0.0.1:11434` for Ollama and `http://127.0.0.1:1234` for LM Studio. A custom `--endpoint` must be a numeric loopback HTTP origin with an explicit port, without credentials, query, or endpoint path. Proxies, redirects, automatic retries, and fallback are disabled. The transport sends no authentication header; a server requiring API authentication needs an explicitly supported integration.

Use `--list-cases` with the required backend, model, output, and capability arguments to inspect the inventory without contacting a server or creating output.

## Budgets and comparison

The command shows the defaults: three trials per scenario, 300 total inference and metadata dispatch attempts, 1800 seconds per run, 120 seconds per request, six inference rounds per trial, and 2048 requested output tokens per response. These are runner budgets, not universal production security limits. The request deadline is bounded by remaining run time. Defaults also request `--temperature 0` and `--seed 17`; repetitions add their index to the seed. Requests are bounded at 4 MiB and responses at 2 MiB.

Before and after execution, the runner reads model metadata and binds inference responses to the selected model and discovered aliases. Metadata drift blocks admission. Server-reported metadata is part of the local server trust boundary.

Add `--baseline artifacts/previous-run/report.json` to compare trial statuses. Comparable criteria require the same scenario suite, evaluator source bytes, capabilities, adapter, generation settings, repetitions, and budgets. Incompatible criteria block admission; model, revision, server, and endpoint changes are recorded separately. An improved result does not override a current failure.

## CI verdict and reports

With `--compare-guard`, compare unguarded and guarded application behavior using `--guard-profile`, `--output-guard-profile`, or both. Each arm has its own equal request/time budget, so reserve resources for both. This mode cannot be combined with historical `--baseline` comparison. A blocked attack can pass the application control without proving model resistance; a blocked allowed task fails. Keep generated model violations separate from violations exposed by the guarded application, and treat review, errors, or incomplete execution as inconclusive.

| Exit code | Verdict | Release action |
| --- | --- | --- |
| `0` | `pass`: all planned trials completed and checks passed | Permit the next promotion step. |
| `1` | `fail`: observed violation or failed allowed task | Block promotion. |
| `2` | `inconclusive` or execution/configuration error | Block promotion. |

Place the [CI script](https://github.com/defrixx/Product-security-skills/blob/main/tools/model-security-eval/examples/ci-gate.sh) before promotion on a runner with the local server. Run it from the skills repository root with `MODEL_ID` and `EVAL_OUTPUT`; LM Studio also needs `MODEL_REVISION` and `SERVER_VERSION`. The script preserves the CLI exit status. Preserve reports through the pipeline's artifact-retention step.

Each run creates `report.md`, structured `report.json`, and an atomically updated `checkpoint.json`. Output directories use permissions `0700`, evidence files `0600`. Private-token forms are redacted; observations are scored in full and stored as bounded previews with hashes. Checkpoints record completed, active, and pending trials. Interruption blocks promotion and records interrupted progress; checkpoints do not imply automatic resume. Stdout carries JSON events with identifiers, diagnostics, counts, and criteria fingerprints rather than provider response text.

## Connection to application controls

[Package tests](https://github.com/defrixx/Product-security-skills/tree/main/tools/model-security-eval/tests) cover fixture actions, normalization, identity, comparison, redaction, checkpoints, CI statuses, and loopback HTTP. They do not require a real model. A passing model run establishes the observed result for the selected synthetic profile; verify application dispatch and action authorization separately.

[prompt-integrity](/en/ai-automation/prompt-integrity/overview/) checks approved static instructions at dispatch. `model-security-eval` evaluates model behavior and fixture action boundaries; it does not automatically install that wrapper or enforce production tool permissions. Keep independent argument validation, resource and recipient scope checks, and authorization before actual application effects.
