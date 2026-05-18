# Kubernetes Cluster Security Review Playbook

## 1. Scope and Objective

This playbook defines a **practical Kubernetes cluster security review** across:
- deployment subjects (human and machine identities);
- deployment and supply chain path;
- external and internal service boundaries;
- observability required for Incident Response;
- Admission / RBAC / ServiceAccount boundaries;
- secrets flow from source to runtime.

**Objective:**
- reduce unauthorized deployment and hidden privilege-escalation risk;
- reduce blast radius after workload or CI/CD compromise;
- ensure incident investigations are reproducible from cluster evidence.

---

## 2. Threat Model (Cluster Security Review)

**What is protected:**
- deployment rights and cluster-configuration change rights;
- `source -> build -> registry -> deploy` chain integrity;
- Kubernetes API access and admission/namespace policy integrity;
- ServiceAccount tokens, application secrets, and external secret-store access;
- audit trail quality for investigations.

**Typical attacker path:**
- compromise developer or CI identity;
- perform unauthorized deployment or policy mutation;
- establish persistence through RBAC/admission drift;
- extract secrets and move laterally.

---

## 3. Review Domains and Checks

### 3.1 Who can deploy

**What to verify:**
- subjects with `create/update/patch/delete` on workload resources (`deployments`, `statefulsets`, `daemonsets`, `jobs`, `cronjobs`, `pods`);
- subjects with rights over `pods/exec`, `pods/ephemeralcontainers`, `pods/attach`, `pods/portforward`;
- subjects who can change `roles`, `clusterroles`, `rolebindings`, `clusterrolebindings`;
- subjects with `nodes/proxy` access (broad node-level Kubelet API access);
- subjects with access to fine-grained Kubelet API subresources: `nodes/metrics`, `nodes/stats`, `nodes/log`, `nodes/spec`, `nodes/checkpoint`, `nodes/configz`, `nodes/healthz`, `nodes/pods`;
- machine identities that actually deploy to live environments (CD controllers, CI bots).

**Risk signals:**
- users or groups holding `cluster-admin` without break-glass ownership;
- wildcard privileges (`resources: ["*"]`, `verbs: ["*"]`) in protected namespaces;
- direct live deployment from human identities, bypassing CD;
- `nodes/proxy`, `escalate`, `bind`, or `impersonate` granted without explicit security approval;
- monitoring/logging agents granted `nodes/proxy` even though fine-grained Kubelet API subresources are sufficient for their function.

**Recommended control:**
- live deployments are performed only by dedicated CI/CD ServiceAccounts;
- human users do not deploy directly except break-glass roles with owner + expiry;
- review all ClusterRole/ClusterRoleBinding objects every `30d`;
- enforce automatic policy fail for high-risk RBAC verbs outside an approved allowlist (`escalate`, `bind`, `impersonate`, `serviceaccounts/token`, `nodes/proxy`);
- for Kubernetes `v1.36+`: `KubeletFineGrainedAuthz` is GA and the feature gate is locked/enabled, so observability workloads should use minimal subresources (`nodes/metrics`, `nodes/stats`, `nodes/pods`, and other required endpoints) instead of broad `nodes/proxy`;
- deny new RBAC bindings to `nodes/proxy` for observability workloads when their kubelet scraping/logging use case is covered by fine-grained permissions.

**Minimum evidence commands:**
```bash
kubectl get clusterrolebindings,rolebindings -A
kubectl get clusterroles,roles -A -o yaml
kubectl auth can-i create deployments --as=<subject> -n <ns>
kubectl auth can-i get nodes/proxy --as=<subject>
kubectl auth can-i get nodes/metrics --as=<subject>
kubectl get clusterroles -o yaml | grep -n 'nodes/proxy'
curl -sk --header "Authorization: Bearer $TOKEN" https://$NODE_IP:10250/metrics \
  | grep 'kubernetes_feature_enabled{name="KubeletFineGrainedAuthz",stage="GA"} 1'
```

---

### 3.2 Deployment chain

**What to verify:**
- deployment intent source (PR merge, release tag, manual apply);
- where builds run and which identity signs artifacts;
- image selection strategy in manifests (`digest` vs mutable tag);
- who can modify pipeline definitions, CD projects, and environments;
- separation of duties between code authors and release approvers/executors.

**Risk signals:**
- live deployment from local `kubectl apply`;
- tag-only image references used in live environments, including version-like tags such as `:v1.2.3`;
- one subject can write code, edit pipeline, and release alone;
- no artifact provenance or pre-deploy verification.

**Recommended control:**
- deploy only via CI/CD, with cluster changes audit-able and replay-able;
- release images pinned by `@sha256` digest only;
- branch protection + mandatory review for IaC/manifests and pipeline configuration;
- separate `author`, `approver`, and `releaser` roles.

---

### 3.3 External and internal services

**What to verify:**
- all cluster entry points: `Ingress`, `Gateway`, `LoadBalancer`, `NodePort`;
- Service objects with `spec.externalIPs` set;
- workload egress dependencies (SaaS, cloud APIs, internal services);
- allowed namespace/service-to-service communication paths;
- existence of an actual live service/data-flow inventory.

**Risk signals:**
- unknown public endpoints;
- use of `Service.spec.externalIPs` in live or multi-tenant clusters;
- no default-deny network model;
- unrestricted egress for critical workloads;
- no ownership for external integrations.

**Recommended control:**
- north-south and east-west flow inventory updated at least every `30d`;
- protected namespaces use default deny + explicit allow rules;
- every public endpoint has owner, data classification, and vulnerability SLA;
- deny new `Service.spec.externalIPs` through admission policy: `DenyServiceExternalIPs`, `ValidatingAdmissionPolicy`, or a tested policy engine. In Kubernetes `v1.36+`, this field is deprecated; historically it has been insecure by default because a user who can create or modify a Service can intercept traffic to a chosen IP when the CVE-2020-8554 conditions are present.
- create a migration plan with owner and deadline for existing `externalIPs`. Preferred targets are managed `type: LoadBalancer`, Ingress/Gateway API for HTTP(S)/L4 entry, or `NodePort` only behind an external load balancer/firewall with explicit IP ownership and network ACLs.
- do not replace `externalIPs` with manual `status.loadBalancer.ingress` patching without a separate permission model: `services/status` must remain a privileged operation, unavailable to ordinary deploy identities.

**Minimum evidence commands:**
```bash
kubectl get services -A -o jsonpath='{range .items[?(@.spec.externalIPs)]}{.metadata.namespace}{"/"}{.metadata.name}{" "}{.spec.externalIPs}{"\n"}{end}'
kubectl auth can-i patch services/status --as=<subject> -n <ns>
```

---

### 3.4 Observability for Incident Response

**What to verify:**
- Kubernetes Audit Logging is enabled on `kube-apiserver`;
- centralized collection exists for audit logs, control-plane logs, and runtime events;
- event coverage includes RBAC/admission/namespace-label changes/deployments;
- CI/CD release events can be correlated with actual Kubernetes API activity.

**Risk signals:**
- audit logging is partial or only local on control-plane nodes;
- no critical operation events (`rolebindings`, `clusterrolebindings`, `validatingwebhookconfigurations`, `mutatingwebhookconfigurations`, `namespaces`);
- retention shorter than typical incident lifecycle.

**Recommended control:**
- centralized immutable audit storage with at least `90d` retention (or stricter regulatory requirement);
- for high-risk API operations, log at `Request`/`RequestResponse` where appropriate while preventing sensitive-data leakage;
- alerting on RBAC changes, webhook config changes, namespace security label changes, and mass Secret reads;
- complement API audit with runtime/network behavioral telemetry (for example, CNI observability and eBPF tooling) to detect not only deploy events but anomalous runtime behavior;
- timeline reconstruction drill at least every `90d`.

---

### 3.5 Admission / RBAC / ServiceAccount boundaries

**What to verify:**
- critical security rules are enforced through admission (not documentation-only policy);
- RBAC controls sensitive read operations (admission does not block `get/list/watch`);
- namespace label mutation is restricted (to protect PSA/NetworkPolicy boundaries);
- `automountServiceAccountToken` is disabled by default for workloads without API needs;
- live workloads do not use the namespace `default` ServiceAccount.

**Risk signals:**
- reliance only on mutating webhook without validating policy;
- developer roles can modify `validatingwebhookconfigurations`/`mutatingwebhookconfigurations`;
- application identities can mutate namespace labels and weaken enforcement;
- one ServiceAccount is reused across unrelated workloads.

**Recommended control:**
- separate responsibilities: RBAC controls "who can", admission controls "with which parameters";
- use `ValidatingAdmissionPolicy` (Kubernetes `v1.30+`) or webhook-based equivalent for policy enforcement;
- deny `escalate` / `bind` / `impersonate` / `serviceaccounts/token` by default;
- for control-plane hardening, evaluate `AlwaysPullImages` separately with operational impact considered where applicable;
- treat `EventRateLimit` as version- and deployment-dependent: it is an alpha admission controller and is disabled by default in upstream Kubernetes; prefer provider-supported API/event throttling or a tested custom policy where alpha admission plugins are not acceptable;
- enforce one ServiceAccount per workload and quarterly permission recertification.

---

### 3.6 Secrets flow

**What to verify:**
- where each secret originates, how it reaches runtime, and how it rotates;
- whether plaintext/base64 secrets appear in Git manifests;
- etcd encryption at rest status for Secret data;
- who has `get/list/watch` on Secrets in live environments;
- token/secret TTL and revocation process quality.

**Risk signals:**
- secrets stored in repository or values files without external secret manager;
- long-lived ServiceAccount token secrets used as the primary mechanism;
- broad `list/watch` on Secrets for human or CI identities;
- no provable rotation and emergency revocation process.

**Recommended control:**
- use pull model from external secret store (for example Vault) instead of storing values in manifests;
- enable etcd encryption at rest and verify status after control-plane changes;
- limit Secret ACL to minimum required workload identities;
- use short-lived tokens and regular secret rotation;
- if push model is used for operational reasons (for example `sops`/`helm-secrets`), require encrypted Git storage, controlled key management, and forbid decryption outside trusted CI/CD boundaries;
- periodically verify logging does not expose secret values.

---

### 3.7 Adversarial validation

**What to verify:**
- key attack paths have been tested from a low-trust workload position: service discovery, east-west reachability, ServiceAccount permissions, `NodePort` exposure, `exec`/ephemeral containers;
- evidence exists before and after remediation, not only a list of YAML settings;
- detection/policy test cases are used to verify audit, runtime telemetry, and admission controls.

**Recommended control:**
- run adversarial validation for live-like environments after major RBAC, CNI, admission policy, runtime security tooling, and deployment-chain changes;
- destructive, DoS, and escape checks run only in an isolated environment or namespace with pre-approved scope;
- use the dedicated playbook for scenario-to-control mapping: [kubernetes/adversarial-validation/playbook.en.md](../adversarial-validation/playbook.en.md).

---

## 4. Minimum Policy Gates for Live Environments

The minimum gatekeeping baseline should include:
- deny direct human deploy into protected namespaces;
- deny tag-only images in live environments and require an immutable digest reference (`@sha256:...`); `tag@sha256` may be allowed for readability, but the digest must be the value used for deployment;
- block high-risk RBAC verbs outside explicit allowlist;
- require protected namespaces to have ingress and egress default-deny NetworkPolicy, or a documented CNI-equivalent policy with tested enforcement;
- block new Service objects with `spec.externalIPs`; existing use is allowed only as a migration exception with `owner`, `expiry`, verified external IP ownership, and a transition plan to `LoadBalancer`, Gateway API/Ingress, or controlled `NodePort`;
- require Kubernetes audit logging with policy coverage for RBAC changes, admission/webhook changes, namespace security label changes, Secret reads, `exec`, attach/port-forward, and ephemeral-container updates;
- restrict and periodically recertify `get/list/watch` access to Secrets in live environments;
- require `automountServiceAccountToken: false` by default unless the workload has a documented Kubernetes API access need;
- block namespace `default` ServiceAccount usage for application workloads;
- require protected namespaces to enforce Pod Security Standards `restricted` by default:
  - `pod-security.kubernetes.io/enforce: restricted`
  - `pod-security.kubernetes.io/enforce-version: <pinned Kubernetes minor version>`
  - `pod-security.kubernetes.io/audit: restricted`
  - `pod-security.kubernetes.io/audit-version: <same pinned version>`
  - `pod-security.kubernetes.io/warn: restricted`
  - `pod-security.kubernetes.io/warn-version: <same pinned version>`;
- require effective seccomp hardening separately from the PSS label: live workloads must explicitly set `seccompProfile.type: RuntimeDefault` at Pod or container level, or nodes must enforce kubelet `--seccomp-default` / `seccompDefault` so unspecified profiles become `RuntimeDefault`; evidence must show the effective runtime profile, not only namespace labels;
- use `warn`/`audit=restricted` without `enforce=restricted` only during a documented rollout or migration window with owner, expiry, and a blocking date for enforcement;
- monitor Pod Security label drift and block deployment if live-environment labels regress, are removed, or point to an unapproved version;
- verify through admission policy tests that live workloads without an image digest are rejected, including `:latest`, version-like tags, and image names with no explicit tag;
- verify etcd Secret encryption at rest where the team owns or can configure the control plane;
- allow exceptions only via explicit object containing `owner`, `justification`, and `expiry`.

---

## 5. Required Review Outputs

A review is complete only when it provides:
- full deploy-subject inventory with effective permissions;
- deployment-chain map with trust boundaries and control points;
- external/internal service interaction inventory;
- observability coverage map for IR (what is logged and where retained);
- Admission/RBAC/ServiceAccount responsibility matrix;
- secrets-flow map including TTL/rotation/revocation and owners.

---

## 6. Anti-patterns

- One shared `cluster-admin` account for the whole team.
- Live deployment via developer local kubeconfig.
- Admission controls without RBAC protection for sensitive reads.
- RBAC least privilege without protection of admission/webhook configs.
- `Service.spec.externalIPs` as the standard way to publish a service externally.
- One shared ServiceAccount for all namespace applications.
- Secrets in Git (including base64 YAML) as normal process.
- No reconstructable incident timeline from audit/logging data.

---

## 7. Related Repository Materials

- Pod runtime hardening: [kubernetes/pod-security/playbook.en.md](../pod-security/playbook.en.md)
- Kubernetes adversarial validation: [kubernetes/adversarial-validation/playbook.en.md](../adversarial-validation/playbook.en.md)
- Seccomp review checklist: [kubernetes/seccomp/checklist.en.md](../seccomp/checklist.en.md)
- Container escape / capabilities: [kubernetes/container-escape-capability-abuse/overview.en.md](../container-escape-capability-abuse/overview.en.md)
- Vault and secrets: [secrets/vault/playbook.en.md](../../secrets/vault/playbook.en.md)
- OIDC/OAuth for machine/human access patterns: [identity/oidc-oauth/playbook.en.md](../../../application-security/identity/oidc-oauth/playbook.en.md)
---

## 7. Related Materials

- [Kubernetes adversarial validation playbook](../adversarial-validation/playbook.en.md)
- [Pod Security playbook](../pod-security/playbook.en.md)
- [Seccomp checklist](../seccomp/checklist.en.md)
- [Container image security playbook](../../../supply-chain/container-image-security/playbook.en.md)
