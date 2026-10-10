# Executable Security Policy Examples

The repository contains three narrowly scoped OPA policies, JSON configuration examples, and 85 allowed/denied scenarios under `examples/security-policies/`. They illustrate how to turn a reviewed requirement into an executable static check. They do not deploy cloud resources or install a Kubernetes admission controller.

## Scope and local assumptions

| Policy | Accepted configuration | Deliberate boundary |
| --- | --- | --- |
| `pod` | One stateless Linux `v1/Pod` in `payments`, using `payments-app`, with no automatic API token, no volumes or host access, digest-pinned images, non-root execution, `RuntimeDefault` seccomp, no privilege escalation, read-only root filesystems, and all capabilities dropped | A strict field allowlist covers ordinary and init containers. Unknown fields fail. This is a local profile, not a complete Kubernetes schema or an implementation of every Pod Security Standard |
| `aws_trust` | One AWS role trust statement for the configured GitHub OIDC provider, `sts:AssumeRoleWithWebIdentity`, exact audience `sts.amazonaws.com`, and exact subject `repo:example@123456/payments@456789:ref:refs/heads/main` | Only this branch-based trust shape is accepted. Environment subjects, wildcard subjects, additional statements, alternative operators, and extra actions fail. Role permissions and live token exchanges are outside the check |
| `slsa_build` | Authenticated synthetic SLSA v1 statement and trusted verifier output for one configured artifact, signer, builder and source revision | Checks only the local decision contract; does not verify cryptography, the complete schema or SLSA Build level |

The names, AWS account `123456789012`, registry `registry.example.com`, and repeated-character image digest are illustrative placeholders. The image reference is syntactically pinned but is not a verified or pullable release artifact. Replace the placeholders with reviewed values before adapting the examples. Namespace and ServiceAccount creation, IAM role permissions, resource policies, and protection of the release branch are separate prerequisites.

This profile checks a Pod creation document and rejects `ephemeralContainers`, including an empty list. Ephemeral containers are added through a separate API subresource; debugging running Pods needs a separate policy, authorization control, and admission test for that operation.

The strict Pod profile deliberately omits ports, environment variables, probes, volumes, and other application settings. Expanding the profile requires review of the new fields and positive and negative cases. Rejecting an unsupported configuration is preferable to silently accepting a field the policy has never evaluated.

GitHub's default `sub` format includes immutable owner/repository IDs for repositories created after 2026-07-15 and for repositories opting in; renames/transfers after that date also migrate the format. Older repositories retain the name-only format until migration, and this rollout does not include GHES. The IDs in this example are synthetic. Before use, obtain the actual subject from an authorized workflow without logging the complete token, verify repository settings and GitHub type, and update the exact expected value. Coordinate the cloud trust change with the subject migration; do not broaden `StringEquals` into a wildcard to bridge formats. Denial cases include wrong owner ID, wrong repository ID and the previous name-only subject.

## Files and execution

The layout is intentionally small:

- `configuration.json` defines the expected namespace, ServiceAccount, OIDC provider, GitHub subject and synthetic SLSA expectations.
- `manifests/pod.json` is a Kubernetes Pod manifest in JSON, which the Kubernetes API accepts as a manifest representation.
- `manifests/aws-trust.json` is an AWS role trust policy document, not the role's resource permissions policy.
- `manifests/slsa-build.json` contains a synthetic authenticated statement and verifier result for the policy contract.
- `policies/pod.rego`, `policies/aws_trust.rego` and `policies/slsa_build.rego` default to denial and implement the three profiles.
- `fixtures.json` contains the complete scenario set; `policies/fixtures_test.rego` runs each scenario through the real policy.

Run from the repository root with Python 3 and Docker available:

```sh
python3 -m unittest discover -s scripts/tests -v
python3 scripts/test_security_policies.py
python3 scripts/test_security_policies.py --policy pod --input examples/security-policies/manifests/pod.json
python3 scripts/test_security_policies.py --policy aws_trust --input examples/security-policies/manifests/aws-trust.json
python3 scripts/test_security_policies.py --policy slsa_build --input examples/security-policies/manifests/slsa-build.json
```

The first command runs eight runner tests and two site generation reproducibility tests. The runner tests cover false and undefined decisions, incomplete and skipped results, invalid JSON, engine failure, and container cleanup on timeout or interruption. The second command validates scenario structure, unique names, allow/deny coverage for each policy, and correspondence between allowed fixtures and published manifests. It runs OPA strict checks and tests, then verifies that OPA executed every expected case. An empty suite, unknown policy, engine error, incomplete report, or failed case returns a nonzero status.

The individual-check commands accept one JSON document and require an explicit boolean `true` decision. Duplicate JSON keys, non-standard numeric values, malformed input, errors, and undefined or `false` decisions fail. Input is serialized again as JSON and written to a temporary file before evaluation. Keep the input format explicit; the script does not split YAML streams, render Helm templates, or extract Pods from controller manifests.

Each engine invocation has a 120-second timeout as a local operational limit for these small examples. On timeout or interruption, the runner separately removes its container by a unique name; terminating the Docker client alone does not guarantee container termination.

OPA 1.21.1 is pinned by image digest in the runner. The container has no network, a read-only filesystem, dropped Linux capabilities, and read-only mounts. Docker may need network access to fetch the pinned image before execution. The commands run locally and in the site build job on pull requests, pushes to main, and manual runs. Unit tests and OPA scenarios must pass before site build and deployment. Repository administrators must separately configure this build check as required for merging; a workflow file alone does not enforce branch protection.

## What the scenarios verify

The Pod cases cover host network/PID/IPC access, host volumes, wrong identity or namespace, automatic token mounting, mutable or malformed image references, empty containers, privilege escalation, writable root filesystems, added capabilities, missing capability drops, root overrides, seccomp overrides, unsupported fields, Windows input, malformed init containers, and missing fields in ordinary and init containers, and ephemeral containers in a Pod creation document. Allowed cases include ordinary and init containers. Malformed top-level inputs are rejected by all three policies.

The IAM cases cover wrong repository, branch, audience, and provider; pull-request and environment subjects; wildcard principal or subject; extra actions or statements; `StringLike`; `NotAction`; `NotPrincipal`; missing trust elements; and malformed statement shapes. The allowed case is the exact reviewed branch profile.

When integrated into an existing CI pipeline, these tests evaluate the policy implementation present in the pull request. They provide regression evidence, not independent approval of a policy change. Protect policy code, expected configuration, fixtures, runner code, and workflow definitions with the same review ownership as the controls they implement. Configure the resulting check as required in repository settings where it is part of the merge decision.

## Apply the result within its boundary

A successful Pod check does not prove caller authorization, image provenance, image availability, seccomp enforcement, network isolation, or cloud identity isolation. Use actual admission enforcement and runtime tests for those boundaries. A successful trust-policy check does not prove that AWS accepts the role, issues the intended session, or restricts its effective resource permissions.

Before production use, validate the rendered configuration against the target platform's schema, test allowed and denied operations in an isolated environment, and verify the enforcement path cannot skip the policy or alter the checked artifact. Use [CI/CD security](../../content/supply-chain/ci-cd-security/playbook.en.md), [Cloud IAM and workload identity](../../content/platform-security/cloud-iam-workload-identity/playbook.en.md), and [Pod security](../../content/platform-security/kubernetes/pod-security/playbook.en.md) for the complete review.

## Synthetic SLSA policy contract

`policies/slsa_build.rego`, `manifests/slsa-build.json` and the `slsa/` fixtures illustrate the policy stage after authentication of an in-toto statement with SLSA v1 provenance. They compare artifact digest, verified signing issuer/identity, builder, build type, source revision and the approved external-parameter shape. Optional build timestamps may be absent. Rejected cases change one boundary at a time or remove required evidence; they include invalid signatures, wrong identities/digest/revision, unapproved parameters, v0.2 data and malformed inputs.

The example uses a synthetic build type and fake identities. It does not validate a signature, certificate chain, transparency proof, full SLSA schema or SLSA Build level. The `verification` object represents output from a trusted cryptographic verifier; accepting that object from a producer or caller would defeat the check. In production, bind verifier output to the exact authenticated statement and the artifact digest computed by the deployment system, and prevent callers from editing expected configuration. Add negative tests for the real verifier, including a signed statement changed after signing, before using a release gate. This is an executable policy contract, not a universal provenance verifier.
