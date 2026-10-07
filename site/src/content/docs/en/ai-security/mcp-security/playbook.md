---
title: "MCP Security Playbook"
description: "This playbook covers production use of Model Context Protocol (MCP) where AI applications discover or invoke tools, resources, or reusable prompts through local or remote MCP se..."
sidebar:
  order: 40
---
## 1. Scope and Objective

This playbook covers production use of Model Context Protocol (MCP) where AI applications discover or invoke tools, resources, or reusable prompts through local or remote MCP servers.

Use this document for:
- MCP architecture review before production use;
- onboarding internal and third-party MCP servers;
- reviewing MCP gateways, OAuth flows, tool wrappers, resource exposure, and prompt templates;
- building negative tests for tool execution, authorization, logging, and capability drift.

Document ownership:
- This playbook owns MCP protocol deployment patterns, server/tool/resource/prompt registry, capability baselines, transport choices, MCP-specific OAuth usage, gateway policy, protocol logging, and capability drift controls.
- It treats tool abuse and data leakage through the MCP boundary: server approval, capability negotiation, resource exposure, token handling, and downstream destination control.
- It relies on [Securing AI](/en/ai-security/securing-ai/overview/) for the general AI control baseline and on the [Agentic AI security playbook](/en/ai-security/agentic-ai/playbook/) for agent autonomy, memory, action traces, approvals, rollback, and kill switches.
- It uses the [OWASP LLM Top 10 overview](/en/ai-security/owasp-llm-top-10/overview/) for threat taxonomy, not as a deployment checklist.

Out of scope:
- general model behavior, prompt injection, RAG, and AI release governance; use the [Securing AI overview](/en/ai-security/securing-ai/overview/);
- OAuth/OIDC fundamentals outside MCP-specific usage; use the [OIDC + OAuth 2.0 security guide](/en/application-security/identity/oidc-oauth/playbook/);
- generic API hardening for downstream business APIs; use the [API security playbook](/en/application-security/api/api-security-patterns/playbook/).

Objective:
- make every MCP capability explicit, authorized, observable, and revocable before it can affect production data or business state.

---

## 2. MCP Trust Boundaries

Minimum components to model:
- host: AI application or IDE/client that embeds an MCP client;
- client: protocol component that connects to MCP servers;
- server: local or remote process exposing tools, resources, and prompts;
- gateway: optional but recommended control point for production;
- downstream systems: APIs, databases, filesystems, browsers, queues, SaaS, and identity providers reached by tools.

MCP primitives are security surfaces:
- tools are callable operations and must be treated as APIs;
- resources are data access paths and inherit the classification of the underlying data;
- prompts are content supply-chain inputs and must not be trusted as policy or secrets;
- elicitation requests user input and introduces consent and identity-binding boundaries;
- Roots and Sampling are deprecated in `2026-07-28`; do not adopt them in new implementations. Roots are informational, never filesystem authorization.

High-impact scenarios:
- a local `stdio` server installed by a developer exposes file or shell access to a production-capable agent;
- a remote server silently adds a write tool or broad resource pattern after initial approval;
- a model-supplied parameter reaches a privileged backend because the tool handler trusts schema hints instead of enforcing server-side validation;
- OAuth tokens leak through logs, prompts, resource payloads, or token passthrough to downstream APIs;
- a third-party MCP server changes behavior, dependencies, or capability declarations without enterprise review.

---

## 3. Production Baseline

### 3.1 MCP Registry

`Baseline`:
- Maintain an enterprise MCP registry as the authoritative inventory for production-approved servers, tools, resources, prompts, transports, owners, environments, scopes, downstream destinations, and review expiry.
- Record a capability baseline for every server: tool names, descriptions, input schemas, resource URI patterns, prompt identifiers, transport, authentication mode, package/artifact identity, and expected logging fields.
- Treat any new tool, resource, prompt, schema expansion, resource pattern expansion, transport change, or authorization change as a security-relevant change.
- Default policy for unregistered or changed capabilities is `deny`.

`High-impact/regulated`:
- Require signed artifacts or pinned digests for MCP servers and tool wrappers.
- Mirror approved third-party MCP artifacts into an internal registry or package mirror; production hosts should not install directly from community registries.
- Set review expiry no longer than `90 days` for servers that can modify data, execute code, access sensitive resources, or use third-party infrastructure.

The `90 days` ceiling is a local assumption for an inventory reconciled continuously and after capability changes, with a named owner able to suspend access. It bounds the age of a manual access/provider review; it does not authorize unchecked drift until the next review. Use a shorter interval for unstable providers or greater potential impact. Expired approval blocks high-impact use until renewed.

Verification:
- compare per-request client capabilities and discovered server capabilities against the registry baseline;
- alert on `listChanged` events, unknown servers, unknown tools, schema drift, and resource pattern expansion;
- sample production requests and confirm every tool call maps to an approved registry entry.

### 3.2 Deployment Patterns

Preferred production pattern:
- Use a gateway-mediated deployment for remote MCP wherever possible. The gateway should enforce server allowlists, user/workload authorization, capability filtering, redaction, audit logging, egress policy, rate limits, and emergency disablement.

Local `stdio` servers:
- Allow only approved server binaries/scripts through endpoint management or application allowlisting.
- Run with the least privileged OS identity available for the workflow.
- Restrict filesystem access with OS permissions, a runtime sandbox, and explicit path allowlists. MCP Roots do not enforce access. Do not grant home-directory or repository-wide access by default.
- Maintain an allowlist of environment variables exposed to each server and block credential-bearing variables unless explicitly approved.
- Block outbound network access from local servers unless the server requires it and the destination is approved.

Remote Streamable HTTP servers:
- Validate `Origin` to prevent DNS rebinding; a present invalid origin requires HTTP `403`. Local HTTP servers should bind to loopback, not `0.0.0.0`.
- Require TLS for all traffic.
- Use enterprise-managed authorization aligned with the current MCP authorization profile: OAuth 2.1 draft behavior plus the MCP-required metadata, `resource` parameter, and token audience checks.
- Require PKCE with `S256` for public clients.
- Publish OAuth Protected Resource Metadata and return `WWW-Authenticate` on `401` so clients discover the correct authorization server from the MCP server, not from user-supplied configuration.
- Prefer OAuth Client ID Metadata Documents; use pre-registration for managed clients where appropriate. Dynamic Client Registration is deprecated and retained only for compatibility. Constrain legacy registration by redirect URI, client type, grant, scope, lifetime, and owner; it must not grant broad access without review.
- Require MCP clients to send the OAuth `resource` parameter in both authorization and token requests, using the canonical MCP server URI.
- Validate every present authorization-response `iss` against the recorded authorization-server issuer before redeeming a code, whether or not metadata advertised support. Reject a missing `iss` when `authorization_response_iss_parameter_supported=true`; use exact string comparison after decoding, without URI normalization.
- Validate token issuer, expiry, audience, and scopes on every request. Establish that the token was issued for this MCP server's resource; a `resource` parameter in a client request does not establish that binding by itself.
- Send the access token only in the `Authorization: Bearer <access-token>` header of every protected HTTP request. Prohibit tokens in URL query strings, which can reach logs, browser history, and observability systems.
- Do not pass client access tokens through to downstream APIs. Tool handlers must obtain separate downstream credentials or use a controlled token exchange pattern approved by identity/security owners.
- Do not make `offline_access` or refresh-token issuance part of the MCP resource-server baseline. If an approved client receives a refresh token, it must be sender-constrained or rotated with reuse detection; storage and revocation are separate identity controls. The MCP server must not request or advertise `offline_access` through `WWW-Authenticate` challenges or Protected Resource Metadata `scopes_supported` without an explicitly approved use case.

Third-party MCP servers:
- Require provider onboarding before use: data handling, subprocessors, security contact, vulnerability disclosure, patch SLA, log access, retention, capability-change notification, and exit process.
- Approve the server for a specific environment and use case; approval for development does not imply production approval.

### 3.3 Tool, Resource, and Prompt Controls

Tools:
- Enforce server-side validation for all tool parameters, including type, size, enum, path, URL, identifier, and business state constraints.
- Apply object-level, tenant-level, and action-level authorization inside the tool handler or gateway; never infer authorization from model intent or natural-language instructions.
- Split read and write operations into separate tools with separate scopes and approval policies.
- Require `preview -> explicit confirm -> execute` for state-changing tools unless the exception is approved with owner, expiry, rollback plan, and abuse-case tests.

Resources:
- Restrict resource URI patterns to the narrowest required scope.
- Apply classification, RBAC/ABAC, tenant isolation, DLP/redaction, and audit logging before resource content enters model context.
- Treat externally sourced or user-controlled resource content as untrusted and scan for indirect prompt injection before use.

Prompts:
- Version MCP prompts and review them as code/configuration.
- Do not store secrets, credentials, hidden policy assumptions, customer data, or proprietary implementation details in prompt declarations.
- Log prompt identifier and version, not raw prompt text by default.

Legacy Sampling compatibility:
- Sampling is deprecated; keep it disabled by default and do not add it to new implementations.
- If enabled, restrict it to approved servers, approved model endpoints, maximum prompt size, and redacted/minimized logs.
- Alert on repeated near-duplicate sampling requests, unusual prompt size, or sensitive data classes in sampling payloads.

### 3.4 Logging and Incident Readiness

Log at minimum:
- authenticated user or workload identity;
- host, client, server, gateway, transport, and environment;
- tool/resource/prompt identifier and version;
- scopes and policy decision;
- request ID and correlation ID; application-level state handles where used, without treating them as identity;
- downstream destination and result class;
- redaction status and denial reason where applicable.

Do not log by default:
- raw access tokens or refresh tokens;
- full prompt/context/resource payloads;
- secrets, private keys, session cookies, or full sensitive documents.

Raw payload capture is allowed only in scoped forensic mode with approval, case ID, encryption, restricted access, retention `<=30 days`, and deletion evidence.

This retention ceiling is a local minimization default; choose a shorter period when sufficient. Any legal hold or longer retention requires separate approval, owner, restricted access, and a review date.

The drill target in section 4 is a local assumption that every gateway and server worker supports out-of-band disablement. Measure from acceptance of the operator's command; downstream effects that can cause damage sooner require tighter limits or preventive authorization/transaction controls. Do not claim cancellation of already committed operations.

Incident response must support:
- disabling a server, gateway route, tool, resource, prompt, OAuth client, OAuth grant, and downstream credential independently;
- freezing the MCP registry during active investigation;
- rotating credentials used by affected tool handlers;
- reconstructing an action timeline from gateway, server, IdP, and downstream logs;
- failing dependent workflows gracefully when a tool or server is disabled.

---

### 3.5 Stateless Requests and Transport Validation

MCP `2026-07-28` removes the initialization handshake and protocol sessions. Use `server/discover` for supported versions and capabilities; carry protocol version and client capabilities in request metadata. Do not apply an older session's identity or capability decision to a new request. Re-authorize application state handles and retries for the calling subject.

For Streamable HTTP, validate `MCP-Protocol-Version` against `_meta.io.modelcontextprotocol/protocolVersion`, `Mcp-Method` against `method`, and `Mcp-Name` against the relevant `params.name` or `params.uri`. `Mcp-Method` is required for every request; `Mcp-Name` is required only for `tools/call`, `resources/read`, and `prompts/get`. Do not require a name for `server/discover` or list methods. Reject missing applicable required headers and header/body disagreements before dispatch. Decode permitted Base64 sentinel values before comparing `Mcp-Name` and `Mcp-Param-*`. Mirror only valid `x-mcp-header` declarations; reject invalid declarations and prevent header injection. Unsupported versions must follow the supported-version error/selection path, not silently downgrade.

Broken streams require a new request ID on retry. Use business-level idempotency for state-changing operations; a new JSON-RPC ID alone does not prevent duplicate effects. Keep legacy session/initialization behavior confined to an explicitly versioned compatibility adapter.

When caching capability lists and resources, honor `ttlMs` and `cacheScope`. Results marked `cacheScope: "private"` must not enter a shared intermediary cache. Partition client caches by server, subject, tenant, and effective access context; freshness does not replace authorization at resource read or tool invocation. After access revocation or approved capability changes, do not keep using a cached permission. Verify that a result obtained by user A cannot reach user B through the client or gateway cache.

### 3.6 Elicitation

Form-mode elicitation must not ask for passwords, API keys, access tokens, or payment credentials. Use URL mode for those interactions, keeping third-party credentials out of the MCP client and LLM context. Do not confuse this flow with authorization of the MCP client to the MCP server.

Before navigation, show the complete URL and obtain explicit consent. Do not pre-fetch the URL or its metadata. Open the interaction outside client/model inspection. A URL must not contain sensitive user information or provide pre-authenticated access to a protected resource.

Bind each request and any stored or returned state to the verified user and client. Confirm that the user completing the external flow is the user who initiated it; a copied URL or client-supplied identity is insufficient. Handle decline, cancellation, and failed processing without performing the dependent action. In this revision, elicitation uses `InputRequiredResult` and retry `inputResponses`; protect `requestState` from substitution, and do not treat acceptance as proof that external authorization completed.

---

## 4. Verification

Required evidence:
- MCP registry entry for every production server and capability;
- capability baseline diff from deployment and `server/discover`, plus per-request metadata checks;
- OAuth Protected Resource Metadata, authorization server metadata, `WWW-Authenticate` behavior, `resource` parameter handling, and token validation tests for remote servers;
- Client ID Metadata Document validation or managed pre-registration evidence; policy for DCR only where compatibility requires it;
- endpoint/application allowlisting evidence for local `stdio` servers;
- gateway policy, redaction, and logging configuration;
- provider onboarding record for third-party servers.

Negative tests:
- Invalid `Origin` receives `403`; a DNS-rebinding test cannot reach the local HTTP server through an unapproved origin.
- Missing version/method headers, a missing name where required, mismatched `_meta`, decoded name mismatch, and malformed `Mcp-Param-*` are rejected before tool dispatch; unsupported versions do not silently downgrade.
- A disconnected stream followed by retry cannot duplicate a committed side effect.
- Form requests for each of passwords, API keys, access tokens, and payment credentials are rejected.
- Elicitation URL and metadata receive no request before consent; the full destination remains visible. Sensitive or pre-authenticated URLs are rejected.
- A substituted user/client, copied elicitation URL, or modified `requestState` cannot bind another person's third-party credentials. Credentials never enter client/model traces.
- Decline, cancel, and an unfinished external flow cannot trigger the dependent action.
- Forged Roots cannot widen OS/sandbox access; legacy Sampling remains disabled unless explicitly approved, and unapproved requests are denied.
- DCR cannot activate outside the compatibility policy or obtain wider scopes through self-registration.
- unregistered server is blocked;
- registered server with a new tool or wider resource URI pattern is blocked until approved;
- model-supplied parameter outside schema or business constraints is rejected server-side;
- expired, wrong-audience, wrong-issuer, or insufficient-scope token is rejected;
- missing or wrong OAuth `resource` parameter is rejected or fails to obtain a token usable for the MCP server;
- authorization response with missing or mismatched `iss` is rejected by the MCP client or gateway according to authorization server metadata;
- refresh token issuance or `offline_access` is not requested, required, or advertised without an approved use case;
- token in query string, log field, tool output, or prompt payload is detected and blocked/redacted;
- write tool cannot execute without required confirmation or approval;
- malformed JSON-RPC messages fail closed and produce safe errors;
- local `stdio` server cannot read outside runtime path allowlists or inherit unapproved environment variables.

Operational signals:
- percentage of MCP servers covered by registry baseline;
- percentage of tool calls evaluated by gateway or policy layer;
- alerts for capability drift, unknown servers, abnormal tool sequences, and redaction failures;
- maximum observed time to deny new effects across gateway/server workers during drills, target `<=60s` for high-impact capabilities; record average latency and queued/in-flight cancellation separately;
- provider log export latency and completeness for third-party servers.

---

## 5. Review Decision

The matrix below defines domain severity and the release decision. The [Vulnerability Management playbook](/en/review/vulnerability-management/playbook/) owns generic remediation SLAs, the exception lifecycle, risk acceptance, and closure evidence; where requirements overlap, apply the stricter one.

| Severity | MCP condition | Required action |
|---|---|---|
| Critical | Unapproved MCP server can execute code, modify production data, access secrets, or reach sensitive internal systems | Block release or disable access immediately |
| Critical | Remote MCP token validation accepts wrong issuer/audience/expiry or permits token passthrough to downstream APIs | Block release until fixed and retested |
| High | Capability drift is not detected or new tools/resources become usable without approval | Block high-impact workflows; approve only read-only low-risk use with compensating monitoring |
| High | Tool handler relies on model/client-side validation for privileged parameters | Fix before production for state-changing or sensitive-data tools |
| Medium | Registry exists but lacks owner, review expiry, or downstream destination metadata | Track remediation with owner and due date |
| Medium | Logs support operations but cannot reconstruct identity-to-tool-to-downstream action chains | Improve before broad rollout |
| Low | Naming, descriptions, or prompt metadata are inconsistent but do not expand access | Fix opportunistically |

Release is approved only when every production MCP capability is registered, scoped, authorized, logged, and independently revocable.

---

## 6. Related Materials

- [Securing AI overview](/en/ai-security/securing-ai/overview/)
- [Agentic AI security playbook](/en/ai-security/agentic-ai/playbook/)
- [Threat modeling playbook](/en/review/threat-modeling/playbook/)
- [API security playbook](/en/application-security/api/api-security-patterns/playbook/)
- [OIDC + OAuth 2.0 security guide](/en/application-security/identity/oidc-oauth/playbook/)
