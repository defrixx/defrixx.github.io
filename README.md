# Product Security Playbook

This repository is a working collection of product security documents, including architecture review checklists, Kubernetes hardening playbooks, and security overviews.

## Repository Status

This repository is a working security knowledge base, not a finished reference.

The content evolves over time based on practical work:
- Existing documents are regularly reviewed and updated
- New materials are added incrementally
- Documents should be treated as work in progress

The guidance reflects accumulated engineering experience, not immutable standards.

## Authorship Note

Not every document here was written from scratch by one person.

Some sections compile and adapt existing practices, references, and public knowledge, with additional analysis, edits, and implementation context.

Treat this repository as curated working material rather than purely original standalone writing.

## Contributions

Feel free to use, adapt, and extend this repository.

PRs are welcome if you want to improve existing materials or add new ones.

---

## Contents

- [`templates/playbook.md`](templates/playbook.md) - reusable template for new security playbook documents

### Review and Governance
- [`content/review/architecture/`](content/review/architecture/) - security architecture review checklist
- [`content/review/threat-modeling/`](content/review/threat-modeling/) - threat modeling methodology review and practical playbook
- [`content/review/release-governance/`](content/review/release-governance/) - release governance and security quality gates for protected environments, deployment approvals, release evidence, exceptions, and escalation

### Application Security
- [`content/application-security/web/owasp-top-10/`](content/application-security/web/owasp-top-10/) - practical defense playbook for OWASP Top 10 (2025)
- [`content/application-security/web/browser-security/`](content/application-security/web/browser-security/) - browser and frontend controls for CSP, CORS, cookies, third-party scripts, embedded content, and frontend supply chain
- [`content/application-security/api/api-security-patterns/`](content/application-security/api/api-security-patterns/) - API security and integration patterns for REST, SOAP/XML, GraphQL, Webhooks, and gRPC
- [`content/application-security/business-logic/business-logic-abuse/`](content/application-security/business-logic/business-logic-abuse/) - business logic abuse playbook for ATO, signup/trial/promo abuse, tenant isolation, workflow abuse, and sensitive business flows
- [`content/application-security/identity/oidc-oauth/`](content/application-security/identity/oidc-oauth/) - OIDC + OAuth 2.0 security playbook

### DevSecOps
- [`content/platform-security/kubernetes/cluster-security-review/`](content/platform-security/kubernetes/cluster-security-review/) - Kubernetes cluster security review playbook
- [`content/platform-security/kubernetes/adversarial-validation/`](content/platform-security/kubernetes/adversarial-validation/) - Kubernetes adversarial validation and attack-path review playbook
- [`content/platform-security/kubernetes/pod-security/`](content/platform-security/kubernetes/pod-security/) - Kubernetes pod security hardening playbook
- [`content/platform-security/kubernetes/seccomp/`](content/platform-security/kubernetes/seccomp/) - Kubernetes seccomp review checklist
- [`content/platform-security/kubernetes/container-escape-capability-abuse/`](content/platform-security/kubernetes/container-escape-capability-abuse/) - container escape and Linux capability abuse overview
- [`content/platform-security/secrets/vault/`](content/platform-security/secrets/vault/) - Vault security playbook

### Supply Chain
- [`content/supply-chain/slsa-provenance/`](content/supply-chain/slsa-provenance/) - SLSA v1.2 provenance overview for container image CI/CD pipelines

### AI Security
- [`content/ai-security/securing-ai/`](content/ai-security/securing-ai/) - Securing AI overview
- [`content/ai-security/owasp-llm-top-10/`](content/ai-security/owasp-llm-top-10/) - OWASP LLM Top 10 threat-focused overview (2025)

### Reference
- [`reference/infrastructure-technologies/`](reference/infrastructure-technologies/) - overview of infrastructure technologies and their production operating models
