---
title: "Bifrost integration"
description: "The Bifrost integration connects Prompt Guard and Prompt Integrity at application ingress and final provider dispatch. It also stages the five independent skills for Bifrost's S..."
sidebar:
  order: 110
---
The Bifrost integration connects Prompt Guard and Prompt Integrity at application ingress and final provider dispatch. It also stages the five independent skills for Bifrost's Skills Repository and runs bounded model-behavior evaluations through a configured gateway route. It uses Bifrost OSS's Chat Completions HTTP interface without a gateway fork or an Enterprise Guardrails subscription.

[Source and setup](https://github.com/defrixx/Product-security-skills/tree/main/integrations/bifrost) | [Skills and tools](/en/ai-automation/security-skills/overview/)

## Capabilities and results

| Task | Input | Result |
| --- | --- | --- |
| Check text chat | Source-labelled UTF-8 JSON messages and an application-owned pinned policy | Checked assistant text; rejection stops the operation |
| Protect request integrity | Approved baselines for model, system instruction, options and tool definitions | Verification and dispatch of the same serialized request snapshot at the selected boundary |
| Connect agent clients | Approved agent contracts, fixed tool schemas and bounded JSON or SSE responses | Checked content and tool proposals after the complete response passes validation |
| Execute approved tools | Checked proposals, authenticated workflow context, application authorizer and executors | One-shot batch execution and checked tool-result messages for an explicit next model round |
| Import skills | Trusted local checkout and a new staging directory | Five independent skill folders and a SHA-256 manifest |
| Investigate route behavior | Configured gateway endpoint, requested route and expected response model | Per-case Model Security Eval results bound to that route |

Supported structured reasoning text is inspected together with visible content in the explicit `inspect-and-drop` mode, then removed before release. Buffered SSE is fully received and checked before any downstream response is emitted; clients receive a fresh SSE envelope after validation, with full-response latency. Tool execution requires the application's explicit authorization for every call and application-owned executors. The application owns authenticated history, effect-side authorization, I/O bounds and durable idempotency.

## Choose the boundary

`GuardedClient` provides an opt-in text boundary for calls made through that client. The token-authenticated ingress facade exposes only `POST /v1/chat/completions` with a closed request contract. `ProviderBoundary` checks the final provider request snapshot and owns serialization and the single send for the selected provider contract.

For a mandatory deployment path, expose the facade to clients, keep Bifrost on a private gateway network, and place final egress between that network and a separate model network. Restrict direct access and keep gateway and model credentials separate. Configure routing, cache and retry behavior for the selected contract; remote ingress requires deployment-owned TLS and access control. The reference runner uses provisioned local images and isolated networks with Bifrost v2.4.0 and a synthetic model backend.

## Run and integrate

Use Python 3.11+ from the Product-security-skills repository root. The examples use synthetic policies; approve application policies, independent digest pins, endpoints and credentials before adapting them.

```sh
export PYTHONPATH="$PWD/tools/prompt-guard/src:$PWD/tools/prompt-integrity/src:$PWD/integrations/bifrost"
python3 integrations/bifrost/example_integrity.py
python3 integrations/bifrost/stage_skills.py /tmp/product-security-skills-import
```

Choose a new staging destination with an existing parent. In Bifrost, create each skill with its existing metadata, paste the Markdown body and upload supporting folders with their relative layout. Review the staged files and explicitly authorize publication. Skill hosting supplies instructions to the assistant; runtime enforcement comes from the selected application boundaries.

The source guide includes separate ingress, final-egress and agent examples, route evaluation, local suites and provisioned-image reference trials for text, JSON tools and buffered streaming.

## Route identity and evaluation

Route evaluation records behavioral results with `eligible=false`: observed failures produce `fail`/exit 1; otherwise the aggregate is `inconclusive`/exit 2. Completion receipts verify an issuer's HMAC-bound statement about request, response and route identity. Actual serving weights and revisions require independent attestation; these receipts retain `weights_attested=false` and `eligible=false`. Requiring Model Security Eval admission currently stops the request before any model send. Use the Guard/Integrity path for its request and response checks, and retain route evaluation as behavioral evidence.
