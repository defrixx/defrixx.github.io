---
title: "Static instruction integrity: prompt-integrity"
description: "`prompt-integrity` is a standalone Python library and CLI that checks application-controlled static instructions immediately before model dispatch. Version 0.1.0 supports a boun..."
sidebar:
  order: 80
---
`prompt-integrity` is a standalone Python library and CLI that checks application-controlled static instructions immediately before model dispatch. Version 0.1.0 supports a bounded text-only subset of Ollama `/api/chat`.

[Source and guide](https://github.com/defrixx/Product-security-skills/tree/main/tools/prompt-integrity) | [Skills and combined workflow](/Product-security-playbook/en/ai-automation/security-skills/overview/)

## What the tool checks

The application loads an approved baseline with an expected profile ID and version. The baseline defines an exact `system` message prefix, allowed subsequent message roles, target alias-to-model mappings, and resource bounds.

`verify_and_send` snapshots the request, validates it, and passes the same immutable bytes to the transport. Changed instruction text, order or roles, unknown models, and unsupported fields block dispatch. Whitespace, newlines, case, and Unicode distinctions matter; equivalent JSON escaping is accepted.

`check_request` is diagnostic only: success does not authorize later dispatch of the mutable original object. Each retry or fallback attempt must call `verify_and_send` again.

## Supported format

Adapter `ollama-chat-text-v1`, version `1`, accepts only `model`, `messages`, and `stream: false`. Each message contains only `role` and string `content`. One or more exact `system` messages precede the `user` and `assistant` messages allowed by the baseline.

Extra fields, tools, images, arbitrary options, and other API formats are unsupported. User text attempting to override instructions remains permitted data when its role is allowed: the tool does not classify such attacks.

## Installation and CLI

Python 3.11+ and POSIX filesystem operations are required. Runtime uses only the standard library. Install the package from a local repository copy into the application's environment:

```sh
python -m pip install /path/to/Product-security-skills/tools/prompt-integrity
```

Use the synthetic files in `examples/` for an initial trial. Replace paths with absolute paths without symlink components:

```sh
prompt-integrity baseline validate --baseline /path/to/examples/baseline.json --config-root /path/to/examples --expected-profile synthetic-support --expected-version 1
prompt-integrity request check --baseline /path/to/examples/baseline.json --request /path/to/examples/request.json --target primary --config-root /path/to/examples --expected-profile synthetic-support --expected-version 1
prompt-integrity baseline create --instructions /path/to/examples/instructions.json --policy /path/to/examples/policy.json --output /path/to/examples/new-candidate.json --config-root /path/to/examples --expected-profile synthetic-support --expected-version 1
```

CLI commands never call a model. Exit code `0` means the selected operation succeeded, `2` means the request failed integrity policy, and `1` means a configuration, I/O, resource, or internal error. Baseline creation produces a candidate for review and approval; existing files are not overwritten.

## Application integration

```python
from prompt_integrity import load_policy, verify_and_send
from prompt_integrity.transport import HTTPTransport

policy = load_policy(
    "/protected/baseline.json", "synthetic-support", "1",
    config_root="/protected",
)
transport = HTTPTransport((("primary", "http://127.0.0.1:11434/api/chat"),))
# request is assembled by the application.
response = verify_and_send(policy, request, "primary", transport)
```

Before a real call, configure an approved baseline and real models: example model names are synthetic. Protect the baseline from modification through untrusted paths; expected profile and version come from trusted deployment configuration. Schema validation does not establish baseline provenance or approval. The loaded policy is immutable; updates and rollbacks require an explicitly selected version and a restart or reload by trusted code.

Route every model call, background job, retry, and fallback through the wrapper. Do not mutate input objects concurrently with snapshot creation. A custom transport remains trusted and must send the supplied bytes unchanged.

The built-in `HTTPTransport` performs no redirects, proxy use, or automatic retries. HTTPS uses platform certificate verification; cleartext HTTP is restricted to loopback addresses. Response size is bounded. `IntegrityError` occurs before dispatch; `TransportError` means transport failed after a successful check and does not guarantee the server never received the request. Neither error authorizes bypassing verification.

## Protection boundaries and validation

The tool checks the observable request. It does not guarantee model obedience, prompt-injection resistance, output safety, or action authorization. Wrapper bypass, a compromised process, and control over both the baseline and checker are outside its protection.

Filesystem operations require an explicit root and refuse symlink path components, nonregular input files, and input hardlinks. Hostile concurrent directory replacement is outside the guarantee. An interrupted candidate write can leave a partial file: validate before approval and use a fresh path for a retry.

[Package tests](https://github.com/defrixx/Product-security-skills/tree/main/tools/prompt-integrity/tests) exercise instruction changes, request shape, snapshots, retries, CLI behavior, filesystem restrictions, and local HTTP. They use synthetic data and need no model. Before use in your application, inspect every dispatch call site and transport interceptor; package tests do not establish the absence of bypass in your integration.
