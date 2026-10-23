# Product Security Playbook

A practical knowledge base for reviewing architecture, code, platforms, and engineering workflows.

The playbooks, checklists, and review methods help apply industry standards and engineering practices to specific product security tasks.

Materials evolve with technologies and attack techniques. Apply them in the context of your project's architecture, component versions, and threat model.

---

## Contents

### Review and Governance
- [`content/review/`](content/review/) - [choose a document by task](content/review/overview.en.md)
- [`content/review/architecture/`](content/review/architecture/) - security architecture review checklist
- [`content/review/threat-modeling/`](content/review/threat-modeling/) - threat modeling methodology review and practical playbook
- [`content/review/release-governance/`](content/review/release-governance/) - release governance and security quality gates for protected environments, deployment approvals, release evidence, exceptions, and escalation
- [`content/review/vulnerability-management/`](content/review/vulnerability-management/) - vulnerability triage, external reports and coordinated disclosure, exploitability, SLA, release blocking, exceptions, and closure evidence

### Application Security
- [`content/application-security/`](content/application-security/) - [choose a document by task](content/application-security/overview.en.md)
- [`content/application-security/web/owasp-top-10/`](content/application-security/web/owasp-top-10/) - web control catalogue with OWASP Top 10:2021 and 2025 mappings
- [`content/application-security/web/browser-security/`](content/application-security/web/browser-security/) - browser and frontend controls for CSP, CORS, cookies, third-party scripts, embedded content, and frontend supply chain
- [`content/application-security/api/api-security-patterns/`](content/application-security/api/api-security-patterns/) - API security and integration patterns for REST, SOAP/XML, GraphQL, Webhooks, and gRPC
- [`content/application-security/business-logic/business-logic-abuse/`](content/application-security/business-logic/business-logic-abuse/) - business logic abuse playbook for ATO, signup/trial/promo abuse, tenant isolation, workflow abuse, and sensitive business flows
- [`content/application-security/secure-coding/code-review/`](content/application-security/secure-coding/code-review/) - secure coding and code review playbook for validation, encoding, auth/session, access control, injection, file handling, logging, crypto misuse, and review evidence
- [`content/application-security/identity/oidc-oauth/`](content/application-security/identity/oidc-oauth/) - OIDC + OAuth 2.0 security playbook

### Platform Security
- [`content/platform-security/`](content/platform-security/) - [choose a document by task](content/platform-security/overview.en.md)
- [`content/platform-security/kubernetes/cluster-security-review/`](content/platform-security/kubernetes/cluster-security-review/) - Kubernetes cluster security review playbook
- [`content/platform-security/kubernetes/adversarial-validation/`](content/platform-security/kubernetes/adversarial-validation/) - Kubernetes adversarial validation and attack-path review playbook
- [`content/platform-security/kubernetes/pod-security/`](content/platform-security/kubernetes/pod-security/) - Kubernetes pod security hardening playbook
- [`content/platform-security/kubernetes/secrets/`](content/platform-security/kubernetes/secrets/) - Kubernetes Secrets security playbook
- [`content/platform-security/kubernetes/seccomp/`](content/platform-security/kubernetes/seccomp/) - Kubernetes seccomp review checklist
- [`content/platform-security/kubernetes/container-escape-capability-abuse/`](content/platform-security/kubernetes/container-escape-capability-abuse/) - container escape and Linux capability abuse overview
- [`content/platform-security/secrets/vault/`](content/platform-security/secrets/vault/) - Vault security playbook
- [`content/platform-security/cloud-iam-workload-identity/`](content/platform-security/cloud-iam-workload-identity/) - cloud federation, workload permissions, metadata isolation, and active-session containment

### Supply Chain
- [`content/supply-chain/`](content/supply-chain/) - [choose a document by task](content/supply-chain/overview.en.md)
- [`content/supply-chain/slsa-provenance/`](content/supply-chain/slsa-provenance/) - SLSA v1.2 provenance overview for container image CI/CD pipelines
- [`content/supply-chain/container-image-security/`](content/supply-chain/container-image-security/) - container image and OCI registry security playbook for Dockerfile baselines, digest pinning, multi-arch images, registry promotion, scanning, signing, and deploy-time verification
- [`content/supply-chain/ci-cd-security/`](content/supply-chain/ci-cd-security/) - pipeline trust boundaries, executor isolation, artifact handoffs, federation, and deployment verification

### AI Security
- [`content/ai-security/`](content/ai-security/) - [choose an AI security document](content/ai-security/overview.en.md) by task and document scope
- [`content/ai-security/securing-ai/`](content/ai-security/securing-ai/) - Securing AI overview
- [`content/ai-security/owasp-llm-top-10/`](content/ai-security/owasp-llm-top-10/) - OWASP LLM Top 10 threat-focused overview (2026), with the 2025/2026 map and stable historical links
- [`content/ai-security/agentic-ai/`](content/ai-security/agentic-ai/) - Agentic AI security playbook for autonomy, tools, memory, action traces, sandboxing, and kill-switch controls
- [`content/ai-security/ai-assisted-development/`](content/ai-security/ai-assisted-development/) - secure AI-assisted development playbook for coding assistants, generated code review, dependency verification, SDLC gates, and coding-agent environments
- [`content/ai-security/mcp-security/`](content/ai-security/mcp-security/) - MCP security playbook for server/tool registry, deployment patterns, OAuth, capability drift, and protocol-layer logging

### Reference
- [`reference/infrastructure-technologies/`](reference/infrastructure-technologies/) - overview of infrastructure technologies and their production operating models
- [`reference/security-policy-examples/`](reference/security-policy-examples/) - executable OPA policies, configuration examples, and allowed/denied CI scenarios

### Security Skills and Tools
- [`content/ai-automation/security-skills/`](content/ai-automation/security-skills/) - Product Security Skills, developed alongside the playbooks for assistant-driven security tasks
- [`content/ai-automation/security-skills/secure-development/`](content/ai-automation/security-skills/secure-development/) - architecture-aware control selection, implementation, and access/recovery checks
- [`content/ai-automation/security-skills/security-review/`](content/ai-automation/security-skills/security-review/) - architecture-aware PR and repository assessment, security deltas, and decisive checks
- [`content/ai-automation/security-skills/sensitive-data-cleanup/`](content/ai-automation/security-skills/sensitive-data-cleanup/) - separate cleaned copies, compound-content coverage, and linked-replacement checks
- [`content/ai-automation/security-skills/security-report-triage/`](content/ai-automation/security-skills/security-report-triage/) - scanner report triage, delivered-artifact applicability, and bounded SARIF intake
- [`content/ai-automation/security-skills/security-fix-verification/`](content/ai-automation/security-skills/security-fix-verification/) - verification of specified repairs across bypass, lifecycle, and recovery cases
- [`content/ai-automation/security-skills/workflow/`](content/ai-automation/security-skills/workflow/) - independent use and combined assessment, implementation, verification, and optional cleanup
- [`content/ai-automation/prompt-integrity/`](content/ai-automation/prompt-integrity/) - standalone static instruction integrity library and CLI
- [`content/ai-automation/model-security-eval/`](content/ai-automation/model-security-eval/) - local model security scenarios and blocking CI verdicts
- [`content/ai-automation/prompt-guard/`](content/ai-automation/prompt-guard/) - source-aware input/output validation, policy-authorized sanitization and tool contracts


## Product Security Hub

The local hub draft uses the existing Astro/Starlight site and library.
Edit source Markdown and the generator; generated pages are not independent sources.

- [`content/hub/`](content/hub/) - hub introduction
- [`content/hub/tasks/`](content/hub/tasks/) - complete route and library topics
- [`content/hub/knowledge/`](content/hub/knowledge/) - full knowledge base
- [`content/hub/catalogue/`](content/hub/catalogue/) - skills and tools catalogue
- [`content/hub/api-integration/`](content/hub/api-integration/) - external API route
- [`content/hub/reviews/delivery-api/`](content/hub/reviews/delivery-api/) - synthetic review
- [`content/hub/usage/`](content/hub/usage/) - usage and attribution

`config/hub-sources.json` is an allowlisted, revision-pinned link registry. The build
does not fetch remote content or copy the sibling repository. `downloads/` contains
public, authored templates; synchronization copies only the explicit authored template
files to `site/public/downloads/`. Private artifacts, reports and evaluation evidence
are outside the import contract.

## Licensing

Original prose, diagrams and prose templates outside complete MIT skill packages
use CC BY 4.0. Original code uses MIT. See [license boundaries](LICENSE) and
[MIT terms](LICENSE-MIT). Third-party and unknown-owner materials are excluded
from these grants and retain their applicable rights and notices.


The home scenario list is generated from `config/hub-scenarios.json`. Add a ready
route only after its RU and EN source pages exist. Each entry uses the same title,
applicability and result layout; candidates and unfilled routes are not published.


- [`content/hub/ci-cd-release/`](content/hub/ci-cd-release/) - local learning route for release security
- [`content/hub/reviews/ci-cd-release/`](content/hub/reviews/ci-cd-release/) - synthetic release review

- [`content/hub/llm-rag/`](content/hub/llm-rag/) - bilingual learning route
- [`content/hub/reviews/llm-rag/`](content/hub/reviews/llm-rag/) - synthetic review with traceable checks

- [`content/hub/agent-tools/`](content/hub/agent-tools/) - bilingual learning route
- [`content/hub/reviews/agent-tools/`](content/hub/reviews/agent-tools/) - synthetic review with traceable checks

- [`content/hub/kafka-integration/`](content/hub/kafka-integration/) - bilingual learning route
- [`content/hub/reviews/kafka-integration/`](content/hub/reviews/kafka-integration/) - synthetic review with traceable checks
