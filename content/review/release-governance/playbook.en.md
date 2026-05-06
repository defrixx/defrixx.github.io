# Release Governance and Security Quality Gates Playbook

## 1. Scope and Objective

This playbook defines the release-control layer around CI/CD: security quality gates, protected environments, deployment approvals, release evidence, exception handling, and escalation.

Use this document for:
- production and high-risk staging releases;
- GitLab, GitHub Actions, Argo CD, Jenkins, or similar delivery systems;
- services, container images, infrastructure changes, Kubernetes manifests, and security-sensitive configuration.

Out of scope:
- detailed SLSA provenance implementation: use the [SLSA provenance overview](../../supply-chain/slsa-provenance/overview.en.md);
- Kubernetes cluster admission and RBAC review: use the [Kubernetes cluster security review playbook](../../platform-security/kubernetes/cluster-security-review/playbook.en.md);
- architecture threat modeling: use the [Threat Modeling Playbook](../threat-modeling/playbook.en.md).

Objective:
- separate the right to merge code from the right to deploy risk;
- make release decisions evidence-based and repeatable;
- prevent high-risk findings, unverified artifacts, unapproved exceptions, and unauthorized deployment paths from silently reaching production.

---

## 2. Version Assumptions and Sources

| Area | Assumption | Source | Last verified |
|---|---|---|---|
| Secure SDLC | NIST SSDF SP 800-218 v1.1 is final and provides high-level secure software development practices | NIST SP 800-218 | 2026-05-06 |
| Provenance | SLSA v1.2 is approved; Build L2/L3 require stronger provenance and build-platform trust than L1 | SLSA v1.2 | 2026-05-06 |
| GitLab environments | Protected environments and deployment approvals are available in GitLab Premium/Ultimate tiers; exact behavior depends on GitLab version and tier | GitLab protected environments and deployment approvals docs | 2026-05-06 |
| GitHub environments | GitHub environments can use protection rules, required reviewers, wait timers, environment secrets, and deployment branch restrictions; availability depends on plan and repository visibility | GitHub deployments and environments docs | 2026-05-06 |

---

## 3. Threat Model

Assets:
- production deployment authority, release artifacts, provenance/attestations, environment secrets, CI/CD runners, approval records, exception decisions, audit logs, and customer-impacting production state.

Attackers and entry points:
- compromised developer or maintainer account;
- malicious or compromised CI job, runner, reusable workflow, plugin, or build dependency;
- insider bypassing security checks through manual deployment or environment permission drift;
- attacker substituting artifacts between build and deploy;
- team pressure that turns exceptions into undocumented release debt.

High-impact scenarios:
- One person can write code, edit pipeline, approve deployment, and deploy to production without independent review.
- Production deploy uses a mutable tag or artifact that was not produced by the trusted release workflow.
- Critical scanner finding is suppressed without owner, expiry, compensating control, or evidence.
- Untrusted fork or branch gains access to signing, deployment, or environment secrets.
- Emergency release bypasses normal gates and leaves no post-release review trail.

---

## 4. Release Control Model

### 4.1 Release Classes

| Release class | Examples | Minimum gate posture |
|---|---|---|
| Low-risk internal | Internal tool, no sensitive data, bounded blast radius | CI checks pass, owner approval, evidence retained |
| Standard production | Customer-facing service, normal API or UI release | Security gates, protected environment, deployment approval, artifact immutability |
| High-risk production | Auth, payment, tenant isolation, admin, secrets, platform, CI/CD, Kubernetes control plane | Independent security approval, stricter gates, rollback plan, release evidence pack |
| Emergency | Incident fix, urgent production restoration | Expedited approval, narrow scope, mandatory post-release review within `2 business days` |

Production recommendation:
- Every repository or deployable service declares its default release class.
- A change can raise the release class for a single release when it touches auth, tenant isolation, payment, secrets, CI/CD, IaC, Kubernetes policy, or privileged admin paths.

### 4.2 Separation of Duties

Production defaults:
- Protected production environments are deployable only by dedicated CD identities or explicitly authorized release roles.
- Human direct production deployment is break-glass only.
- The same person should not be the sole author, sole approver, and sole deploy approver for a high-risk production release.
- Changes to pipeline definitions, reusable workflows, deployment manifests, IaC modules, signing configuration, and environment protection rules require review by owners listed in CODEOWNERS or equivalent policy.

Verification:
- List users/groups/service accounts allowed to deploy to production.
- Confirm environment secrets are only exposed to jobs that reference protected environments after required rules pass.
- Review audit events for changes to protected environment rules and deployment approvals.

---

## 5. Security Quality Gates

### 5.1 Gate Types

| Gate | Purpose | Blocking default |
|---|---|---|
| Source governance | Protected branch/tag, required review, CODEOWNERS for high-risk paths | Block direct production-source changes |
| SAST/secret scan | Prevent obvious code and secret issues before release | Block new Critical/High confirmed findings and live secrets |
| SCA/SBOM | Detect vulnerable dependencies and maintain release inventory | Block exploitable Critical/High without exception |
| IaC/container scan | Catch unsafe infrastructure, image, and runtime settings | Block Critical/High in production deploy path |
| Artifact signing/provenance | Prove artifact came from expected builder/source/workflow | Block unsigned/unverified artifacts where required |
| DAST/API tests | Validate deployed test/staging surface and auth/session behavior | Block confirmed Critical/High reachable issues |
| Manual approval | Record release readiness and risk acceptance | Required for standard and high-risk production |

Production defaults:
- Gates apply to changes, not only full repositories. Do not block a release solely because unrelated legacy debt exists unless policy says legacy debt has crossed the release threshold.
- New Critical findings block release unless a valid Critical exception exists.
- New High findings block high-risk production releases by default; standard production may proceed only with owner, due date, compensating controls, and explicit acceptance.
- Live secret findings block release until the secret is revoked/rotated and exposure is assessed.
- Scanner output must be triaged into confirmed issue, false positive, accepted risk, or backlog debt. Raw unreviewed reports are not release evidence by themselves.

### 5.2 Gate Aggregation

Production defaults:
- Release decision uses one aggregated status rather than multiple disconnected scanner dashboards.
- Aggregated status records: gate name, tool/source, commit/artifact digest, result, finding IDs, exception IDs, approver, timestamp, and evidence link.
- A failed non-security quality gate can block deployment, but security exceptions must remain visible and separately approved.

Verification:
- Rebuild the release decision from logs and artifacts after deployment.
- Confirm the deployed artifact digest matches the gated artifact digest.

---

## 6. Protected Environments and Deployment Approvals

Production defaults:
- `production` is a protected environment.
- `staging` is protected when it has production-like data, secrets, network reachability, or release-signoff role.
- Deployment authority is narrower than merge authority.
- Approval rules are environment-specific: production, regulated, platform, and break-glass environments may require different approver groups.
- Self-approval is disabled for high-risk production unless explicitly justified by organization policy and compensated by post-deploy review.
- Deployment approvals include a short reason or release reference, not only a button click.

GitLab-specific notes:
- Protected environments restrict who can deploy to named environments.
- Deployment approvals can block deployments until required approvals are granted.
- Verify tier/version behavior before relying on deployment approval features.

GitHub-specific notes:
- Environments can require protection rules before a job proceeds or accesses environment secrets.
- Required reviewers, branch restrictions, wait timers, and custom protection rules can express release policy.
- Verify plan and repository visibility because feature availability differs.

Verification:
- Attempt deployment from an unauthorized user/branch and confirm it fails.
- Confirm environment secrets are unavailable before protection rules pass.
- Review audit logs for approval, rejection, and environment-rule changes.

---

## 7. Release Evidence

Minimum evidence pack for standard production:
- release ID, service, owner, environment, release class;
- source repository, protected ref, commit SHA, and reviewed PR/MR;
- artifact name and immutable digest;
- CI/CD pipeline ID and runner/build identity;
- gate results and scanner versions/configs where relevant;
- SBOM or dependency inventory where required;
- provenance/signature verification result where required;
- deployment approval record;
- open findings and approved exceptions;
- rollback or remediation reference for high-risk changes.

Additional evidence for high-risk production:
- threat model or abuse-case update;
- negative tests for auth, tenant isolation, payment/ledger, admin, or secrets path touched by the change;
- rollback/kill-switch plan;
- monitoring and alert confirmation for the changed sensitive flow;
- explicit security owner approval.

Retention:
- Keep release evidence for at least `1 year` for production, or longer when regulatory, customer, audit, or incident-response requirements demand it.

---

## 8. Exceptions and Escalation

Exception record must include:
- finding or gate ID;
- affected service/release;
- risk statement and business reason;
- compensating controls;
- owner and approver;
- expiry date;
- verification condition for closure.

Production defaults:
- Critical findings are rejected by default. A Critical exception is valid only with security leadership and business/product owner approval, explicit TTL, compensating controls, and mandatory post-release review.
- High exceptions require service owner plus security owner approval.
- Exceptions without expiry are invalid.
- Expired exceptions automatically fail the next release gate unless renewed through review.
- Emergency bypass requires post-release review within `2 business days`, including what was bypassed, why, impact, and remediation plan.

Escalation triggers:
- release blocked by Critical without accepted risk;
- disputed severity or business impact;
- repeated exception renewal;
- missing owner for a production finding;
- evidence cannot prove which artifact was deployed.
