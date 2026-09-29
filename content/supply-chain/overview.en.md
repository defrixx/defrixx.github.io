# Supply Chain

Choose a document based on the task: reviewing build provenance or container image security. A complete delivery assessment may require both.

| Task | Document | Review scope |
| --- | --- | --- |
| Review build provenance | [SLSA and build provenance](./slsa-provenance/overview.en.md) | SLSA and artifact provenance |
| Review container images | [Container images](./container-image-security/playbook.en.md) | Image security throughout build and delivery |

## When to use both documents

- If the question concerns an artifact’s origin and build process, start with the SLSA overview.
- If you are reviewing a Dockerfile, container image, or delivery through a registry, start with the image security playbook.
- For a review spanning build and delivery, use both: the SLSA overview provides artifact provenance context, while the image playbook covers handling container artifacts.

## When to use other sections

For release criteria, use [release governance](../review/release-governance/playbook.en.md). Review runtime configuration with the documents in [platform security](../platform-security/overview.en.md).
