---
title: "Platform Security"
description: "For an overall Kubernetes assessment, start with the cluster review, then examine individual security mechanisms. Separate playbooks cover cloud workload identities and secret m..."
sidebar:
  order: 5
---
For an overall Kubernetes assessment, start with the cluster review, then examine individual security mechanisms. Separate playbooks cover cloud workload identities and secret management in Vault.

| Task | Document | Review scope |
| --- | --- | --- |
| Review cloud roles and workload federation | [Cloud IAM and workload identity](/en/platform-security/cloud-iam-workload-identity/playbook/) | Provider trust, ServiceAccount selection, SDK credential sources, node metadata, effective permissions, and containment of issued sessions. |
| Review a Kubernetes cluster | [Cluster review](/en/platform-security/kubernetes/cluster-security-review/playbook/) | Control plane, API access, RBAC, network boundaries, workloads, and admission policies. Includes verifying effective restrictions and recording evidence and cluster review findings. |
| Review Pod configuration | [Pod security](/en/platform-security/kubernetes/pod-security/playbook/) | Process identity, privileges, capabilities, filesystems, volumes, and host access. Also covers ServiceAccounts, resource constraints, debugging surfaces, and Pod Security Standards enforcement. |
| Review Kubernetes secrets | [Kubernetes secrets](/en/platform-security/kubernetes/secrets/playbook/) | Secret access through RBAC and Pod creation, delivery to applications, and storage in etcd and on nodes. Covers external secret stores, registry credentials, negative tests, and access auditing. |
| Review seccomp | [Seccomp checklist](/en/platform-security/kubernetes/seccomp/checklist/) | Profile provenance, completeness of allowed system calls, and effective attachment to containers. Accounts for capabilities, runtime behavior, CPU architecture, application compatibility, and configuration drift. |
| Explore container escape | [Container escape and capabilities](/en/platform-security/kubernetes/container-escape-capability-abuse/overview/) | Container escape scenarios involving excessive privileges, host access, and dangerous capability combinations. Connects attack prerequisites to isolation settings and the limits of individual controls. |
| Validate controls through attack scenarios | [Adversarial validation](/en/platform-security/kubernetes/adversarial-validation/playbook/) | Practical scenarios for network boundaries, RBAC, host access, secrets, and debugging surfaces. Connects execution conditions, expected controls, observed outcomes, and detection evidence for each scenario. |
| Review Vault | [Secrets in Vault](/en/platform-security/secrets/vault/playbook/) | Vault hardening, authentication methods, access policies, auditing, and recovery. Also covers secret and token issuance, rotation and revocation, application integration, PKI, and compromise response. |

## How to choose the review depth

- For an unfamiliar cluster, start with the overall Kubernetes review. Then use the Pod, secrets, and seccomp documents to examine the corresponding settings in detail.
- For a change to one mechanism, open its document directly. The container escape overview helps connect configuration choices to the attack scenarios under review.
- To validate controls already in place, use adversarial validation and follow the conditions for conducting it described in that playbook.
- For a Vault assessment, start with its playbook. Add the Kubernetes secrets document when the review also covers secret storage in the cluster.
- For application or pipeline cloud permissions, start with the Cloud IAM playbook; in Kubernetes also review deployment rights and ServiceAccount selection.

## When to use other sections

To review build provenance and container image security, use [supply chain](/en/supply-chain/overview/).
