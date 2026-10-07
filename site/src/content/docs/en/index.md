---
title: "Product Security Playbook"
description: "A practical knowledge base for AppSec, platform security, supply chain, and AI security."
tableOfContents: false
sidebar:
  order: 0
---

A practical knowledge base for reviewing architecture, code, platforms, and engineering workflows.

The playbooks, checklists, and review methods help apply industry standards and engineering practices to specific product security tasks.

Materials evolve with technologies and attack techniques. Apply them in the context of your project's architecture, component versions, and threat model.

<section class="home-getting-started" aria-labelledby="home-start-title">
<h2 id="home-start-title">Where to start</h2>
<div class="site-map-grid">
<section class="site-map-card">
<h3>Review an architecture</h3>
<p>Identify trust boundaries and attack scenarios, then review design decisions.</p>
<ul>
<li><a href="/en/review/threat-modeling/playbook/">Threat modeling</a></li>
<li><a href="/en/review/architecture/checklist/">Architecture review</a></li>
</ul>
</section>
<section class="site-map-card">
<h3>Develop or review code</h3>
<p>Select applicable requirements, verify controls, and record the results.</p>
<ul>
<li><a href="/en/application-security/secure-coding/code-review/playbook/">Code review</a></li>
<li><a href="/en/ai-automation/security-skills/secure-development/overview/">Secure development skill</a></li>
</ul>
</section>
<section class="site-map-card">
<h3>Prepare a production release</h3>
<p>Review the platform, deployment permissions, and release acceptance criteria.</p>
<ul>
<li><a href="/en/platform-security/kubernetes/cluster-security-review/playbook/">Kubernetes cluster review</a></li>
<li><a href="/en/review/release-governance/playbook/">Release governance</a></li>
</ul>
</section>
<section class="site-map-card">
<h3>Secure an AI system</h3>
<p>Start with the common controls, then select checks for agents and integrations.</p>
<ul>
<li><a href="/en/ai-security/securing-ai/overview/">Securing AI features</a></li>
<li><a href="/en/ai-security/overview/">Choose a playbook by task</a></li>
</ul>
</section>
</div>
</section>

<section class="home-site-map" aria-labelledby="home-site-map-title">
<h2 id="home-site-map-title">Site map</h2>
<div class="site-map-grid">
<section class="site-map-card">
<h3><a href="/en/review/overview/">Review and Governance</a></h3>
<ul>
<li><a href="/en/review/architecture/checklist/">Architecture review</a></li>
<li><a href="/en/review/threat-modeling/playbook/">Threat modeling</a></li>
<li><a href="/en/review/release-governance/playbook/">Release governance</a></li>
<li><a href="/en/review/vulnerability-management/playbook/">Vulnerability management</a></li>
</ul>
</section>
<section class="site-map-card">
<h3><a href="/en/application-security/overview/">Application Security</a></h3>
<div class="site-map-group">
<h4>Code, APIs, and access control</h4>
<ul>
<li><a href="/en/application-security/api/api-security-patterns/playbook/">API security</a></li>
<li><a href="/en/application-security/business-logic/business-logic-abuse/playbook/">Business logic</a></li>
<li><a href="/en/application-security/secure-coding/code-review/playbook/">Code review</a></li>
<li><a href="/en/application-security/identity/oidc-oauth/playbook/">OIDC and OAuth</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Web and browser</h4>
<ul>
<li><a href="/en/application-security/web/owasp-top-10/playbook/">OWASP Top 10</a></li>
<li><a href="/en/application-security/web/browser-security/playbook/">Browser security</a></li>
</ul>
</div>
</section>
<section class="site-map-card">
<h3><a href="/en/platform-security/overview/">Platform Security</a></h3>
<div class="site-map-group">
<h4>Cloud access</h4>
<ul>
<li><a href="/en/platform-security/cloud-iam-workload-identity/playbook/">Cloud IAM and workload access</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Kubernetes</h4>
<ul>
<li><a href="/en/platform-security/kubernetes/cluster-security-review/playbook/">Cluster review</a></li>
<li><a href="/en/platform-security/kubernetes/adversarial-validation/playbook/">Adversarial validation</a></li>
<li><a href="/en/platform-security/kubernetes/pod-security/playbook/">Pod security</a></li>
<li><a href="/en/platform-security/kubernetes/secrets/playbook/">Kubernetes secrets</a></li>
<li><a href="/en/platform-security/kubernetes/seccomp/checklist/">Seccomp checklist</a></li>
<li><a href="/en/platform-security/kubernetes/container-escape-capability-abuse/overview/">Container escape and capabilities</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Secrets management</h4>
<ul>
<li><a href="/en/platform-security/secrets/vault/playbook/">Secrets in Vault</a></li>
</ul>
</div>
</section>
<section class="site-map-card">
<h3><a href="/en/supply-chain/overview/">Supply Chain</a></h3>
<ul>
<li><a href="/en/supply-chain/slsa-provenance/overview/">SLSA and build provenance</a></li>
<li><a href="/en/supply-chain/container-image-security/playbook/">Container images</a></li>
<li><a href="/en/supply-chain/ci-cd-security/playbook/">CI/CD security</a></li>
</ul>
</section>
<section class="site-map-card">
<h3><a href="/en/ai-security/overview/">AI Security</a></h3>
<div class="site-map-group">
<h4>AI features and threats</h4>
<ul>
<li><a href="/en/ai-security/securing-ai/overview/">Securing AI features</a></li>
<li><a href="/en/ai-security/owasp-llm-top-10/overview/">OWASP LLM Top 10</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Agents and integrations</h4>
<ul>
<li><a href="/en/ai-security/agentic-ai/playbook/">Agent security</a></li>
<li><a href="/en/ai-security/mcp-security/playbook/">MCP security</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>AI-assisted development</h4>
<ul>
<li><a href="/en/ai-security/ai-assisted-development/playbook/">AI-assisted development</a></li>
</ul>
</div>
</section>
<section class="site-map-card">
<h3><a href="/en/ai-automation/security-skills/overview/">Skills and Tools</a></h3>
<div class="site-map-group">
<h4>Skills</h4>
<ul>
<li><a href="/en/ai-automation/security-skills/secure-development/overview/">Secure development</a></li>
<li><a href="/en/ai-automation/security-skills/security-review/overview/">Security review</a></li>
<li><a href="/en/ai-automation/security-skills/sensitive-data-cleanup/overview/">Sensitive data cleanup</a></li>
<li><a href="/en/ai-automation/security-skills/security-report-triage/overview/">Security report triage</a></li>
<li><a href="/en/ai-automation/security-skills/security-fix-verification/overview/">Fix verification</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Combined workflow</h4>
<ul>
<li><a href="/en/ai-automation/security-skills/workflow/overview/">Combined skill workflow</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Tools</h4>
<ul>
<li><a href="/en/ai-automation/prompt-integrity/overview/">prompt-integrity</a></li>
<li><a href="/en/ai-automation/model-security-eval/overview/">model-security-eval</a></li>
<li><a href="/en/ai-automation/prompt-guard/overview/">prompt-guard</a></li>
</ul>
</div>
</section>
<section class="site-map-card">
<h3>Reference</h3>
<ul>
<li><a href="/en/reference/infrastructure-technologies/infrastructure-technologies/">Infrastructure technologies</a></li>
<li><a href="/en/reference/security-policy-examples/overview/">Security policy examples</a></li>
</ul>
</section>
</div>
</section>
