# Platform Security

For an overall Kubernetes assessment, start with the cluster review, then examine individual security mechanisms. A separate playbook covers secret management in Vault.

| Task | Document | Review scope |
| --- | --- | --- |
| Review a Kubernetes cluster | [Cluster review](./kubernetes/cluster-security-review/playbook.en.md) | An overall cluster review workflow |
| Review Pod configuration | [Pod security](./kubernetes/pod-security/playbook.en.md) | Workload security settings |
| Review Kubernetes secrets | [Kubernetes secrets](./kubernetes/secrets/playbook.en.md) | Secret handling in the cluster |
| Review seccomp | [Seccomp checklist](./kubernetes/seccomp/checklist.en.md) | System call profiles |
| Explore container escape | [Container escape and capabilities](./kubernetes/container-escape-capability-abuse/overview.en.md) | Escape scenarios and capability abuse |
| Validate controls through attack scenarios | [Adversarial validation](./kubernetes/adversarial-validation/playbook.en.md) | Practical validation of Kubernetes controls |
| Review Vault | [Secrets in Vault](./secrets/vault/playbook.en.md) | Secret management with Vault |

## When to use other sections

To review build provenance and container image security, use [supply chain](../supply-chain/overview.en.md).
