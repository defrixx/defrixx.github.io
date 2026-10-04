---
title: "Context and model output validation and sanitization: prompt-guard"
description: "`prompt-guard` is an independent Python library and CLI for checking untrusted input context and model outputs against independent policies. It inspects UTF-8 text and JSON mess..."
sidebar:
  order: 100
---
`prompt-guard` is an independent Python library and CLI for checking untrusted input context and model outputs against independent policies. It inspects UTF-8 text and JSON messages with source-scoped literal and regex rules. Version 0.3.0 requires Python 3.11+ on Linux or macOS and uses only the standard library at runtime. CLI inspection runs offline.

[Source and guide](https://github.com/defrixx/Product-security-skills/tree/main/tools/prompt-guard) | [Skills and tools](/Product-security-playbook/en/ai-automation/security-skills/overview/)

## Modes and admission decisions

`strict` is the default: a blocking match rejects the whole input without changing it. Explicit `sanitize` mode applies only policy-authorized replacements to a separate result, then checks the entire result again. A blocking rule without a replacement still blocks; overlapping incompatible edits also block. There is one transformation pass, with no automatic approval or iterative removal.

| Decision | CLI exit code | Application action |
| --- | --- | --- |
| `allow` | 0 | Send only the returned payload to the model or user. |
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

## Input sources, profiles and detection coverage

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
2. Assemble the request from accepted payloads. Keep static instructions and tool definitions under [prompt-integrity](/Product-security-playbook/en/ai-automation/prompt-integrity/overview/) at final dispatch.
3. Inspect model responses with a separate output policy before user delivery or execution of proposed tool calls.
4. Validate arguments, resource scope and permissions for every proposed tool action before execution.

The library's `inspect` returns `payload` only on `allow`; send these bytes, including approved changes. Never fall back to the unchecked original on block, review or error. Apply the same boundaries to retries and fallback routes. Input objects and the loaded policy remain unchanged.

Protect policy configuration separately. For a pinned release, `load_policy` accepts `expected_id`, `expected_version` and `expected_sha256`; CLI equivalents are `--expected-policy`, `--expected-version` and `--expected-sha256` with `--policy`. Obtain all expected values from separately protected deployment configuration. The digest binds exact file bytes. A mismatch stops loading; rotation and rollback explicitly select the approved identity, version and digest together.

`prompt_guard.adapters.GuardedDispatch` supports Ollama `/api/chat` and Chat Completions `/v1/chat/completions` with a trusted static template and an exact numeric loopback HTTP endpoint. It checks all data messages together and sends the accepted snapshot. Its default sender has bounded bodies and a socket timeout, with no proxies, redirects or retries. An application-owned `integrity_sender` can connect it to `prompt-integrity`; protocol/history validation and action authorization remain application responsibilities. Attempted sanitization of assistant tool-call metadata stops dispatch.

## Model output inspection

Select a separate output policy and keep it in trusted application configuration. Input and output policies are configured independently; request content must not let users select them. A custom output policy must select the `assistant` source.

| Output profile | Coverage |
| --- | --- |
| `output-topics` | Restricted topic mentions; matches block in both modes. |
| `output-secrets` | Private-key blocks, including unfinished blocks, selected token shapes and credential assignments. |
| `output-security-and-topics` | Secret detection and topic restrictions. |
| `output-personal-data` | Email addresses and international phone numbers; explicitly selected. |

These are lexical rules, not universal content classification. For example, `output-personal-data` also blocks matching public contact details in `strict` mode. Supply exact protected values through `protected=(...)`: matches always block, even in `sanitize`. Explicitly list encoded variants when the application's protected-value requirements call for them.

```python
from prompt_guard import OutputGuard, load_profile

boundary = OutputGuard.create(
    load_profile("output-security-and-topics"),
    mode="sanitize",
    protected=("SYNTHETIC_APPLICATION_CANARY",),
)
result = boundary.check_text("Public greeting API")
if result.decision == "allow":
    deliver(result.payload.decode("utf-8"))
else:
    deliver("The response was withheld by application policy.")
```

Here, `deliver` is the application's response delivery function. Content is available only on `allow`; diagnostics and result repr exclude it. On rejection, use an application-owned fallback without fragments from the rejected result.

To inspect a saved response through the CLI:

```sh
prompt-guard --direction output --profile output-security-and-topics \
  --input /path/to/input/answer.txt --input-root /path/to/input
```

In this direction, text is assigned to `assistant`, and `--format json` accepts a message with `content` and optional `tool_calls`, rather than the input `messages` list. Use `--output-contract /path/to/config/contract.json` with `--format json` and `--config-root`; the file must contain exactly `{"schema": ..., "tools": ...}`. Write a separate accepted copy with `--output` and `--output-root` in either `strict` or `sanitize` mode.

## Structured responses and tool calls

`OutputGuard.create(..., schema=..., tools={name: argument_schema})` pins content and argument contracts. `check_message` accepts `{"content": text_or_json, "tool_calls": [{"id": ..., "name": ..., "arguments": ...}]}`. It scans string values in content and arguments, field names and routing metadata; `assembled` rules also inspect combined values. Sanitization can change values, but not tool names, keys or IDs. The original object is preserved, and transformed content and arguments must satisfy their contracts again.

Unconfigured tools are denied. The whole batch is checked before the first handler runs. `execute_tools(message, executors)` invokes trusted application handlers and returns `(diagnostics, results)`; rejection returns `results=None`. When executing calls yourself, decode only an allowed result, including checked transformations. The application owns the handler registry; model data must not supply it.

The supported JSON contract subset includes `type`, `enum`, closed objects with `properties`, `required` and `additionalProperties: false`, arrays with `items`, `minItems` and required `maxItems`, strings with `minLength` and required `maxLength`, and numbers with `minimum` and `maximum`. Unknown keywords, schema references, regex validators and coercion are rejected. Nesting is limited to 16; booleans are not numbers. Bind sensitive paths, recipients and commands to exact application-authorized `enum` values.

Contracts do not replace authorization. Handlers own current permissions, filesystem access, execution deadlines and transactions. A handler failure stops later calls with `tool_execution_failed` but does not roll back completed effects. Tool results must pass input inspection before the next model round.

## Provider responses and streaming

Pass `output_guard=boundary` to `GuardedDispatch.create(...)`. With `stream: false`, `send` and `send_user_text` return safe diagnostics and an accepted canonical message. The original provider envelope is not released. Separate inspection is available through `check_provider(response, "openai" | "ollama")`. With a structured contract, response content is parsed as strict JSON. One complete assistant choice is supported; truncated responses, unsupported fields and malformed argument JSON stop release. Multimodal data and additional provider channels require a separate contract.

For a trusted template with `stream: true`, use `send_stream(request, emit, timeout=30)`. The adapter collects OpenAI-compatible SSE or Ollama NDJSON, including fragmented tool arguments, requires the terminal protocol marker and checks the complete message. It calls `emit` once only on `allow`; raw events are not passed to the caller. The built-in transport bounds data size, read waits and whole-transport duration, with no redirects or retries. An integrity-backed stream requires an explicit `stream_sender` that verifies final request bytes.

For application-decoded text chunks, use `boundary.stream(chunks, emit, delivery="buffered")`. Buffering holds the whole response until acceptance and supports both modes, regex, normalization and assembled-context rules. Defaults allow 4,096 chunks, 1 MiB and 60 seconds between iterator reads; custom iterators must enforce their own blocking-read timeout.

`delivery="delayed"` is explicitly selected and supports text with raw case-sensitive literal rules only. It checks accumulated text and retains a possible partial-match tail. Regex, normalization, `assembled` rules and replacements require buffering; incompatible policies return `stream_policy_requires_buffering` before reading data. An emitted prefix cannot be retracted: choose `buffered` when any topic match must reject the whole answer. Iterator or emitter errors stop delivery without fallback; the emitter should commit an approved fragment atomically. Diagnostics include `emitted_characters`, not emitted text.

## Execution limits and verification

Package hard maxima are 1 MiB for input and transformed payload, 128 JSON messages, 64 rules and 1,024 matches per scan. A worker scan is bounded at 2,000 ms, overall inspection at 6,000 ms and worker memory at 256 MiB. Policies may tighten these limits. Each interpreter admits at most four workers; excess requests return `worker_capacity_exhausted` and close the gate. These are package limits, separate from inference budgets. On macOS, sampled memory monitoring is not an instantaneous allocation ceiling.

Diagnostics include decisions, codes, policy/rule IDs and counts, excluding input text, matched fragments, paths and prompt hashes. Keep identifiers nonsensitive. An allowed payload may still contain sensitive data outside the selected rules.

[Package tests and synthetic corpus](https://github.com/defrixx/Product-security-skills/tree/main/tools/prompt-guard/tests) cover attacks, benign controls and intentional topic blocks. Before deployment, verify final-payload dispatch, all model-call routes, false blocks, withheld rejected outputs, contract revalidation after sanitization, truncated streams, resource exhaustion and policy mismatch handling in your integration.

[model-security-eval](/Product-security-playbook/en/ai-automation/model-security-eval/overview/) supports `--guard-profile`, `--guard-mode` and `--compare-guard` when the package is installed. Paired trials retain guard decisions, model violations and fixture actions separately, including blocked benign controls. A blocked input is `not_assessed_for_blocked_input`, not evidence that the model resisted the attack. Synthetic results do not establish detection coverage for arbitrary production inputs.

For paired output evaluation, use `--output-guard-profile output-security-and-topics --compare-guard`, optionally with an input profile. Reports separately retain raw-generation violations as redacted evidence, released responses, output guard decisions and fixture actions. Blocking a violation can pass the application control while the model violation remains recorded. Blocked benign controls fail; output inspection execution errors are inconclusive.
