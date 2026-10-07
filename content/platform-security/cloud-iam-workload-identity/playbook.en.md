# Cloud IAM and Workload Identity Playbook

Use this playbook to review cloud roles assumed by applications, Kubernetes workloads, and CI/CD jobs. Federation replaces stored credentials with an exchange of identity evidence; it does not remove the need to protect the issuer, the caller, and the resulting permissions.

## 1. Map identities to resources

For each workload, record its owner, environment, cloud account or project, issuer, subject, audience, federation mechanism, role, accessible resources, and credential source used by the SDK. Include role chaining, impersonation, resource policies, organization restrictions, permission boundaries, and delegated administration.

Separate workload identities by application and environment. Give production applications a purpose-built identity rather than the node role, a shared default service account, or the deployment administrator's identity. Grant the required actions on explicit resources; review write and administrative operations independently from read access.

Model the full escalation path. Reading a secret is not the only way to obtain a credential: creating a Pod, modifying a controller's Pod template, executing in a container, or requesting a service-account token can expose the workload identity. In cloud IAM, changing trust, passing a role to a service, impersonating an identity, or editing a resource policy may be more powerful than the apparent data-access permission.

## 2. Configure the provider-specific trust boundary

| Mechanism | Identity binding to check | Operational constraint |
| --- | --- | --- |
| AWS IRSA | The intended cluster OIDC provider; exact `sub` for namespace and ServiceAccount; `aud` equal to `sts.amazonaws.com` | Verify projected token use and the supported SDK credential chain; prohibit unintended node-role fallback |
| EKS Pod Identity | Association of cluster, namespace, ServiceAccount, and role; trust for `pods.eks.amazonaws.com` with `sts:AssumeRole` and `sts:TagSession` | Uses EKS Auth and the Pod Identity Agent rather than an IRSA OIDC provider; verify supported compute, SDK, and association propagation |
| Workload Identity Federation for GKE | Intended workload pool and IAM principal or service-account impersonation binding | Namespace and ServiceAccount names can represent the same identity across clusters in the same pool; constrain cluster context where supported or separate the pools/projects |
| Microsoft Entra Workload ID for AKS | Exact OIDC issuer, `system:serviceaccount:<namespace>:<name>` subject, and `api://AzureADTokenExchange` audience in the federated credential | Enable the required cluster integration and `azure.workload.identity/use: "true"` Pod label; verify the supported application credential library |
| CI/CD federation | Expected platform issuer, audience, repository, and release subject accepted by the provider | Enforce branch/environment rules where the cloud does not evaluate those attributes directly |

Do not copy trust policies between these mechanisms. Check the provider's supported condition keys, issuer format, audience, signing-key handling, and authorization model. Validate tokens through the provider or the intended authentication API; decoding a JWT is not signature or audience validation.

Avoid broad subject wildcards for production roles. For GitHub-to-AWS federation, use supported exact `aud` and `sub` conditions for the intended branch or environment. When using an environment subject, branch restrictions belong in protected environment settings. Name-based bindings need a lifecycle owner: deleting and recreating a namespace, ServiceAccount, repository, or project may reuse a trusted name. Remove obsolete bindings and review identity reuse before recreation.

For AKS, the table describes direct federation. The preview identity bindings feature uses `api://AKSIdentityBinding`; direct exchange needs a separate projected token with `api://AzureADTokenExchange`. Do not reuse the token file across these paths without checking its audience.

## 3. Protect Kubernetes identity selection

Treat permission to deploy with a protected ServiceAccount as permission to act as its cloud role. RBAC does not restrict `serviceAccountName` choices merely because the caller lacks permission to read that ServiceAccount. Apply a separate namespace and deployment boundary, or an admission control that checks the authenticated caller and the selected identity.

Cover direct Pods and workload controllers, their updates and subresources, generated Pods, and the controllers that create them. If a controller identity is allowed to create Pods, prevent an untrusted caller from setting the protected identity on the parent workload. Protect admission policies, bindings, exemption labels, and the platform identities that manage them. Test error handling and excluded namespaces as well as the normal match path.

Review `serviceaccounts/token`, `pods/exec`, `pods/attach`, and `pods/ephemeralcontainers`; also check permission to alter Pod templates, cloud associations, and identity annotations. Restrict these operations for privileged workloads and record necessary debugging exceptions. Disable automatic service-account token mounting when no Kubernetes API token is needed, while verifying that explicit provider token projection continues to work where federation requires it.

The [policy examples](../../../reference/security-policy-examples/overview.en.md) validate a single Pod configuration before deployment. They do not authenticate its author or enforce Kubernetes admission and must not be represented as the identity-selection boundary.

## 4. Verify the credential source and network boundary

Inspect the credential chain used by the deployed SDK version. Remove static access keys and environment variables that override federation. On a test instance, identify the effective principal through provider-supported diagnostics and correlate it with a harmless resource request and the audit log. Identity introspection alone does not prove resource permissions.

Prevent ordinary workloads from obtaining the node's credentials. Test the actual runtime network path, including host-network Pods, proxies, IPv6, and SSRF from the application. IMDSv2 is a useful AWS control but does not replace node isolation and access restrictions. On EKS, host-network Pods can reach IMDS; assigning Pod Identity or IRSA does not remove that path.

Preserve the intended workload credential endpoint. GKE uses a metadata integration for workload federation, and EKS Pod Identity uses its agent endpoint. A blanket block on all link-local traffic can break legitimate credential delivery without proving isolation. Test that the assigned workload identity works while node identity and neighboring workload credentials remain inaccessible.

Federation is not a boundary against compromise of the node kernel or a privileged container. Separate workloads with materially different trust requirements onto appropriate compute boundaries and minimize the node's own permissions. Network policy behavior depends on the CNI and metadata path; verify enforcement rather than assuming a manifest is sufficient.

## 5. Review effective authorization

Evaluate the complete permission set, including resource policies and organization controls. Look for wildcard resources, broad role assumption, identity impersonation, credential creation, policy administration, and permissions that let a workload deploy a more privileged workload. Separate business data access from identity administration and release permissions.

Use provider policy analysis and simulation to find mistakes, then exercise a controlled allowed request and denied requests against real non-production resources. Simulators do not reproduce every resource policy, organization control, service-specific condition, or eventual-consistency effect. Record the principal, resource, operation, result, and corresponding audit event.

Choose credential/session duration within provider limits from the workload's renewal behavior and the acceptable exposure window. Document that operational assumption rather than applying one universal TTL. Verify renewal, issuer/key rotation, temporary provider failures, and application recovery without introducing fallback static credentials. Existing resource connections and downstream sessions may survive credential expiration and need their own termination procedure.

## 6. Contain issued credentials

Prepare two separate operations: stop new credential issuance and contain credentials or access already issued. Removing an association or federated trust normally addresses the first operation; do not declare all active sessions revoked as a consequence.

For ordinary AWS IAM role sessions, the session-revocation mechanism attaches an explicit deny conditioned on `aws:TokenIssueTime`. It affects all matching sessions of the role, including legitimate workloads. Retain the deny until affected credentials have expired, prevent new malicious assumptions, and separately contain roles reached through chaining. IAM Identity Center and service-linked roles have different supported procedures. Verify with a harmless resource operation using a captured test session; `GetCallerIdentity` is not an authorization-revocation test.

For Google Cloud and Microsoft Entra integrations, identify the actual issued token type, lifetime, resource authorization behavior, and applicable revocation mechanism. Do not assume deletion of a federated credential immediately invalidates a resource access token. Test the chosen permission removal, resource-side denial, workload shutdown, or provider-supported revocation using a pre-existing session and document propagation time and residual access. Workload shutdown stops that instance from requesting new credentials, but does not invalidate an access token copied by an attacker.

Contain established database sessions, signed URLs, copied secrets, and derived credentials separately. Avoid restoring access by removing a temporary deny before the exposed credentials can no longer be used. Recovery requires clean workload instances, reviewed trust and permissions, and a successful allowed/denied request pair.

## 7. Execute the review scenarios

Use disposable resources and synthetic data. Test as both the application principal and a lower-trust deployer; do not use an administrator's successful request as evidence of workload access.

| Scenario | Required outcome | Verification signal |
| --- | --- | --- |
| Wrong issuer, audience, namespace, or ServiceAccount | No production credential exchange | Provider rejection and selected identity |
| Lower-trust deployer selects a protected ServiceAccount directly or in a controller | Rejected before the workload can obtain credentials | API/admission decision and no cloud access |
| Pod reaches node metadata or another identity endpoint | No usable node or neighboring credentials | Runtime network result and effective principal |
| SDK has an accidental static credential override | Deployment check detects the wrong principal | Credential-source diagnostic and cloud audit |
| Workload accesses an unrelated resource or assumes an unrelated role | Denied | Resource operation and authorization audit |
| Trusted name is deleted and recreated | Obsolete binding does not grant unexpected access | Identity lifecycle record and attempted exchange |
| Issuance is disabled while a session is already active | Existing access is tested and contained separately | Pre-existing session denied on a resource request |
| Provider or agent is temporarily unavailable | Defined recovery without broader credentials | Renewal failure, application behavior, and recovery |

Deliver a mapping of identities to resources, tested trust conditions, escalation paths, and containment procedures with owners. Use [CI/CD security](../../supply-chain/ci-cd-security/playbook.en.md) for pipeline trust and [Vault](../secrets/vault/playbook.en.md) for a separate secret or dynamic credential service.
