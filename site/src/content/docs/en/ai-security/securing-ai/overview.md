---
title: "Securing AI: Overview"
description: "This overview is aimed at securing live systems:"
editUrl: "https://github.com/defrixx/Product-security-playbook/edit/main/content/ai-security/securing-ai/overview.en.md"
sidebar:
  order: 10
---
## 1. Scope and objective

This overview is aimed at securing live systems:
- AI/LLM assistants and agentic workflows
- RAG and knowledge retrieval
- decisioning models (including antifraud/scoring)
- MLOps/LLMOps and business-system integrations

Objective:
- cover all key security aspects starting from `Zero Trust`
- provide practical, verifiable controls for each aspect

Document ownership:
- This document owns the cross-cutting production control baseline for AI systems.
- It maps AI risks to practical controls, control levels, operational signals, and governance expectations.
- It references the OWASP LLM Top 10 as a taxonomy, but does not re-own the threat catalogue.
- It delegates deep agent autonomy, memory, tool execution, and action-trace requirements to the [Agentic AI security playbook](/Product-security-playbook/en/ai-security/agentic-ai/playbook/).
- It delegates MCP server registry, protocol deployment, OAuth usage, and capability drift controls to the [MCP security playbook](/Product-security-playbook/en/ai-security/mcp-security/playbook/).

---

## 2. Foundational principles

### 2.1 Zero Trust for AI

**Focus:**
- trust no input, output, integration, model, or data source by default

**Practical controls:**
- `Baseline`: explicit trust boundaries for `user -> model -> tool -> downstream` flows
- `Baseline`: `deny-by-default` for tool execution and data access
- `Baseline`: continuous verification of user context (not just at session start)
- `High-impact/regulated`: policy-as-code for authorization and data policies
- `Recommended maturity`: regular threat modeling for agent-flow changes

**Verification signals:**
- percentage of tool calls blocked by policy engine
- trust-boundary test coverage

### 2.2 Control levels and source assumptions

Control labels in this document are requirement profiles, not finding severity:
- `Baseline`: minimum live-environment baseline for the AI system class in scope.
- `High-impact/regulated`: required for autonomous state-changing actions, cross-tenant data access, financial/safety/privacy impact, regulated use cases, or externally exposed AI capabilities.
- `Recommended maturity`: useful for mature programs, higher assurance, or future hardening, but not a default release blocker unless adopted by local policy.

---

## 3. Security aspects and controls

### 3.1 Identity and access (AI IAM)

**Risks:**
- over-privileged agents
- service identity impersonation
- cross-tenant access

**OWASP LLM Top 10 coverage:**
- `LLM06: Excessive Agency`
- `LLM02: Sensitive Information Disclosure`

**Practical controls:**
- `Baseline`: workload identity instead of static keys
- `Baseline`: least privilege per tool and API
- `Baseline`: tenant-aware authorization on every downstream step
- `High-impact/regulated`: short-lived tokens, rotation, audience binding
- `Recommended maturity`: SoD for high-impact operations

**Verification signals:**
- share of services without long-lived credentials
- number of cross-tenant policy denied attempts

### 3.2 Data security and privacy

**Risks:**
- PII/secret leakage via prompt/context/output
- unauthorized data use for training
- retention/regulatory violations

**OWASP LLM Top 10 coverage:**
- `LLM02: Sensitive Information Disclosure`
- `LLM07: System Prompt Leakage`

**Practical controls:**
- `Baseline`: data classification + data handling matrix for AI use cases
- `Baseline`: DLP/redaction before model call and before user response
- `Baseline`: encryption in transit/at rest + tenant isolation
- `Baseline`: classify embeddings, vector stores, memory, cached outputs, and interaction logs as sensitive data even when raw source text is not stored
- `High-impact/regulated`: strict data minimization for inference/training
- `High-impact/regulated`: enforceable retention/deletion controls
- `Recommended maturity`: privacy impact assessment for new AI features

**Verification signals:**
- number of DLP hits per 1k requests
- deletion SLA and on-time completion rate

### 3.3 Model and supply chain security

**Risks:**
- compromised models/adapters
- vulnerable ML dependencies
- legal exposure from licensing terms
- unmanaged AI assets outside normal software and infrastructure inventory

**OWASP LLM Top 10 coverage:**
- `LLM03: Supply Chain`
- `LLM04: Data and Model Poisoning`

**Practical controls:**
- `Baseline`: trusted registry + provenance checks (hash/signature/publisher)
- `Baseline`: inventory AI assets beyond deployed services: model endpoints, prompt/config stores, vector stores, memory stores, evaluation harnesses, tool adapters, MCP servers, provider consoles, and local AI runtimes
- `High-impact/regulated`: SBOM/AI-BOM for model artifacts and runtime
- `Baseline`: CVE scanning + gating for critical vulnerabilities
- `High-impact/regulated`: controlled promotion flow (dev -> staging -> prod) with approvals
- `High-impact/regulated`: legal review for third-party model terms
- `Recommended maturity`: independent red team before live release adoption

**Verification signals:**
- release share with signed artifacts
- inventory coverage for AI assets and owner/review-expiry completeness
- time-to-fix for critical CVEs in AI stack

### 3.4 Prompt, context, and RAG security

**Risks:**
- prompt injection (direct/indirect)
- poisoned knowledge base
- retrieval without ACL and cross-tenant leakage

**OWASP LLM Top 10 coverage:**
- `LLM01: Prompt Injection`
- `LLM08: Vector and Embedding Weaknesses`
- `LLM04: Data and Model Poisoning`

**Practical controls:**
- `Baseline`: strict context separation (trusted vs untrusted)
- `Baseline`: retrieval with document-level/tenant-level authorization
- `Baseline`: ingestion security pipeline (malware/content/policy checks)
- `Baseline`: memory write policy for agents; exclude secrets, tokens, raw regulated data, and unnecessary sensitive fields from working memory, long-term memory, checkpoints, and summaries
- `High-impact/regulated`: detection for jailbreak/injection patterns
- `High-impact/regulated`: prompt template versioning + mandatory security review
- `High-impact/regulated`: semantic recovery tests for vector stores and agent memory so restored context is authorized, current, and not poisoned
- `Recommended maturity`: adversarial test suite in CI/CD

**Verification signals:**
- injection success rate in red-team tests
- share of RAG documents passing policy scan
- memory write rejection rate and vector-store recovery test results

### 3.5 Output and agent-action security

**Risks:**
- unsafe execution of model output
- unwanted transactions and destructive actions
- escalation through tool chains

**OWASP LLM Top 10 coverage:**
- `LLM05: Improper Output Handling`
- `LLM06: Excessive Agency`

**Practical controls:**
- `Baseline`: always treat output as untrusted input
- `Baseline`: schema validation + allowlisted commands/operations
- `Baseline`: two-step execution for state-changing actions (`preview -> explicit confirm -> execute`)
- `High-impact/regulated`: human-in-the-loop + four-eyes approval for high-impact/irreversible operations
- `High-impact/regulated`: sandbox for code/command execution
- `High-impact/regulated`: rate limits, loop guards, kill switch with starting guardrails (`max tool-chain depth=3`, `max autonomous steps=5`, `request budget=60 req/min per user`, `token budget=20k tokens/request`)
- `Recommended maturity`: transaction risk scoring before execution

Applicability matrix for numeric guardrails:

| AI workflow class | Starting default | Hard cap | Exception rule | Verification signal |
|---|---|---|---|---|
| Public assistant without state-changing tools | `60 req/min per user`, `20k tokens/request`, no autonomous tool chain by default | Tenant/IP cost quota, max context and streaming duration per product tier | Higher limits require abuse/cost model, tenant quota, and alert owner | 429 rate, spend per tenant, prompt-flood detection, context-window rejection tests |
| Internal copilot with read-only tools | `max tool-chain depth=3`, `max autonomous steps=5`, `20k tokens/request` | Tool calls only to approved read-only systems; no cross-tenant or live-write actions | Wider retrieval/tool access requires data-owner approval and audit sampling | Policy-denied tool calls, retrieval ACL test pass rate, sampled audit events |
| Autonomous state-changing agent | `preview -> explicit confirm -> execute`; default autonomous execution disabled for high-impact actions | `max autonomous steps=3` before re-authorization; kill switch SLO `<=60s`; no irreversible action without human approval | Any no-confirm action needs owner, expiry, rollback plan, and abuse-case tests | Unauthorized-action negative tests, approval coverage, mean time to kill runaway actions |
| Batch/RAG ingestion or offline processing | Budget by job, tenant, corpus, and source; no per-chat request budget assumption | Max documents, max tokens per document, max runtime, max outbound fetches, and quarantine threshold | Larger batch requires staging run, cost estimate, malware/content scan, and source trust decision | Poisoned-document test results, ingestion reject rate, job cost variance, quarantine metrics |

Treat these numbers as local starting baselines. Tune them by model context window, streaming mode, batch size, tenant tier, cost profile, tool risk, and downstream blast radius; record the chosen values in the release gate. A small numeric limit is not safe if one allowed tool call can perform a destructive operation, and a larger limit can be acceptable for tightly scoped read-only tools. The release gate must assess blast radius per step, not only the number of steps or tokens.

**Verification signals:**
- number of blocked risky action attempts
- share of requests blocked by guardrail budget limits
- mean time to kill in runaway-agent scenarios (SLO: `<=60s`)

### 3.6 MCP and agent tool protocol security

**Risks:**
- untrusted MCP/tool servers entering the agent runtime
- tool manifest poisoning or silent tool-scope expansion
- shadow tools, context over-sharing, and token leakage in protocol logs

**OWASP LLM Top 10 coverage:**
- `LLM06: Excessive Agency`
- `LLM02: Sensitive Information Disclosure`
- `LLM03: Supply Chain`

**Practical controls:**
- `Baseline`: maintain an approved inventory for MCP servers and agent tools, including owner, environment, allowed clients, data classes, downstream destinations, and review expiry
- `Baseline`: deny-by-default tool discovery; live agents may use only registered tools from approved transports and trust boundaries
- `Baseline`: authorize every tool call with user/workload identity, tenant, action, data class, and workflow state before execution
- `Baseline`: use per-tool scopes and short-lived credentials; secrets must not appear in prompts, tool descriptions, context payloads, or protocol traces
- `High-impact/regulated`: require a dedicated MCP/agentic review for tools that can change business state, access sensitive data, execute code, browse external content, or move data across trust boundaries
- `High-impact/regulated`: detect unknown tools, manifest/capability drift, abnormal tool chains, redaction failures, and unusual cross-tool data movement

Canonical details:
- MCP protocol deployment, `stdio`/remote server handling, token passthrough rules, gateway policy, `listChanged` handling, and protocol-layer logging are owned by the [MCP security playbook](/Product-security-playbook/en/ai-security/mcp-security/playbook/).
- Agent autonomy, memory, action traces, approvals, rollback, and kill-switch behavior are owned by the [Agentic AI security playbook](/Product-security-playbook/en/ai-security/agentic-ai/playbook/).

**Verification signals:**
- inventory coverage for MCP servers and registered tools
- percentage of tool calls evaluated by policy before execution
- alerts for unknown tools, capability drift, redaction failures, and abnormal tool sequences

### 3.7 Infrastructure and runtime security

**Risks:**
- compromise of inference/training environments
- lateral movement inside platform
- uncontrolled egress

**OWASP LLM Top 10 coverage:**
- `LLM10: Unbounded Consumption`
- `LLM03: Supply Chain`

**Practical controls:**
- `Baseline`: node/container hardening (seccomp, runtime policies)
- `Baseline`: network segmentation and egress allowlisting
- `Baseline`: centralized vault-based secrets management
- `High-impact/regulated`: EDR/runtime detection for AI workloads
- `High-impact/regulated`: immutable logs + centralized SIEM
- `Recommended maturity`: confidential compute for sensitive scenarios

**Verification signals:**
- runtime policy coverage across AI workloads
- number of egress-deny events in AI namespaces

### 3.8 AppSec for AI applications

**Risks:**
- classic web/API vulnerabilities + AI-specific attack chains
- unsafe frontend rendering of model output
- SSRF/XSS/SQLi via LLM-mediated paths
- agent browser, file, email, and code-execution tools becoming untrusted ingestion and execution paths

**OWASP LLM Top 10 coverage:**
- `LLM05: Improper Output Handling`
- `LLM01: Prompt Injection` (in LLM-mediated flows)

**Practical controls:**
- `Baseline`: secure coding baseline for web/API code plus AI-specific checks
- `Baseline`: parameterized queries + context-aware output encoding
- `Baseline`: CSP/HTML sanitization for LLM content
- `Baseline`: run browser automation, URL fetchers, file parsers, and code interpreters in isolated sandboxes with deny-by-default egress and no default access to internal networks, host files, metadata services, or production credentials
- `Baseline`: scan and sanitize downloaded files, HTML, PDFs, email content, and retrieved web content before they enter memory, RAG, or execution tools
- `High-impact/regulated`: SAST/DAST/IAST profiles for AI endpoints
- `High-impact/regulated`: human approval before third-party code execution, package installation, shell commands, or file operations outside a temporary workspace
- `Recommended maturity`: security contract tests between AI gateway and downstream APIs

**Verification signals:**
- high-severity findings discovered before release
- AI endpoint coverage in automated security testing
- sandbox escape, egress-deny, and malicious-content rejection test results

### 3.9 Monitoring, detection, and incident response

**Risks:**
- late detection of abuse/prompt attacks/data leakage
- lack of AI-specific incident playbooks

**OWASP LLM Top 10 coverage:**
- cross-functional coverage of `LLM01`–`LLM10` through detection and response

**Practical controls:**
- `Baseline`: audit trail for prompts, retrieval, tool calls, policy decisions with field-level data minimization
- `Baseline`: action trace for agent workflows that correlates model calls, retrieval events, memory writes, tool invocations, policy decisions, approvals, downstream actions, and final output
- `Baseline`: secret/PII masking and redaction in logs before storage
- `Baseline`: keep raw prompt/context/tool payload logging disabled by default; use redacted/minimized logs for normal operations
- `Baseline`: keep raw payload capture limited to scoped forensic mode with approval, break-glass access, case ID, encryption, retention `<=30 days`, deletion evidence, and DLP/redaction where possible
- `Baseline`: detection rules for injection, privilege misuse, data exfiltration
- `Baseline`: confirm provider-managed AI runtimes expose enough logs, retention controls, export capability, memory isolation, and emergency disablement before production use
- `High-impact/regulated`: AI incident runbooks (containment, rollback, customer comms)
- `High-impact/regulated`: tabletop exercises for realistic AI attack paths
- `Recommended maturity`: continuous purple teaming

**Verification signals:**
- MTTD/MTTR for AI security events
- percentage of incidents handled with runbook compliance
- share of raw-payload logs deleted on time per retention policy
- percentage of high-impact agent actions reconstructable from redacted action traces

### 3.10 Governance, risk, and compliance

**Risks:**
- uncontrolled rollout of AI features
- non-compliance with internal policy and regulations

**OWASP LLM Top 10 coverage:**
- cross-functional coverage of `LLM01`–`LLM10` through release gates and risk ownership

**Practical controls:**
- `Baseline`: AI risk register with owner and remediation due dates
- `Baseline`: release gate for security/privacy/compliance criteria
- `High-impact/regulated`: model cards + system cards for high-risk use cases
- `High-impact/regulated`: third-party risk assessment for AI vendors
- `Recommended maturity`: quarterly control effectiveness review

**Verification signals:**
- release share passing AI risk gate without exception
- number of overdue remediation actions

### 3.11 Safety and abuse resilience

**Risks:**
- harmful output, misuse, business-logic abuse
- in antifraud scenarios: adversarial adaptation and detector bypass

**OWASP LLM Top 10 coverage:**
- `LLM09: Misinformation`
- `LLM10: Unbounded Consumption` (abuse/automation loops)
- `LLM04: Data and Model Poisoning` (for model manipulation)

**Practical controls:**
- `Baseline`: policy filters for harmful/disallowed intents
- `Baseline`: safeguarded fallback to deterministic business logic
- `High-impact/regulated`: abuse monitoring by user/device/session behavior
- `High-impact/regulated`: regular threshold calibration for fraud/risk models
- `Recommended maturity`: attacker-in-the-loop simulations

**Verification signals:**
- false negative/false positive rates in abuse/fraud cases
- model drift indicators and drift response time

---

## 4. Operating model for implementation

### 4.1 Minimum RACI

- Product: owner of AI feature business risk
- Security/AppSec: owner of security requirements and release gates
- ML/AI Engineering: owner of model lifecycle and technical controls
- Platform/SRE: owner of runtime hardening, observability, and IR readiness
- Legal/Privacy: owner of data-use terms and privacy controls

### 4.2 Mandatory release artifacts

- threat model for the AI feature
- policy matrix (`who/what/can-do`)
- data flow + data classification
- AI asset inventory entry, including owner, autonomy level, tools, memory/retrieval stores, provider/runtime, and review expiry
- model/supply chain provenance package
- action-trace schema and kill-switch/rollback evidence for agentic workflows
- test evidence (security + abuse + resilience)

### 4.3 LLMSecOps lifecycle gates

**Scope & Plan:**
- `Baseline`: define the business use case, data classes, user groups, trust boundaries, and disallowed actions before selecting a model or vendor
- `Baseline`: perform third-party risk assessment for model/provider/tooling, including data usage, retention, training opt-out, residency, and incident notification
- `High-impact/regulated`: document model selection rationale, task suitability, and fallback strategy for cases where deterministic logic is safer than an LLM

**Augment, fine-tune, data:**
- `Baseline`: validate training/fine-tuning/RAG data sources for usage rights, freshness, malware/content risk, and tenant boundaries
- `Baseline`: protect the data pipeline and vector database as live data stores: document-level authorization, audit trail, encryption, backup/restore, and deletion workflow
- `High-impact/regulated`: version datasets, embeddings, prompt templates, and retrieval policies so incident response can roll back context, not only code

**Develop & experiment:**
- `Baseline`: apply the secure coding baseline to the AI gateway, tool adapters, prompt orchestration, and downstream integrations, not only to the web/API wrapper
- `Baseline`: register MCP/tool servers before use; unregistered local, shadow, or developer-only tools must not be reachable from live agents
- `High-impact/regulated`: track experiments with model, parameters, prompt version, dataset snapshot, evaluator version, and security findings
- `High-impact/regulated`: isolate developer sandboxes from live data and live tools; handle exceptions as temporary break-glass access

**Test & evaluate:**
- `Baseline`: include adversarial testing, prompt-injection tests, authorization tests for tools/RAG, and output-handling tests in release evidence
- `High-impact/regulated`: run incident simulation and response testing for data leakage, runaway agent, compromised model artifact, and poisoned RAG source scenarios
- `Recommended maturity`: benchmark not only quality/latency/cost, but also refusal behavior, jailbreak resistance, data leakage rate, and policy false positives

**Release:**
- `High-impact/regulated`: produce an AI-BOM/SBOM for model artifacts, datasets where applicable, prompt/runtime components, dependencies, and external services
- `Baseline`: sign and verify model/dataset artifacts; allow promotion to live environments only from a trusted registry
- `High-impact/regulated`: perform model security posture evaluation before live release promotion and after a material model/provider change

**Deploy:**
- `Baseline`: validate runtime configuration, secrets, network egress, API exposure, tenant isolation, and user/machine access before enabling live traffic
- `Baseline`: verify model and dataset artifact signatures/provenance during deployment, not only in CI
- `Baseline`: verify MCP/tool manifest identity, version, transport, scopes, and outbound destinations before enabling agent access
- `High-impact/regulated`: enable fallback, rollback, and kill switch before launching autonomous or high-impact tool flows

**Operate:**
- `Baseline`: keep runtime guardrails, rate limits, budget limits, output validation, and tool policy enforcement enabled continuously, including degraded mode
- `High-impact/regulated`: use patch/update alerts for model providers, AI frameworks, vector databases, model serving, and orchestration components
- `High-impact/regulated`: regularly tune risk scoring for agent actions based on real denied events and incident learnings

**Monitor:**
- `Baseline`: collect security metrics for adversarial input, tool denial, policy bypass attempts, data leakage signals, anomaly in agent chains, and model behavior drift
- `Baseline`: alert on unknown MCP servers, tool manifest drift, abnormal tool chains, and token/secret patterns in protocol logs
- `High-impact/regulated`: route alerts to Security/SRE/Product with severity, owner, and runbook; AI alerts without an owner quickly become noise
- `Recommended maturity`: track ethical/compliance signals where they are live-environment risks: bias, unfair denial, regulated advice, unsafe recommendations

**Govern:**
- `Baseline`: conduct user/machine access audits for AI tools, model registries, prompt repositories, vector stores, and provider consoles
- `Baseline`: retain audit evidence for model decisions, dataset versions, prompt/system changes, exceptions, and incident governance
- `High-impact/regulated`: review the AI risk register at least quarterly and on major model/provider change

---

## 5. Related Materials

- [OWASP LLM Top 10 threat overview](/Product-security-playbook/en/ai-security/owasp-llm-top-10/overview/)
- [Agentic AI security playbook](/Product-security-playbook/en/ai-security/agentic-ai/playbook/)
- [MCP security playbook](/Product-security-playbook/en/ai-security/mcp-security/playbook/)
- [Threat modeling playbook](/Product-security-playbook/en/review/threat-modeling/playbook/)
- [API security playbook](/Product-security-playbook/en/application-security/api/api-security-patterns/playbook/)
- [Secure coding and code review playbook](/Product-security-playbook/en/application-security/secure-coding/code-review/playbook/)
