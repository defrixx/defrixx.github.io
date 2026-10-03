# Input context validation and sanitization: prompt-guard

`prompt-guard` is an independent Python library and CLI for checking untrusted UTF-8 text and JSON messages against source-scoped literal and regex rules. Version 0.2.0 requires Python 3.11+ on Linux or macOS and uses only the standard library at runtime. CLI inspection runs offline.

[Source and guide](https://github.com/defrixx/Product-security-skills/tree/main/tools/prompt-guard) | [Skills and tools](../security-skills/overview.en.md)

## Modes and admission decisions

`strict` is the default: a blocking match rejects the whole input without changing it. Explicit `sanitize` mode applies only policy-authorized replacements to a separate result, then checks the entire result again. A blocking rule without a replacement still blocks; overlapping incompatible edits also block. There is one transformation pass, with no automatic approval or iterative removal.

| Decision | CLI exit code | Application action |
| --- | --- | --- |
| `allow` | 0 | Dispatch only the returned payload. |
| `block` | 1 | Stop dispatch. |
| `review` | 2 | Stop automatic dispatch and resolve the signal through application policy. |
| `error` | 3 | Stop dispatch and address the diagnostic code. |

`allow` means the configured rules accepted the input. It does not establish semantic safety or authorize a model-proposed action. Sanitization can change task meaning; test allowed tasks as well as attacks before enabling replacements.

## Installation and first check

Install into the application's environment:

```sh
python -m pip install /path/to/Product-security-skills/tools/prompt-guard
```

Use existing directories and absolute paths without symbolic links. The CLI checks one file, not a directory. For a first offline check with a packaged profile:

```sh
prompt-guard --profile user-input \
  --input /path/to/input/sample.txt --input-root /path/to/input --source user
```

For sanitization, select a protected policy with authorized replacements and a fresh output file outside the input and configuration roots:

```sh
prompt-guard --policy /path/to/config/policy.json --config-root /path/to/config \
  --input /path/to/input/sample.txt --input-root /path/to/input --source user \
  --mode sanitize --output /path/to/results/new-clean.txt --output-root /path/to/results
```

A copy is written only on `allow`, with permissions `0600` and exclusive creation. Without `--output`, sanitization checks the result but does not emit its content. A failed write returns `error` and may leave a partial private file; do not dispatch it.

## Sources, profiles and detection coverage

JSON input uses `--format json` without `--source` and has this envelope:

```json
{"messages": [{"source": "user", "text": "Public request"}, {"source": "retrieval", "text": "Public document"}]}
```

Supported sources are `user`, `retrieval`, `file`, `tool` and `assistant`. The application assigns provenance from trusted routes; content must not choose its own source. These fields are distinct from provider message roles. Unknown fields, duplicate keys, invalid Unicode and empty message lists are rejected.

| Packaged profile | Coverage |
| --- | --- |
| `user-input` | User input; selected imperative attack patterns are anchored. |
| `retrieval`, `tool-results` | Retrieved documents or tool text, with broad instruction markers. |
| `security` | Attack markers across data sources and assembled context. |
| `restricted-topics` | Strict lexical topic restrictions. |
| `security-and-topics` | Combined attack and topic rules. |

Profiles contain representative English, Spanish, Russian and Japanese expressions; they are example policies requiring application-specific acceptance. Broad security rules can block quoted attacks. Topic rules block matching mentions even in prevention, education, news or quotations, have no contextual exemptions and permit no sanitization. Measure false blocks on realistic benign content before choosing a profile.

Schema v2 adds `normalized` detection views and `assembled` rules. Normalized views remove Unicode format characters, apply NFKC and, for case-insensitive rules, casefold; replacements map back to original spans. They do not decode base64 or transliterate arbitrary confusable alphabets. Assembled rules check source-selected messages in order using `assembly_separator`; set it to the application's actual text composition. These rules can block or request review, but cannot sanitize across message boundaries.

## Application integration and policy protection

1. Inspect incoming data and every new retrieval/tool round with trusted provenance. Check assembled context where fragments can combine into a prohibited expression.
2. Assemble the request from accepted payloads. Keep static instructions and tool definitions under [prompt-integrity](../prompt-integrity/overview.en.md) at final dispatch.
3. Validate arguments, resource scope and permissions for every proposed tool action before execution.

The library's `inspect` returns `payload` only on `allow`; send these bytes, including approved changes. Never fall back to the unchecked original on block, review or error. Apply the same boundaries to retries and fallback routes. Input objects and the loaded policy remain unchanged.

Protect policy configuration separately. For a pinned release, `load_policy` accepts `expected_id`, `expected_version` and `expected_sha256`; CLI equivalents are `--expected-policy`, `--expected-version` and `--expected-sha256` with `--policy`. Obtain all expected values from separately protected deployment configuration. The digest binds exact file bytes. A mismatch stops loading; rotation and rollback explicitly select the approved identity, version and digest together.

`prompt_guard.adapters.GuardedDispatch` supports Ollama `/api/chat` and Chat Completions `/v1/chat/completions` with a trusted static template and an exact numeric loopback HTTP endpoint. It checks all data messages together and sends the accepted snapshot. Its default sender has bounded bodies and a socket timeout, with no proxies, redirects or retries. An application-owned `integrity_sender` can connect it to `prompt-integrity`; protocol/history validation and action authorization remain application responsibilities. Attempted sanitization of assistant tool-call metadata stops dispatch.

## Execution limits and verification

Package hard maxima are 1 MiB for input and transformed payload, 128 JSON messages, 64 rules and 1,024 matches per scan. A worker scan is bounded at 2,000 ms, overall inspection at 6,000 ms and worker memory at 256 MiB. Policies may tighten these limits. Each interpreter admits at most four workers; excess requests return `worker_capacity_exhausted` and close the gate. These are package limits, separate from inference budgets. On macOS, sampled memory monitoring is not an instantaneous allocation ceiling.

Diagnostics include decisions, codes, policy/rule IDs and counts, excluding input text, matched fragments, paths and prompt hashes. Keep identifiers nonsensitive. An allowed payload may still contain sensitive data outside the selected rules.

[Package tests and synthetic corpus](https://github.com/defrixx/Product-security-skills/tree/main/tools/prompt-guard/tests) cover attacks, benign controls and intentional topic blocks. Before deployment, verify final-payload dispatch, all model-call routes, false blocks, resource exhaustion and policy mismatch handling in your integration.

[model-security-eval](../model-security-eval/overview.en.md) supports `--guard-profile`, `--guard-mode` and `--compare-guard` when the package is installed. Paired trials retain guard decisions, model violations and fixture actions separately, including blocked benign controls. A blocked input is `not_assessed_for_blocked_input`, not evidence that the model resisted the attack. Synthetic results do not establish detection coverage for arbitrary production inputs.
