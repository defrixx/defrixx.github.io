# Knowledge assistant: external LLM and RAG

Local learning route, version 0.1. The example is synthetic; checks on your system are not executed here.

Assess internal knowledge retrieval before connecting an external model. Separate an employee’s right to read a document from organizational permission to disclose its content to a provider.

## When to use and expected result

Employees ask questions about internal documents and excerpts are sent to an external model.

Knowledge-access model, provider data contract, revocation/injection checks, worked review and templates.

## Inputs

- Document classes, owners, permitted recipients and authoritative ACL/membership sources.
- Ingestion, chunking, indexing, retrieval and ranking; identify embedding, reranking and generation providers separately.
- User/tenant model, ACL/document revisions, caches, conversation history, citations, logs and backups.
- Exact provider service, endpoint, region and controls: data use, retention, service logs, subprocessors and deletion. Do not transmit restricted documents without a confirmed contract.
- Accepted revocation/deletion propagation time, evidence method, request/context limits and application/model/policy revisions.

## Decisions and trust boundaries

| Decision | Boundary |
| --- | --- |
| Where data travels | A local index does not imply local processing: embedding and ranking may also transmit text. |
| What may be read | Derive identity/rights from the trusted session. Apply ACL filtering and freshness checks before any external stage receives a chunk. |
| What may be sent | User access does not override data-class, region or service restrictions. Unknown policy blocks transmission. |
| What revocation means | Block new answers, cache reuse and stale history; separately erase derived copies. Text already read by a human cannot be technically recalled. |

## Workflow

1. Map every data copy, including embeddings, ranking, history and traces; assign boundary owners.
2. Select allowed fields/classes and provider controls. Compare actual network requests with the approved content.
3. Enforce server-side ACL/source-version checks before releasing context; test allowed users, foreign tenants and revoked groups.
4. Separately test injected instructions, citations and safe rendering. Document text receives no application authority.
5. Exercise revocation/deletion across index, cache and history while observing provider requests; complete the matrix and human decision.

## Requirements and observable expectations

IDs belong to the chosen model, not a corporate standard. Establish applicability and test allowed/rejected cases for each requirement.

| ID | Area | Requirement | Allowed case / result | Negative case / result |
| --- | --- | --- | --- | --- |
| RAG-001 | Identity and scope | Derive user, tenant and current groups on the server; request filters are not authoritative. | Allowed OPS-17 question: Only permitted chunks enter the answer | Spoof tenant/group in the request: No foreign chunk, identifier or title disclosed |
| RAG-002 | Authorization before disclosure | Enforce ACLs before external embedding/ranking/generation, not after the answer. | Retrieve an authorized source: Observed external request matches authorized context | Highly relevant SEC-42 is forbidden: No external stage receives the forbidden excerpt |
| RAG-003 | Source binding | Bind chunks to source/version/ACL; check updates and forged provenance. | Update an allowed document: Use verified version and citation | Forge document_id or stale ACL: Unknown/stale binding is blocked |
| RAG-004 | Provider contract | Verify data class, service, region, retention and effective controls for all external stages. | Approved fields at selected endpoint: Disclosure matches recorded contract | Unknown retention or provider switch: Restricted data blocked pending a new decision |
| RAG-005 | Untrusted context | Documents are data; their instructions cannot change policy, destination or authority. | Ordinary question and quoted text: Answer retains provenance; no actions | Document requests exporting SEC-42 to an external URL: No forbidden context or network effect; answer manipulation tracked separately |
| RAG-006 | Output and links | Constrain rendering/citations; do not execute HTML/code or auto-fetch external resources. | Answer with an allowed citation: Citation opens under fresh authorization | HTML, foreign citation or external tracking image: No execution/automatic request; foreign source not exposed |
| RAG-007 | Cache and history | Reauthorize cached/history content, isolate users and track policy revisions. | Repeat an allowed question: Cache preserves access scope | Another user or group revoked before reuse: Cache/history cannot bypass current rights |
| RAG-008 | Revocation and deletion | Define revocation propagation, block stale context; separately track erasure of source and derived copies. | Delete document and complete agreed workflow: Index/cache/copies and deletion receipts accounted for | Revocation during request; provider deletion unconfirmed: New context blocked; incomplete erasure remains visible |
| RAG-009 | Secrets and observability | Keep keys outside context; minimize logs and protect trace access/retention. | Diagnose a synthetic request: IDs/versions/metrics without secrets or raw text by default | Provider error or verbose tracing: No keys or restricted excerpts disclosed |
| RAG-010 | Evaluation and shutdown | Version model/settings/policy; test benign/adversarial cases, budgets and external-transfer shutdown. | Baseline suite after a model update: Version-bound outcomes include benign usefulness | New model, budget exhaustion or emergency stop: No policy bypass/new disclosure; unexecuted cases not-run |

## Example, templates and evidence

[Open synthetic review example](../reviews/llm-rag/overview.en.md).

<!-- hub:llm-rag-downloads -->

The matrix contains 20 starter cases with IDs. Split compound scenarios into separate runs/observations before execution. Establish a valid allowed baseline: rejections alone do not establish usefulness.

Link requirement, test ID, finding, baseline revision, proposed/applied repair and a separate recheck. Initial outcomes are `not-run` with empty observations. `pass`/`fail` need observed evidence; `inconclusive` preserves uncertainty. `not-applicable` needs a reason/owner and is not an exception to an applicable rule.

Exceptions record scope, objects/revision, expiry, compensating measures and approving human. They cannot make an access-boundary failure pass. Hand residual risk/unexecuted checks to a human; the site makes no real release decision.

## Working references

- [Securing AI features](../../ai-security/securing-ai/overview.en.md)
- [LLM threats](../../ai-security/owasp-llm-top-10/overview.en.md)
- [Review and recheck](../catalogue/overview.en.md)

Our independent skills support review and separately authorized repair verification. Consult the catalogue for inputs/tool limits; a skill does not automatically connect to your model, MCP server or Kafka.

Author: Defrixx. Original prose, diagram and templates: CC BY 4.0. [Usage and licenses](../usage/overview.en.md).
