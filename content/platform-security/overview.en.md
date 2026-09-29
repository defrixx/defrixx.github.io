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

## How to choose the review depth

- For an unfamiliar cluster, start with the overall Kubernetes review. Then use the Pod, secrets, and seccomp documents to examine the corresponding settings in detail.
- For a change to one mechanism, open its document directly. The container escape overview helps connect configuration choices to the attack scenarios under review.
- To validate controls already in place, use adversarial validation and follow the conditions for conducting it described in that playbook.
- For a Vault assessment, start with its playbook. Add the Kubernetes secrets document when the review also covers secret storage in the cluster.

## When to use other sections

To review build provenance and container image security, use [supply chain](../supply-chain/overview.en.md).
