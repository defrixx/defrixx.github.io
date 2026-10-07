---
title: "CI/CD Security Playbook"
description: "Use this playbook when reviewing a pipeline that executes contributor code, publishes packages, obtains cloud credentials, or deploys a release. The asset is the complete delive..."
sidebar:
  order: 30
---
Use this playbook when reviewing a pipeline that executes contributor code, publishes packages, obtains cloud credentials, or deploys a release. The asset is the complete delivery path: source, workflow definition, executor, dependencies, artifact, identity, and deployment decision.

## 1. Establish the trust boundaries

Record the repository owner, accepted trigger events, workflow revision, executor pool, network reachability, credentials, artifact stores, and deployment roles. Distinguish code from a fork, code from an internal contributor, and a reviewed release revision. Organization membership alone does not make executable code safe.

The production default is separate execution contexts for pull-request tests, trusted builds, and deployment. A pull request can run arbitrary dependency installation hooks, test code, build scripts, and local actions. Give that context read-only repository access, no production secrets, no cloud identity exchange, and no route to deployment systems. Disable persisted checkout credentials where subsequent code does not need authenticated Git access.

Treat changes to workflows, reusable workflows, action implementations, runner images, policy files, and dependency lockfiles as changes to the delivery security boundary. Require designated owners to review them and protect the branch against bypass. A required check is useful only if an attacker cannot replace its implementation, rename a different check to satisfy the rule, or bypass the rule through another release path.

## 2. Review triggers and permissions

For GitHub Actions, start with `permissions: {}` and grant each job only the permissions it uses. A job that exchanges OIDC tokens needs `id-token: write`; this authorizes token issuance, not a cloud operation. Its cloud trust policy and role permissions supply the remaining boundary. Account for an action's access to `github.token` even when no token input is passed explicitly.

`pull_request_target` executes in the base repository's privileged context. Do not check out the pull request head or execute its scripts, local actions, dependencies, or generated binaries there. Apply the same separation to `workflow_run`: a successful untrusted workflow does not make its code, cache, or uploaded artifacts trusted. A privileged consumer may parse bounded data with a safe parser; it must not execute downloaded content or use an attacker-controlled artifact path as a command.

Pass event fields into commands as quoted environment variables or structured arguments. Do not interpolate pull-request titles, branch names, issue text, or commit messages into generated shell code. Quoting a workflow expression inside a shell string does not remove the code-injection boundary.

Pin third-party actions and reusable workflows to reviewed full commit SHAs belonging to the intended upstream repository. Pin container images by digest and use dependency lockfiles with immutable resolution where the package ecosystem supports it. Track updates through a reviewed process; a permanent pin to a vulnerable revision is not an update strategy.

## 3. Isolate executors and build credentials

Use fresh executor environments for untrusted jobs. For self-hosted infrastructure, destroy the compute instance or equivalent security boundary after the job; re-registration or workspace deletion alone does not remove persistent malware. Do not reuse an untrusted executor for signing or deployment.

A container on a shared privileged host does not provide this isolation. Review Docker socket mounts, privileged containers, host mounts, node credentials, Kubernetes service accounts, management agents, and access to adjacent jobs. Separate pools and network access for public pull requests, trusted builds, and deployment. An ephemeral runner still needs an isolated host and limited network reachability.

Scope build credentials to the required registry or dependency service and operation. Use build secret mechanisms instead of build arguments, image layers, or checked-in configuration. Do not give dependency installation code a production deployment role. If dependencies must be downloaded, allow the required endpoints through an audited egress path and test that metadata services and internal administration endpoints remain inaccessible.

Do not rely on log masking as an access control. Test ordinary and failure paths with a synthetic secret, including debug output, transformed values, uploaded artifacts, test reports, and executor diagnostics. Retain only the evidence needed for investigation and restrict its readers.

## 4. Protect caches and artifact handoffs

Define who can write each cache and which contexts can restore it. Separate caches across trust levels, repository ownership, operating systems, dependency resolution, and toolchain revisions. A key containing a branch name or commit hash does not establish writer authenticity; broad restore prefixes can cross the intended boundary.

Never promote a pull-request cache into a privileged build unless its contents are independently verified against immutable expected inputs. Where that verification is unavailable, rebuild in the trusted context. Treat downloaded archives as hostile: limit size, reject traversal and links escaping the extraction directory, and avoid evaluating configuration or executables obtained from an untrusted run.

At each artifact handoff, bind the artifact digest to the source revision, build identity, expected workflow, and policy result. Names, tags, run success, and upload permissions are insufficient. A report supplied by the build is an assertion until the trusted verifier checks its provenance and subject digest.

## 5. Constrain federation and deployment

Bind the cloud federation policy to the expected issuer, audience, and subject. For GitHub-to-AWS federation, enforce the supported `aud` and `sub` conditions; do not assume arbitrary GitHub claims are directly usable as IAM condition keys. An environment-based subject identifies the environment rather than the branch, so enforce allowed deployment branches or tags in the environment configuration as well.

Separate build publication and deployment roles. Limit each role to explicit repositories, registries, resources, and environments. A deployment role should not edit its own trust policy, expand IAM permissions, modify release approval rules, or replace the verifier. Where a workflow identity can request credentials, prevent unreviewed contributor-controlled code from executing in that job before or after the exchange.

Protected environment approval must cover the reviewed revision and exact artifact digest. Fetch that digest again at deployment and verify it; do not rebuild after approval or resolve a mutable tag as the approved artifact. Make rollback subject to the same identity and integrity checks, with a documented exception process for emergency releases.

## 6. Verify signing and provenance at consumption

Signing is not proof that an artifact is safe. Verify the digest, accepted signing identity and OIDC issuer, trusted builder, provenance subject, and expected source revision before promotion or deployment. A signature from an arbitrary identity must fail. Keep provenance generation outside attacker-controlled build steps to the extent required by the selected assurance level.

For multi-platform images, define whether approval covers the index and its referenced manifests, and verify the objects the runtime can actually pull. Confirm registry promotion preserves the intended digests and required evidence. Verification failures, missing evidence, unsupported formats, and unavailable verification services must stop the protected release path or enter an explicitly recorded exception process.

Read [SLSA and build provenance](/en/supply-chain/slsa-provenance/overview/) and [container image security](/en/supply-chain/container-image-security/playbook/) for evidence formats and image handling. Do not replace signature verification with a label or boolean embedded in an artifact by its producer.

## 7. Run negative tests

Use a disposable repository and non-production roles. Record the trigger, effective permissions, executor identity, artifact digest, cloud audit event, and deployment outcome.

| Scenario | Expected result | Evidence |
| --- | --- | --- |
| Fork changes a test or dependency hook to read credentials | No production credential or metadata access | Effective token scope and denied network request |
| Privileged event downloads a pull-request artifact containing an executable or traversal entry | No execution; unsafe archive rejected | Consumer logs and extraction result |
| Untrusted job writes a cache later requested by a release | Release cannot consume that cache as trusted code | Writer context and release cache resolution |
| Different repository, branch, environment, or audience requests the release role | Federation denied under the configured subject model | Provider denial and decoded synthetic claims |
| Approved artifact is replaced under the same tag | Deployment denied or continues using the approved digest | Requested digest and verifier decision |
| Signed image has a different signer or source revision | Deployment denied | Verified identity and provenance mismatch |
| Old executor is reused after an untrusted job | Pool policy prevents reuse | Executor lifecycle and host teardown evidence |

Static examples in [security policy examples](/en/reference/security-policy-examples/overview/) check selected configuration invariants. They do not exercise these runtime boundaries.

## 8. Prepare compromise response

Stop affected jobs and disable new credential exchanges before rebuilding delivery infrastructure. Preserve restricted executor, workflow, artifact, and cloud audit evidence. Revoke exposed static credentials and contain temporary sessions according to the cloud provider's actual semantics; changing federation trust alone does not invalidate already issued credentials.

Recreate compromised executor hosts and inspect releases, registry writes, caches, and workflow changes made during the exposure window. Rebuild artifacts from a reviewed revision in a trusted context. Re-signing an artifact from the compromised build does not restore trust.

Define the owner and recovery test for every release path, including manual publication and rollback. Completion means an unauthorized release is blocked, a valid release succeeds, and the evidence links the deployed digest to the reviewed source and decision. Use [release governance](/en/review/release-governance/playbook/) for exception ownership and release criteria.
