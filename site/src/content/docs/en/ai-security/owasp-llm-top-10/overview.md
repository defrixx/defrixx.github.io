---
title: "OWASP Top 10 for LLM Applications (2026): Overview"
description: "This overview is a threat-focused summary of OWASP Top 10 for LLM Applications (2026)."
sidebar:
  order: 20
---
## 1. Scope

This overview is a threat-focused summary of OWASP Top 10 for LLM Applications (2026).

This overview focuses on:
- how each threat emerges in real systems
- what technical and business risks it creates
- what adjacent risks can amplify impact

Document ownership:
- This document owns the threat taxonomy and risk vocabulary for LLM application reviews.
- It explains prompt injection, data leakage, tool abuse, excessive agency, and related risks as categories and attack mechanics.
- It does not define the production control baseline; use [Securing AI](/en/ai-security/securing-ai/overview/) for controls, implementation priorities, and verification signals.
- It does not replace the specialized playbooks for agent autonomy or MCP protocol governance.

The 2026 taxonomy covers a model used as an application component. When the model acts through tools, retains memory, coordinates with other agents, or autonomously causes downstream effects, pair this taxonomy with the OWASP Top 10 for Agentic Applications.

---

### 1.1 Version map and stable links

Use the 2026 identifiers in new threat models, findings and coverage records. The section order retains the previous layout and explicit legacy anchors preserve 2025 links; section positions are not risk ranks. Record the edition with every LLM identifier. Update linked control maps and navigation together rather than reinterpreting an old finding's number.

| Category | 2025 | 2026 |
| --- | --- | --- |
| Prompt Injection | LLM01 | LLM01 |
| Sensitive Information Disclosure | LLM02 | LLM02 |
| Supply Chain | LLM03 | LLM04 |
| Data and Model Poisoning | LLM04 | LLM05 |
| Improper Output Handling | LLM05 | LLM10 |
| Excessive Agency | LLM06 | LLM03 |
| System Prompt Leakage / Hidden Context Exposure | LLM07 | LLM08 |
| Vector and Embedding Weaknesses | LLM08 | LLM09 |
| Misinformation | LLM09 | LLM07 |
| Unbounded Consumption | LLM10 | LLM06 |

The 2026 Hidden Context Exposure category covers extraction, inference and reconstruction of hidden operational context as well as system instructions. Classify its impact by the sensitivity of the exposed information and the attacker capability it enables, not by disclosure of instruction text alone.

## 2. Threat context (how LLM incidents happen in reality)

Most incidents are failures at trust boundaries between components:
- user input -> model
- external content -> RAG/indexing -> model
- model output -> tools/API/DB
- model runtime -> cost/quotas/infrastructure
- model lifecycle -> datasets/adapters/registries/deployment

In real reviews, these areas are non-negotiable:
- IAM and authorization for tools and downstream systems
- data classification and handling (PII, secrets, etc.)
- secure output processing before execution/rendering
- provenance and integrity of models/adapters/datasets

---

## 3. Threat-focused breakdown of OWASP LLM Top 10

This document intentionally focuses on threats, attack mechanics, and risks.
For practical controls, implementation priorities, and verification signals, see [Securing AI](/en/ai-security/securing-ai/overview/). For agent autonomy, memory, tool execution, and action traces, use the [Agentic AI security playbook](/en/ai-security/agentic-ai/playbook/). For MCP server registry, protocol deployment, OAuth usage, and capability drift, use the [MCP security playbook](/en/ai-security/mcp-security/playbook/).

<a id="31-llm01-prompt-injection"></a>

## 3.1 LLM01:2026 Prompt Injection

Include injected instructions retained in memory or forwarded across retrieval, multimodal inputs and agent boundaries; a trusted-looking wrapper does not change their origin.

### Summary (OWASP)
A vulnerability where input (including hidden or external content) changes LLM behavior against expected rules and can lead to unauthorized actions.

### How it appears in live environments
- hidden instructions in documents, web pages, emails, images
- prompts like "ignore previous instructions"
- obfuscation (encodings, multilingual payloads, split payload)

### Main risks
- unauthorized tool invocation
- exfiltration of sensitive data
- manipulation of decisions in business processes

---

<a id="32-llm02-sensitive-information-disclosure"></a>

## 3.2 LLM02:2026 Sensitive Information Disclosure

Inspect reasoning/observability output, caches and derived artifacts as disclosure paths; an embedding or summary does not remove the source data sensitivity.

### Summary (OWASP)
Risk of exposing sensitive information (PII, secrets, internal data, intellectual property) via LLM responses, context, training, or insecure data handling.

### How it appears in live environments
- leakage of PII/secrets from chat history in responses
- confidential data entering training/fine-tuning
- disclosure of internal configs and diagnostic details

### Main risks
- privacy breach and regulatory penalties
- credential compromise and lateral movement
- intellectual property and trade secret leakage

---

<a id="33-llm03-supply-chain"></a>

## 3.3 LLM04:2026 Supply Chain

### Summary (OWASP)
Compromise or misrepresentation of models, adapters, datasets, dependencies, tools, and deployment artifacts across the LLM supply chain.

### How it appears in live environments
- vulnerable or malicious ML/LLM dependencies and serialized artifacts
- an untrusted base model, LoRA adapter, converter, or third-party tool package
- a promoted model artifact whose identity, provenance, or integrity was not verified

### Main risks
- backdoored behavior or malicious code execution in training/inference environments
- substitution between evaluated and deployed artifacts
- licensing, privacy, and compliance exposure from opaque sources

---

<a id="34-llm04-data-and-model-poisoning"></a>

## 3.4 LLM05:2026 Data and Model Poisoning

### Summary (OWASP)
Poisoning of pre-training, fine-tuning, feedback, or retrieval data, or direct manipulation of model artifacts, introduces triggers, biases, or unsafe behavior that persists into production.

Training-data poisoning can embed unsafe behavior in model parameters. RAG corpus poisoning acts through retrieved content: changing a response does not require changing model weights. These paths can overlap with prompt injection, but require reviewing different parts of the data lifecycle.

### How it appears in live environments
- poisoned training, fine-tuning, or preference datasets
- fine-tuning subversion and trigger-based backdoors
- malicious documents or embeddings entering a RAG corpus

### Main risks
- integrity loss, targeted bias, manipulation, or toxic output
- persistent backdoor behavior activated by a trigger
- fraud and unsafe automation in downstream processes

---

<a id="35-llm05-improper-output-handling"></a>

## 3.5 LLM10:2026 Improper Output Handling

Rendering output can automatically load external URLs or resources and leak context even without script execution; inspect Markdown, image and document clients as downstream consumers.

### Summary (OWASP)
Insufficient validation, sanitization, and contextual encoding of LLM output before it reaches consumer systems turns model responses and generated code into injection or execution paths.

Here, downstream systems means any component that consumes LLM output and performs an action: databases, APIs, shell runners, template engines, browser renderers, workers, and automation pipelines.

### How it appears in live environments
- model output sent directly to shell, API, SQL, or a template renderer
- generated HTML, JavaScript, or Markdown rendered without contextual sanitization
- generated code or package recommendations accepted without security verification

### Main risks
- XSS, SQL injection, SSRF, command injection, or RCE in downstream components
- vulnerable generated code propagated at scale
- supply-chain compromise through hallucinated packages

---

<a id="36-llm06-excessive-agency"></a>

## 3.6 LLM03:2026 Excessive Agency

### Summary (OWASP)
Excessive functionality, permissions, or autonomy allows model output to trigger damaging actions, especially when prompt injection or misinformation reaches tools and downstream systems.

### How it appears in live environments
- the application exposes tools that are not required for the task
- tool credentials or permissions exceed the initiating user's scope
- irreversible or externally visible actions execute without deterministic authorization or confirmation

### Main risks
- unauthorized changes, deletions, messages, or transactions
- cross-tenant access through an over-privileged execution identity
- prompt injection or false output acquiring a much larger blast radius

---

<a id="37-llm07-system-prompt-leakage"></a>

## 3.7 LLM08:2026 Hidden Context Exposure

### Summary (OWASP)
Hidden Context Exposure includes unauthorized extraction, inference or reconstruction of system/developer instructions, retrieved policy text, tool schemas and other non-user-facing operational context. Exposure matters when it reveals sensitive information or logic that increases attacker capability. Disclosure of the prompt text alone does not establish a vulnerability: the underlying risk is exposed sensitive data or security decisions delegated to the model. Authorization and privilege boundaries must hold even when the instructions are known.

### How it appears in live environments
- extraction of system prompts, developer instructions, or retrieved policy text
- disclosure of tool/function schemas, refusal logic, roles, or workflow rules
- credentials or security-critical configuration embedded in model-visible context

### Main risks
- targeted bypass of guardrails and more effective prompt injection
- exposure and reuse of embedded credentials
- privilege escalation or unsafe output manipulation using disclosed policy and tool details

---

<a id="38-llm08-vector-and-embedding-weaknesses"></a>

## 3.8 LLM09:2026 Vector and Embedding Weaknesses

Manipulation of embedding geometry or retrieval ranking can select attacker-controlled context without changing model weights; distinguish relevance from authorization.

### Summary (OWASP)
Weaknesses in generating, storing, authorizing, and retrieving embeddings and vectors, especially in RAG, lead to cross-tenant leakage, poisoned context, unauthorized access, and reconstruction of source data.

### How it appears in live environments
- cross-tenant retrieval from a shared vector index
- authorization applied after retrieval instead of inside the index query
- embedding inversion, membership inference, and poisoned retrieval content

### Main risks
- confidential data leakage or source reconstruction
- response manipulation through poisoned context
- legal and compliance exposure from improperly governed data sources

---

<a id="39-llm09-misinformation"></a>

## 3.9 LLM07:2026 Misinformation

### Summary (OWASP)
Plausible but false, misleading, or unsupported output causes users or downstream systems to make incorrect decisions or perform unsafe actions.

### How it appears in live environments
- confident false claims in legal, medical, financial, or operational workflows
- fabricated evidence, citations, completion status, or nonexistent packages
- users or automation treating model output as authoritative without verification

### Main risks
- user harm and incorrect business or security decisions
- reputational, contractual, and legal damage
- supply-chain compromise through hallucinated dependencies

---

<a id="310-llm10-unbounded-consumption"></a>

## 3.10 LLM06:2026 Unbounded Consumption

Include reasoning-token and multimodal-processing costs, repeated failed calls and work that continues after client cancellation; input size alone does not bound resource use.

### Summary (OWASP)
Uncontrolled use of requests, context, tokens, inference, tools, or recursive workflows causes availability loss, denial of wallet, capacity exhaustion, or model extraction.

### How it appears in live environments
- prompt flooding, oversized context, long sessions, or expensive repeated inference
- parallel, recursive, or tool-mediated loops without budgets
- high-volume API probing intended to extract model behavior or weights

### Main risks
- service degradation and denial of service
- uncontrolled spend and shared-capacity starvation
- model theft and intellectual-property loss

---

## 4. Threat Differentiation Summary

- `LLM01 Prompt Injection`: attacks execution instructions; key distinction is behavioral control of the model through input content.
- `LLM02 Sensitive Information Disclosure`: leaks sensitive data in outputs; distinction is confidentiality impact rather than action control.
- `LLM04 Supply Chain`: compromises or misrepresents external artifacts and dependencies; distinction is risk entering through the delivery chain.
- `LLM05 Data and Model Poisoning`: poisons training, fine-tuning, feedback, or retrieval data; distinction is persistent behavior manipulation through model inputs or artifacts.
- `LLM10 Improper Output Handling`: passes model output unsafely to a consumer; distinction is the integration boundary after generation.
- `LLM03 Excessive Agency`: grants excessive functionality, permissions, or autonomy; distinction is that model output can reach privileged actions.
- `LLM08 Hidden Context Exposure`: exposes or reconstructs sensitive instructions and hidden operational context; distinguish disclosure of prompt text from exposed secrets or authorization delegated to the model.
- `LLM09 Vector and Embedding Weaknesses`: exploits authorization, integrity, and confidentiality failures in retrieval and embedding storage.
- `LLM07 Misinformation`: produces plausible but false or unsupported content; distinction is decision-quality and downstream trust.
- `LLM06 Unbounded Consumption`: permits uncontrolled resource use; distinction is availability, capacity, cost, and extraction impact.

---

## 5. Related Materials

- [Securing AI overview](/en/ai-security/securing-ai/overview/)
- [Agentic AI security playbook](/en/ai-security/agentic-ai/playbook/)
- [MCP security playbook](/en/ai-security/mcp-security/playbook/)
- [Threat modeling playbook](/en/review/threat-modeling/playbook/)
- [API security playbook](/en/application-security/api/api-security-patterns/playbook/)
