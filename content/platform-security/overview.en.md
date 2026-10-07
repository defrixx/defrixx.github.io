# Platform Security

For an overall Kubernetes assessment, start with the cluster review, then examine individual security mechanisms. Separate playbooks cover cloud workload identities and secret management in Vault.

| Task | Document | Review scope |
| --- | --- | --- |
| Review cloud roles and workload federation | [Cloud IAM and workload identity](./cloud-iam-workload-identity/playbook.en.md) | Provider trust, ServiceAccount selection, SDK credential sources, node metadata, effective permissions, and containment of issued sessions. |
| Review a Kubernetes cluster | [Cluster review](./kubernetes/cluster-security-review/playbook.en.md) | Control plane, API access, RBAC, network boundaries, workloads, and admission policies. Includes verifying effective restrictions and recording evidence and cluster review findings. |
| Review Pod configuration | [Pod security](./kubernetes/pod-security/playbook.en.md) | Process identity, privileges, capabilities, filesystems, volumes, and host access. Also covers ServiceAccounts, resource constraints, debugging surfaces, and Pod Security Standards enforcement. |
| Review Kubernetes secrets | [Kubernetes secrets](./kubernetes/secrets/playbook.en.md) | Secret access through RBAC and Pod creation, delivery to applications, and storage in etcd and on nodes. Covers external secret stores, registry credentials, negative tests, and access auditing. |
| Review seccomp | [Seccomp checklist](./kubernetes/seccomp/checklist.en.md) | Profile provenance, completeness of allowed system calls, and effective attachment to containers. Accounts for capabilities, runtime behavior, CPU architecture, application compatibility, and configuration drift. |
| Explore container escape | [Container escape and capabilities](./kubernetes/container-escape-capability-abuse/overview.en.md) | Container escape scenarios involving excessive privileges, host access, and dangerous capability combinations. Connects attack prerequisites to isolation settings and the limits of individual controls. |
| Validate controls through attack scenarios | [Adversarial validation](./kubernetes/adversarial-validation/playbook.en.md) | Practical scenarios for network boundaries, RBAC, host access, secrets, and debugging surfaces. Connects execution conditions, expected controls, observed outcomes, and detection evidence for each scenario. |
| Review Vault | [Secrets in Vault](./secrets/vault/playbook.en.md) | Vault hardening, authentication methods, access policies, auditing, and recovery. Also covers secret and token issuance, rotation and revocation, application integration, PKI, and compromise response. |

## How to choose the review depth

- For an unfamiliar cluster, start with the overall Kubernetes review. Then use the Pod, secrets, and seccomp documents to examine the corresponding settings in detail.
- For a change to one mechanism, open its document directly. The container escape overview helps connect configuration choices to the attack scenarios under review.
- To validate controls already in place, use adversarial validation and follow the conditions for conducting it described in that playbook.
- For a Vault assessment, start with its playbook. Add the Kubernetes secrets document when the review also covers secret storage in the cluster.
- For application or pipeline cloud permissions, start with the Cloud IAM playbook; in Kubernetes also review deployment rights and ServiceAccount selection.

## When to use other sections

To review build provenance and container image security, use [supply chain](../supply-chain/overview.en.md).
