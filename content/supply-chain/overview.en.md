# Supply Chain

Choose a document based on the task: pipeline security, build provenance, or container image security. A complete delivery assessment covers all three areas.

| Task | Document | Review scope |
| --- | --- | --- |
| Review a CI/CD pipeline | [CI/CD security](./ci-cd-security/playbook.en.md) | Untrusted pull requests, triggers, executor isolation, caches, artifacts, federation, and approval bound to the release digest. |
| Review build provenance | [SLSA and build provenance](./slsa-provenance/overview.en.md) | SLSA Build levels, CI/CD trust boundaries, and the relationship between an artifact and its build provenance. Covers attestation distribution, trusted builder identities, and provenance verification before deployment. |
| Review container images | [Container images](./container-image-security/playbook.en.md) | Dockerfiles, base images, dependencies, build secrets, digests, and multi-architecture images. Covers scanning, signatures, promotion through registries, and image checks before deployment. |

## How to choose the documents

- For executors, workflow permissions, and artifact handoffs, start with the CI/CD playbook.
- If the question concerns an artifact’s origin and build process, start with the SLSA overview.
- If you are reviewing a Dockerfile, container image, or delivery through a registry, start with the image security playbook.
- For a review spanning build and delivery, use all three: CI/CD covers execution and deployment boundaries, SLSA provides provenance context, and the image playbook covers handling container artifacts.

## When to use other sections

For release criteria, use [release governance](../review/release-governance/playbook.en.md). Review runtime configuration with the documents in [platform security](../platform-security/overview.en.md).
