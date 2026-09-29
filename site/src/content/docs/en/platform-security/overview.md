---
title: "Platform Security"
description: "For an overall Kubernetes assessment, start with the cluster review, then examine individual security mechanisms. A separate playbook covers secret management in Vault."
sidebar:
  order: 5
---
For an overall Kubernetes assessment, start with the cluster review, then examine individual security mechanisms. A separate playbook covers secret management in Vault.

| Task | Document | Review scope |
| --- | --- | --- |
| Review a Kubernetes cluster | [Cluster review](/Product-security-playbook/en/platform-security/kubernetes/cluster-security-review/playbook/) | An overall cluster review workflow |
| Review Pod configuration | [Pod security](/Product-security-playbook/en/platform-security/kubernetes/pod-security/playbook/) | Workload security settings |
| Review Kubernetes secrets | [Kubernetes secrets](/Product-security-playbook/en/platform-security/kubernetes/secrets/playbook/) | Secret handling in the cluster |
| Review seccomp | [Seccomp checklist](/Product-security-playbook/en/platform-security/kubernetes/seccomp/checklist/) | System call profiles |
| Explore container escape | [Container escape and capabilities](/Product-security-playbook/en/platform-security/kubernetes/container-escape-capability-abuse/overview/) | Escape scenarios and capability abuse |
| Validate controls through attack scenarios | [Adversarial validation](/Product-security-playbook/en/platform-security/kubernetes/adversarial-validation/playbook/) | Practical validation of Kubernetes controls |
| Review Vault | [Secrets in Vault](/Product-security-playbook/en/platform-security/secrets/vault/playbook/) | Secret management with Vault |

## When to use other sections

To review build provenance and container image security, use [supply chain](/Product-security-playbook/en/supply-chain/overview/).
