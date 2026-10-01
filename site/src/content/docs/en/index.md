---
title: "Product Security Playbook"
description: "A practical knowledge base for AppSec, platform security, supply chain, and AI security."
sidebar:
  order: 0
---

A practical knowledge base for reviewing architecture, code, platforms, and engineering workflows.

This project is a curated and continuously maintained Product Security knowledge base focused on practical security engineering.

The content combines industry standards, public research, security frameworks, and hands-on engineering practices into reusable playbooks, checklists, and review approaches.

Its goal is not to reproduce existing standards, but to translate them into practical workflows that can be applied during architecture reviews, threat modeling, secure development, platform security, software supply chain assessments, and AI security reviews.

Materials are continuously refined as technologies, attack techniques, and engineering practices evolve.

Detailed references and source attribution are provided where applicable.

## Site map

<div class="site-map-grid">
<section class="site-map-card">
<h3><a href="/Product-security-playbook/en/review/overview/">Review and Governance</a></h3>
<ul>
<li><a href="/Product-security-playbook/en/review/architecture/checklist/">Architecture review</a></li>
<li><a href="/Product-security-playbook/en/review/threat-modeling/playbook/">Threat modeling</a></li>
<li><a href="/Product-security-playbook/en/review/release-governance/playbook/">Release governance</a></li>
<li><a href="/Product-security-playbook/en/review/vulnerability-management/playbook/">Vulnerability management</a></li>
</ul>
</section>
<section class="site-map-card">
<h3><a href="/Product-security-playbook/en/application-security/overview/">Application Security</a></h3>
<div class="site-map-group">
<h4>Code and application interfaces</h4>
<ul>
<li><a href="/Product-security-playbook/en/application-security/api/api-security-patterns/playbook/">API security</a></li>
<li><a href="/Product-security-playbook/en/application-security/business-logic/business-logic-abuse/playbook/">Business logic</a></li>
<li><a href="/Product-security-playbook/en/application-security/secure-coding/code-review/playbook/">Code review</a></li>
<li><a href="/Product-security-playbook/en/application-security/identity/oidc-oauth/playbook/">OIDC and OAuth</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Web and browser</h4>
<ul>
<li><a href="/Product-security-playbook/en/application-security/web/owasp-top-10/playbook/">OWASP Top 10</a></li>
<li><a href="/Product-security-playbook/en/application-security/web/browser-security/playbook/">Browser security</a></li>
</ul>
</div>
</section>
<section class="site-map-card">
<h3><a href="/Product-security-playbook/en/platform-security/overview/">Platform Security</a></h3>
<div class="site-map-group">
<h4>Kubernetes</h4>
<ul>
<li><a href="/Product-security-playbook/en/platform-security/kubernetes/cluster-security-review/playbook/">Cluster review</a></li>
<li><a href="/Product-security-playbook/en/platform-security/kubernetes/adversarial-validation/playbook/">Adversarial validation</a></li>
<li><a href="/Product-security-playbook/en/platform-security/kubernetes/pod-security/playbook/">Pod security</a></li>
<li><a href="/Product-security-playbook/en/platform-security/kubernetes/secrets/playbook/">Kubernetes secrets</a></li>
<li><a href="/Product-security-playbook/en/platform-security/kubernetes/seccomp/checklist/">Seccomp checklist</a></li>
<li><a href="/Product-security-playbook/en/platform-security/kubernetes/container-escape-capability-abuse/overview/">Container escape and capabilities</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Secrets management</h4>
<ul>
<li><a href="/Product-security-playbook/en/platform-security/secrets/vault/playbook/">Secrets in Vault</a></li>
</ul>
</div>
</section>
<section class="site-map-card">
<h3><a href="/Product-security-playbook/en/supply-chain/overview/">Supply Chain</a></h3>
<ul>
<li><a href="/Product-security-playbook/en/supply-chain/slsa-provenance/overview/">SLSA and build provenance</a></li>
<li><a href="/Product-security-playbook/en/supply-chain/container-image-security/playbook/">Container images</a></li>
</ul>
</section>
<section class="site-map-card">
<h3><a href="/Product-security-playbook/en/ai-security/overview/">AI Security</a></h3>
<div class="site-map-group">
<h4>AI features and threats</h4>
<ul>
<li><a href="/Product-security-playbook/en/ai-security/securing-ai/overview/">Securing AI features</a></li>
<li><a href="/Product-security-playbook/en/ai-security/owasp-llm-top-10/overview/">OWASP LLM Top 10</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Agents and integrations</h4>
<ul>
<li><a href="/Product-security-playbook/en/ai-security/agentic-ai/playbook/">Agent security</a></li>
<li><a href="/Product-security-playbook/en/ai-security/mcp-security/playbook/">MCP security</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>AI-assisted development</h4>
<ul>
<li><a href="/Product-security-playbook/en/ai-security/ai-assisted-development/playbook/">AI-assisted development</a></li>
</ul>
</div>
</section>
<section class="site-map-card">
<h3><a href="/Product-security-playbook/en/ai-automation/security-skills/overview/">Skills and Tools</a></h3>
<div class="site-map-group">
<h4>Skills</h4>
<ul>
<li><a href="/Product-security-playbook/en/ai-automation/security-skills/secure-development/overview/">Secure development</a></li>
<li><a href="/Product-security-playbook/en/ai-automation/security-skills/security-review/overview/">Security review</a></li>
<li><a href="/Product-security-playbook/en/ai-automation/security-skills/sensitive-data-cleanup/overview/">Sensitive data cleanup</a></li>
<li><a href="/Product-security-playbook/en/ai-automation/security-skills/security-report-triage/overview/">Security report triage</a></li>
<li><a href="/Product-security-playbook/en/ai-automation/security-skills/security-fix-verification/overview/">Fix verification</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Combined workflow</h4>
<ul>
<li><a href="/Product-security-playbook/en/ai-automation/security-skills/workflow/overview/">Combined skill workflow</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Tools</h4>
<ul>
<li><a href="/Product-security-playbook/en/ai-automation/prompt-integrity/overview/">prompt-integrity</a></li>
</ul>
</div>
</section>
<section class="site-map-card">
<h3>Reference</h3>
<ul>
<li><a href="/Product-security-playbook/en/reference/infrastructure-technologies/infrastructure-technologies/">Infrastructure technologies</a></li>
</ul>
</section>
</div>
