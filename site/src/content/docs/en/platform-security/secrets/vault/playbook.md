---
title: "Vault Security Playbook"
description: "This document is for platform engineers, security engineers, and service owners who run Vault in Kubernetes-based environments."
sidebar:
  order: 70
---
## 1. Scope and Goal

This document is for platform engineers, security engineers, and service owners who run Vault in Kubernetes-based environments.

The TTLs, rotation intervals, and response targets below are local operational defaults for production services with automated renewal or re-authentication and dedicated secret owners. They are not HashiCorp defaults or universal security limits. Confirm each value against backend lease limits, job duration, rollout and outage behavior, and the ability to revoke or rotate credentials within the stated target. Record approved deviations and test renewal failure and recovery before adoption.

## 2. Security of Vault Itself

### 2.1 Cluster and network hardening

- Run Vault in HA mode.
- Restrict inbound access to Vault listeners with Kubernetes NetworkPolicy and perimeter firewall rules.
- Limit outbound access from Vault pods to required backends only (KMS/HSM, storage, auth dependencies).
- Enforce TLS for client traffic and intra-cluster traffic.
- Keep Vault version current and follow a regular patch window.

### 2.1.1 Vault server/runtime hardening for Kubernetes

Treat Vault as a tier-0 service. Kubernetes makes operation easier, but it does not remove the need to harden the Vault process, pod, and nodes.

Pod and process baseline:
- run Vault as a dedicated unprivileged user (`runAsNonRoot: true`, fixed non-zero `runAsUser`/`runAsGroup`);
- set `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `seccompProfile.type: RuntimeDefault`, and drop unnecessary Linux capabilities;
- do not run Vault with a shell/debug sidecar, package manager, or general-purpose troubleshooting container in live environments;
- restrict writable paths to the minimum required runtime, data, and audit-log locations; Vault's service account must not be able to overwrite the Vault binary or configuration;
- deny `exec` and ephemeral containers for Vault pods except approved break-glass roles with audit logging and short expiry;
- keep Vault pods on dedicated or tightly isolated nodes where feasible; if full single tenancy is not possible, document the co-tenancy risk and isolate with node pools, taints/tolerations, runtime policy, NetworkPolicy, and restricted admin access.

Node and OS baseline:
- disable swap for nodes that run Vault, or use an equivalent node profile that prevents sensitive Vault memory from being paged to disk;
- disable core dumps for the Vault process/node profile; on Linux this normally means `RLIMIT_CORE=0` or an equivalent systemd/container-runtime control;
- restrict host access: no broad `hostPath`, no runtime socket mounts, no host namespaces, no privileged mode;
- limit node-level SSH/debug access and require central logging instead of ad hoc shell access.

Required evidence:
- deployed StatefulSet/Pod security context and admission policy result;
- node pool or scheduling policy showing Vault isolation assumptions;
- evidence that swap and core dumps are disabled or an explicit exception with compensating controls;
- proof that Vault pods cannot be modified with `exec`/ephemeral debug by normal operator roles.

### 2.2 Seal/unseal and key custody

- Prefer auto-unseal with cloud KMS or HSM.
- If Shamir unseal is used, define M-of-N quorum, named key custodians, and recovery steps.
- Store unseal material outside day-to-day operator access.
- Test recovery and unseal procedures at least quarterly.

### 2.3 Administrative model

- Root token is break-glass only.
- Day-to-day admin tasks use named identities through OIDC/SSO with MFA.
- Split privileges between platform admin, security admin, and emergency admin.
- Policy changes and auth-mount changes require review and audit traceability.

### 2.4 Auth methods and trust boundaries

- Kubernetes auth for in-cluster workloads.
- OIDC for humans.
- JWT/OIDC for CI pipelines.
- AppRole only where stronger identity attestation is not available.

Kubernetes auth minimums:

- Bind roles to exact `serviceAccount` and namespace.
- Set and validate `audience` for Kubernetes auth roles. `bound_audiences` is the JWT/OIDC auth role parameter; do not use it in Kubernetes auth role examples.
- Keep `alias_name_source=serviceaccount_uid` for Kubernetes auth roles unless there is an approved reason to use `serviceaccount_name`. Name-based aliases tolerate ServiceAccount deletion and recreation worse, so they require strict ServiceAccount creation controls and separate risk acceptance.
- Do not make a long-lived reviewer JWT the default TokenReview strategy. If Vault runs inside Kubernetes, prefer the Vault pod's local service account token or the client JWT pattern; a long-lived reviewer token is acceptable only as an exception with owner, rotation, RBAC scope, and review expiry.
- Use explicit Vault token parameters instead of generic "short-lived" wording:
  - `token_ttl`: `15m` default for initial TTL of workload login tokens
  - `token_max_ttl`: `<=1h` as the cap for renewable service tokens that the workload or Vault Agent can renew
  - `token_type=batch`: use for jobs and short-running workloads that do not need renewal, child tokens, or lease tree semantics
  - `token_period`: only for periodic long-running workload tokens, with explicit role owner, renewal monitoring, and incident revocation path
  - `token_explicit_max_ttl`: set when the role needs a hard cap that renewal cannot exceed
  - Human/admin token TTL belongs to the OIDC/SSO auth method policy: `<=1h`, no non-expiring admin tokens
- Use short-lived batch tokens for jobs and one-shot workloads only when their TTL fits the incident containment deadline: they have no accessor and cannot be individually revoked or renewed. Choose service tokens when immediate individual revocation is required. For long-running services through Vault Agent, a renewable service token is acceptable when it has a short `token_ttl`, a bounded `token_max_ttl` or `token_explicit_max_ttl`, and renewal monitoring.
- Treat periodic tokens as an exception path: use `token_period <=15m`, renewal failure alerting, and `token_explicit_max_ttl <=24h` unless a documented platform exception explains why the token must remain renewable indefinitely.
- Do not use periodic tokens for human or administrator sessions.
- Avoid wildcard role bindings.

Example Kubernetes auth role:

```bash
vault write auth/kubernetes/role/payments-api-prod \
  bound_service_account_names=payments-api \
  bound_service_account_namespaces=prod-payments \
  audience=vault \
  token_policies=payments-api-prod \
  token_ttl=15m \
  token_max_ttl=1h
```

### 2.5 Audit and detection

- Enable Vault audit devices before onboarding live workloads.
- Write audit logs to durable and access-controlled sinks.
- Enable at least two audit devices where operationally feasible. If only one audit sink is used, record the availability risk explicitly: Vault can refuse requests when all enabled audit devices are unable to write.
- Monitor audit device health, write failures, disk/backpressure signals, and sink reachability.
- Alert on unusual auth failures, policy changes, and sudden read-volume spikes.
- Correlate Vault audit events with Kubernetes audit logs and runtime telemetry.
- Restrict access to audit logs. Vault hashes sensitive values in audit entries, but audit logs still contain high-value metadata and may include non-hashed request headers unless explicitly configured.

### 2.6 Operational resilience

- Keep encrypted backups and verify restore procedures.
- Run failover and disaster recovery exercises with explicit RTO/RPO targets.
- Capacity test authentication bursts (node restarts, mass pod rollouts).

## 3. Security of Secrets

### 3.1 Data model and ownership

- Assign an owner for each secret path.
- Store only secret data; do not use Vault as a general data store.
- Classify secrets by impact (for example: customer data path access, payment access, internal-only).
- Tie each class to TTL and rotation requirements.

Baseline secret classes (minimum):
- Critical (payments, live DB admin, signing material):
  - Dynamic lease TTL: `5-15m`
  - Max TTL: `<=1h`
  - Static secret rotation: every `30d`
  - Revoke SLA during incident: `<=15m`
- High (service-to-service live-environment credentials):
  - Dynamic lease TTL: `15-30m`
  - Max TTL: `<=4h`
  - Static secret rotation: every `60d`
  - Revoke SLA during incident: `<=30m`
- Recommended (internal non-critical automation):
  - Dynamic lease TTL: `30-60m`
  - Max TTL: `<=8h`
  - Static secret rotation: every `90d`
  - Revoke SLA during incident: `<=60m`

### 3.1.1 Choosing between Vault and an application database

Choose storage based on the purpose and lifecycle of a value, not only on its confidentiality. A value belongs in a secret manager when knowledge of the original value enables authentication, grants authority, enables signing or decryption, and the value must be issued, rotated, or revoked independently of application data.

| Value type | Default placement | Notes |
|---|---|---|
| Database, cloud, broker, and service-to-service credentials | Vault dynamic secret engine | Prefer a short-lived credential with a lease and revocation over a static password or token. |
| API keys, OAuth client secrets, webhook secrets, and external integration credentials | Vault KV when the provider does not support dynamic issuance | Each value must have an owner, scope, rotation, and incident revocation path. |
| Signing keys, CA/intermediate private keys, and other non-exportable cryptographic keys | Vault Transit/PKI or an approved KMS/HSM | The application should request a cryptographic operation without receiving the private key when the integration supports it. |
| Workload TLS private keys and certificates | Vault PKI or an approved certificate manager | Prefer automated issuance and renewal; do not store the private key in the application database. |
| User password verifier | Application identity database | Store only the output of an approved password hashing algorithm with a unique salt and required parameters; plaintext or reversibly encrypted passwords are not acceptable. A verifier remains sensitive authentication data and requires strict access. |
| One-time activation, password-reset, or similar bearer token | Application database as a verifier/hash when the protocol permits | Store expiry, usage status, and the associated subject; expose or deliver the original value only once. If a downstream dependency requires recovery of the original value, apply the recoverable-secret rules below. |
| PII, payment, health, and other business records | Application database or specialized data store | This is sensitive data, but Vault is not a general data store. Apply the data classification, authorization, retention, and encryption controls for the relevant domain. |
| Public identifiers, certificate serials, secret versions/references, and Vault paths | Application database or configuration store | A reference must not contain a secret value or grant access by itself. |
| Non-secret configuration | Configuration store, ConfigMap, or application database | Do not put it in Vault merely because it relates to a protected service. |

Recoverable secrets, such as a large population of per-user or per-tenant OAuth refresh tokens, may be stored in an application database only when keeping every value in Vault is operationally unsuitable or the product requires transactions and queries over metadata. This is an approved architectural decision, not a routine fallback. Minimum requirements:
- encrypt every value at the application layer using envelope encryption; ciphertext, nonce/IV, authentication tag, wrapped data-encryption key, and non-secret metadata may reside in the database, while the key-encryption key must remain in Vault Transit, KMS, or HSM and must not be directly accessible from the database;
- bind ciphertext to immutable record context through authenticated additional data when the selected scheme supports it, preventing ciphertext substitution between tenants or records;
- grant the workload only the minimum encrypt/decrypt permissions; separate access to database ciphertext from key administration and prohibit bulk decryption for routine human and support roles;
- exclude plaintext, encryption context containing sensitive values, and cryptographic material from logs, traces, analytics, backups, and error responses;
- document ownership, rotation/re-encryption, downstream credential revocation, recovery, audit, and behavior during Vault/KMS unavailability;
- treat compromise of an application with decrypt permission as compromise of the secrets available to it: encryption at rest does not protect against an authorized runtime.

Do not store plaintext or merely base64-encoded reusable credentials in an application database. Disk encryption, transparent database encryption, and encrypted backups are additional controls, but alone they do not separate keys from ciphertext and do not replace application-layer envelope encryption for recoverable secrets.

### 3.2 Prefer dynamic secrets

Use dynamic engines whenever available (database, cloud, broker credentials).
- Issue short-lived credentials.
- Renew only while workload is healthy.
- Revoke leases immediately for decommissioned workloads or incidents.

Use the TTL returned by issuance or renewal, not the requested increment, to schedule the next renewal or replacement. Test revocation against the downstream service: removing a lease record is not sufficient evidence that credentials no longer work. KV values have no revocable lease; token revocation prevents further Vault access but does not invalidate a copied static password or API key. Rotate or revoke those values at their issuer.

Operational commands:

```bash
vault lease lookup <lease_id>
vault lease revoke <lease_id>
vault lease revoke -prefix database/creds/payments-ro
```

### 3.3 Static secret controls

If static secrets are unavoidable:
- Define rotation cadence (for example 30/60/90 days by class).
- Use overlapping rollout (new value live, app switched, old value revoked).
- Rotation overlap window must be explicit:
  - default `30m`
  - maximum `24h` (requires exception approval)
- Keep emergency rotation runbooks for every critical secret class.

### 3.4 Policy boundaries for secret access

- Separate `dev`, `stage`, and `prod` paths.
- Separate services by path and policy.
- Grant only required capabilities on exact paths (capabilities depend on the specific secret engine and path semantics; do not treat `read`, `list`, `update` as a universal default set).

Reject patterns like broad shared policy scopes:

```hcl
path "kv/*" {
  capabilities = ["read", "list"]
}
```

### 3.5 PKI: issuance, rotation, revocation

- Keep root CA offline or heavily restricted.
- Issue service certificates from intermediates.
- Restrict PKI roles by domain, SAN rules, key type, and TTL.
- Rotate certificates before expiry through automation.

PKI roles default to `generate_lease=false`: certificate validity is governed by its X.509 expiry, and revoking the issuing token does not automatically revoke such a certificate. Record the role's lease/storage settings and test the actual revocation path. `tidy` removes eligible expired records after the configured buffer; it is maintenance, not a replacement for revocation or incident evidence retention.

Compromise response for certificates:
1. Revoke by serial number when Vault stores the certificate. With `no_store=true`, test the supported bring-your-own-certificate (BYOC) revocation path in advance; ordinary serial-only revocation is unavailable.
2. Confirm CRL/OCSP publication and downstream consumption.
3. Re-issue certificate and redeploy affected workload.
4. Investigate usage from audit evidence.

Operational commands:

```bash
vault write pki_int/revoke serial_number="39:dd:2e:..."
vault read pki_int/crl
vault write pki_int/tidy tidy_cert_store=true tidy_revoked_certs=true safety_buffer=72h
```

Important: revocation works only where relying systems actually validate CRL/OCSP. Separately terminate established connections if they do not recheck certificate status within the response deadline.

### 3.6 Token hygiene

- Do not keep long-lived broad tokens.
- Login through non-`token` auth methods issues orphan tokens: revoking an assumed parent will not stop them. Do not create additional orphan tokens without justification; test individual service-token revocation by accessor. For batch tokens, test revocation of a known parent when the token is not orphan, or bound residual access by TTL and revoke issued credentials at their issuer.
- Revoke tokens for offboarded users/services immediately.
- Use accessors in incident workflows to avoid exposing full token values.

```bash
vault token lookup -accessor <accessor>
vault token revoke -accessor <accessor>
```

## 4. Application Secret Handling

### 4.1 Integration patterns

Use one approved pattern per workload and document why it was chosen.

This section compares ways to deliver secrets from Vault. It does not mean Vault is mandatory for every Kubernetes secret; the decision between native Kubernetes Secret, sync-based delivery, and file-only external secret manager delivery is covered in the [Kubernetes Secrets playbook](/en/platform-security/kubernetes/secrets/playbook/).

Pattern A (preferred): Vault Agent Injector
- Secrets rendered into files at runtime.
- Works well for apps that support reload/restart on change.
- Avoids storing runtime secret values in Kubernetes Secret objects.

Pattern B: Secrets Store CSI Driver (Vault provider)
- Mounts secrets as files via CSI.
- Use when teams already depend on CSI volume workflows.
- Avoid syncing into Kubernetes Secret unless there is a hard compatibility requirement.

Pattern C: External Secrets Operator
- Use when application or platform constraints require Kubernetes Secret objects.
- Treat this as higher exposure than file-only delivery.
- Require etcd encryption at rest and strict RBAC.

For all three patterns, distinguish storage location from the application interface. Vault Agent Injector and file-only CSI keep the value out of Kubernetes Secret and expose it as a file. External Secrets Operator first copies the value from Vault into a Kubernetes Secret; the application should then normally consume it as a file through a Secret volume, while environment-variable delivery is permitted only as an exception under the Kubernetes Secrets playbook.

### 4.2 Minimal Injector example

The Vault Agent Injector mutates the Pod and mounts its own shared memory volume at `/vault/secrets` by default. Do not add a manual `emptyDir` or application `volumeMount` for that path unless you have a tested custom injector configuration; otherwise the example can conflict with the mutation or hide how the injector actually works.

This example disables the default Kubernetes API-audience ServiceAccount token mount and uses a dedicated projected ServiceAccount token with `audience: vault`. Vault Agent Injector mounts that volume only into the agent/init containers and reads the login JWT from its service-account token path. Keep the token short-lived and aligned with the Vault Kubernetes auth role `audience`.

The application container must not mount the projected Vault login token. It should read only rendered secret files from `/vault/secrets`; otherwise a compromised application process can use the projected JWT to authenticate to Vault directly under the workload role.

The template serializes each value as JSON so that quotes, backslashes, and line breaks in credentials cannot change the file structure. The Injector does not export the fields into the process environment. The application must parse `/vault/secrets/app-config.json` as JSON, require string values for `DB_USER` and `DB_PASS`, and reject missing or invalid fields. Do not execute the file through a shell or copy its values into command-line arguments, logs, or durable writable storage.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payments-api
  namespace: prod-payments
spec:
  selector:
    matchLabels:
      app: payments-api
  template:
    metadata:
      labels:
        app: payments-api
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "payments-api-prod"
        vault.hashicorp.com/agent-service-account-token-volume-name: "vault-token"
        vault.hashicorp.com/auth-config-token-path: "/var/run/secrets/vault.hashicorp.com/serviceaccount/token"
        vault.hashicorp.com/agent-inject-containers: "app"
        vault.hashicorp.com/agent-inject-secret-app-config: "kv/data/prod/payments/api"
        vault.hashicorp.com/secret-volume-path-app-config: "/vault/secrets"
        vault.hashicorp.com/agent-inject-file-app-config: "app-config.json"
        vault.hashicorp.com/agent-inject-perms-app-config: "0400"
        vault.hashicorp.com/agent-run-as-user: "10001"
        vault.hashicorp.com/error-on-missing-key-app-config: "true"
        vault.hashicorp.com/agent-inject-template-app-config: |
          {{- with secret "kv/data/prod/payments/api" -}}
          {
            "DB_USER": {{ .Data.data.username | toJSON }},
            "DB_PASS": {{ .Data.data.password | toJSON }}
          }
          {{- end -}}
        # If Vault is reached through a non-default service or private CA, also set:
        # vault.hashicorp.com/service: "https://vault.vault.svc:8200"
        # vault.hashicorp.com/tls-secret: "vault-ca"
        # vault.hashicorp.com/tls-server-name: "vault.vault.svc"
    spec:
      serviceAccountName: payments-api
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      volumes:
        - name: vault-token
          projected:
            sources:
              - serviceAccountToken:
                  path: token
                  audience: vault
                  expirationSeconds: 600
      containers:
        - name: app
          image: ghcr.io/example/payments-api:1.0.0@sha256:<digest>
          securityContext:
            runAsNonRoot: true
            runAsUser: 10001
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
            capabilities:
              drop: [ALL]
```

The tag in `tag@sha256` is for readability. Live admission/deploy policy must enforce the digest as the immutable artifact identity.

Apply the [Pod security profile](/en/platform-security/kubernetes/pod-security/playbook/) to the rendered Pod after injection. Pod-level seccomp is inherited unless a container overrides it; capability drops and `allowPrivilegeEscalation: false` must hold for every ordinary and init container, including Vault Agent containers. Keep Injector security-context generation enabled and verify the deployed Injector's actual output against the namespace's pinned Restricted version. This application fragment alone does not prove the injected Pod passes admission.

Verification:
- Confirm admission accepts the injected Pod under the selected Restricted profile and rejects missing or unsafe required fields; do not weaken the namespace policy to run the example. Check file permissions and successful secret rendering after injection.
- Inspect the final pod specification to confirm that the application container does not mount `vault-token` while the agent does. If checking the path through `kubectl exec`, first confirm that the command works and the image contains the tool: missing `ls` or exec failure does not prove token absence.
- Vault Agent auto-auth must still succeed, and `/vault/secrets/app-config.json` must be present in the application container after injection.
- Deployment policy must reject the same manifest if the image is changed to a tag-only reference.
- With synthetic credentials containing quotes, backslashes, line breaks, and shell command syntax, verify that JSON parsing preserves the original strings and causes no command execution. Do not use live credentials for this test.

### 4.3 Application contract

Each service must define and test:
- Where secret files are read from.
- Which UID/GID and file mode allow only the intended application container to read the file; the application must not weaken permissions after startup.
- How rotation is applied (live reload, SIGHUP, or controlled restart).
- Whether the application reopens the file after an atomic update, avoids retaining a stale file descriptor, and closes old connections that use the previous credential.
- How startup fails safely if secret retrieval is unavailable.
- How logs and metrics avoid leaking secret values.
- That the secret file exists only in a runtime volume and is not copied into an image layer, persistent volume, backup, support bundle, or crash artifact.

Runtime behavior during Vault outage must be explicit for already-running pods:
- Define per secret class whether the service fails closed or uses bounded stale credentials.
- If stale credentials are allowed, maximum stale window must be documented:
  - Critical: `0m` (fail closed)
  - High: `<=15m`
  - Recommended: `<=60m`
- After the window expires, stop operations requiring secrets, including background work and use of established connections, and fail pod readiness. Readiness alone does not stop the process or existing connections. Resume processing only after obtaining valid secrets; an outage window does not permit expired or revoked credentials.
- During a Vault outage, pause planned rotation until coordinated switching can safely resume. Emergency revocation of compromised credentials at their issuer must remain possible independently of Vault availability.

### 4.4 CI/CD boundary

- CI can deploy and configure, but runtime secret reads belong to workload identity.
- Do not bake secret values into images, Helm values files, or generated manifests.
- Do not pass secrets through pipeline logs or artifact storage.

### 4.5 Rotation playbook for service teams

1. For a static secret, create or change credentials in the target system and store the new value in Vault; for a dynamic secret, obtain new credentials through the appropriate secrets engine. If the target cannot accept old and new credentials concurrently, agree on the switching sequence and acceptable interruption in advance.
2. Trigger rollout or reload.
3. Validate service health and downstream connectivity with the new value across all replicas and background workers, including connection pools.
4. After confirming consumer migration and closing the agreed overlap window, revoke old credentials in their issuing system or through supported lease revocation. For a compromise, follow the immediate revocation procedure.
5. Within the revocation SLA, confirm that fresh authentication with old credentials fails and check existing connections and derived sessions. Deleting a KV version or observing no lease does not prove revocation of a static secret in the target system; clean up old Vault versions separately under the retention policy.

### 4.6 Common mistakes in applications

- Reading secrets only once at boot when TTL is shorter than pod lifetime.
- Using environment variables for high-value long-lived secrets.
- Sharing one Vault role across unrelated services.
- Skipping failure-path testing for Vault outages.

## 5. Incident Actions

### 5.1 Suspected workload token theft

1. Revoke a service token by accessor and revoke associated leases. For a batch token, apply section 3.6; do not assume individual revocation. Verify loss of Vault access and rejection of issued credentials by their target systems.
2. Tighten or disable affected role.
3. Rotate related secrets.
4. Redeploy workload with reviewed policy.

### 5.2 Suspected secret exfiltration

1. Identify impacted paths and owners.
2. Rotate by secret class.
3. Increase monitoring for replay and lateral movement.
4. Build timeline from Vault and Kubernetes audit trails.

### 5.3 Compromised CI identity

1. Disable CI auth role/mount.
2. Revoke CI-issued service tokens and associated leases using a verified path prefix. Apply section 3.6 to batch tokens. Disabling a role stops new logins but does not itself prove that previously issued tokens are invalid.
3. Rotate all secrets accessed by that CI scope.
4. Re-enable with narrowed policy and stronger identity constraints.

## 6. Release Sign-off Checklist

- Vault admin model excludes root token from routine work.
- Roles are tightly bound to workload identity (`serviceAccount`, namespace, audience).
- Kubernetes auth uses `alias_name_source=serviceaccount_uid`, and reviewer JWT strategy does not depend on a non-expiring ServiceAccount token without an exception.
- Policy scopes are explicit by environment and service.
- Secret class ownership, TTL, and rotation cadence are documented.
- Each recoverable secret has a documented Vault-versus-application-database decision; database-backed designs demonstrate envelope encryption, external key-encryption-key storage, and restricted decrypt scope.
- Certificate revocation is tested end-to-end (issuer to relying service).
- Application secret reload behavior is tested in staging.
- Audit logging and alerting are active and reviewed.
- Backup restore and DR exercises are current.

---

### Recovery Keys and Restore Verification

With auto-unseal, recovery keys authorize recovery operations; they cannot replace the configured KMS/HSM seal mechanism or decrypt the root key when that mechanism is unavailable. Include seal-provider availability, permissions, and key deletion protection in the recovery design.

Treat Raft snapshots as sensitive encrypted backups. Restrict snapshot creation and retrieval, protect storage and retention, and retain the seal dependencies needed to restore. Periodically restore to an isolated environment and verify authentication, policies, secret access, and audit output; record the restore time and any data-loss window. A successful snapshot command alone is not a recovery test.

## 7. Related Materials

- [OIDC + OAuth 2.0 playbook](/en/application-security/identity/oidc-oauth/playbook/)
- [Kubernetes cluster security review playbook](/en/platform-security/kubernetes/cluster-security-review/playbook/)
- [Kubernetes Secrets playbook](/en/platform-security/kubernetes/secrets/playbook/)
- [SLSA provenance overview](/en/supply-chain/slsa-provenance/overview/)
- [Infrastructure technologies reference](/en/reference/infrastructure-technologies/infrastructure-technologies/)

## Preparing materials for sharing

To prepare a separate copy of materials for sharing, use the [Sensitive Data Cleanup skill](/en/ai-automation/security-skills/sensitive-data-cleanup/overview/). See the skill page for processing scope and limitations.
