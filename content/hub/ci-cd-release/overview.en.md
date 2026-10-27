# CI/CD: requirements for a secure release

Learning route, version 0.2. Connect source, build, artifact and deployment to verifiable requirements and a human decision. The example is synthetic; this site executes no checks on your system.

## When to use and expected result

You release a service through CI/CD and need to decide which artifacts may enter a selected environment. The route is especially useful when introducing container images, workload federation, signing or a separate artifact promotion stage.

Produce trust boundaries, REL-001 through REL-010 requirements, an allowed/rejected test matrix, findings and a release decision record. IDs belong to this route, not an approved corporate policy or an achieved compliance level.

## Inputs

Record repository and exact commit SHA, workflow revision, branch protection, trigger events and the PR/fork trust model. Identify runner types, dependency/cache sources, job permissions, secret delivery, artifact registry and target environment.

Define trusted builder/signer identities, provenance/SBOM formats, verification trust roots, risk rules, owners and exceptions. Missing documents or unavailable checks remain `not-run` or `inconclusive`, never implicit approval. Exclude tokens, private keys and original secrets from reports.

## Decisions and trust boundaries

| Stage | Trusted decision | Input that is not automatically trusted |
| --- | --- | --- |
| Source | Selected repository, SHA and workflow received required review | PR text, branch name, mutable tag or workflow from a fork |
| Build | An isolated runner builds approved source with selected dependencies | Shared cache, another job's output or dependency scripts |
| Artifact | Exact bytes are identified by digest and supporting documents bind to it | Image name, release label or a signature file alone |
| Admission | Integrity checks and risk acceptance are accounted for separately | Signature success instead of risk assessment; manual approval instead of signature verification |
| Deployment | A separate role applies the verified digest to an allowed environment | Substituted tag, rebuild after verification or another deployment request |

Choose who may change workflows and verifier policy, where trusted roots/identities originate and where build authority ends and deployment authority begins. Release approval does not expand a job's permissions.

Promote the same artifact without rebuilding. In the OCI model, verification, provenance, SBOM, scanning and deployment request bind to one digest. For multiple platforms record the relation between the index and selected child manifests. Rollback verifies the prior artifact under current rules rather than bypassing admission.

## Verification policy before execution

For REL-001 define the trusted repository, build-definition revision, triggers and actual CI dependency resolutions. Follow the [CI/CD playbook](../../supply-chain/ci-cd-security/playbook.en.md): a supported, onboarded lockfile or full reviewed SHAs for other cases. A lockfile in a workflow that is not onboarded does not establish dependency pinning.

For REL-005 specify expected format/`predicateType`, `subject`, `builder.id`, canonical source repository/revision, `buildType` and allowed `externalParameters` using the actual builder format. This model rejects unknown external parameters pending policy review. A signed arbitrary JSON document is insufficient. Establish who produces the attestation: an untrusted job's self-report does not inherit protected-builder trust just because it is signed.

For REL-006 pin verifier version/origin, roots of trust, signer/issuer and policy. The unchecked artifact or its PR must not replace verifier code, policy or trust roots. For REL-009 bind the decision to digest, environment, policy revision and validity period; recheck conditions immediately before deployment.

If registry promotion changes manifest bytes/format, the new digest is a new object. Old signatures and decisions do not transfer automatically: record the transformation and obtain required evidence and a fresh decision for the delivered object.

## Requirements

| ID | Requirement for the chosen model | Verification |
| --- | --- | --- |
| REL-001 | Protect source and build definitions; bind an authorized run to exact repo/SHA/workflow | A modified workflow or untrusted fork does not inherit protected-branch trust |
| REL-002 | Isolate jobs/workspaces; partition trusted and untrusted caches | Another job's artifact or poisoned cache cannot substitute the release |
| REL-003 | Grant minimal job/environment permissions; constrain federation by issuer, audience, subject and workflow context | Untrusted PR gets no secrets/deployment credential; foreign claims are rejected |
| REL-004 | Identify artifacts by digest and promote the same bytes without rebuilding | Byte or tag substitution after approval does not change the selected object |
| REL-005 | Verify provenance: subject digest, trusted builder, source revision and selected provenance policy | A validly signed statement from another builder or for another digest is rejected |
| REL-006 | Verify signatures and trust evidence with an explicit identity/issuer, root and applicable time/log policy | Foreign signer, missing proof or verifier error never becomes admission |
| REL-007 | Bind SBOM and scan outputs to the delivered digest; record generator, format, coverage and vulnerability database revision | A source-tree or other-image SBOM is not presented as delivered composition |
| REL-008 | Separate mandatory integrity checks and risk gates; scope exceptions by requirement, digest/revision, owner and expiry | A vulnerability exception cannot bypass forged provenance; an expired exception is invalid |
| REL-009 | Constrain deployment to environment and verified digest; protect decision handoff against substitution and races | Tag replacement, concurrent requests and rollback do not admit an unchecked object |
| REL-010 | Bind results to revisions, run, policy and human owner; protect evidence and exclude secrets | `not-run`, errors and uncertainty remain visible; a human makes the real release decision |

A signature confirms properties of the signed object within the selected trust model. It does not replace provenance, SBOM, vulnerability applicability or risk assessment. SBOM presence also does not establish complete dependency discovery: record generator limits and actual delivered composition.

## Workflow

1. Record inputs and trust handoffs using the [CI/CD playbook](../../supply-chain/ci-cd-security/playbook.en.md), without duplicating the library in your report.
2. Select provenance and artifact checks using [SLSA and provenance](../../supply-chain/slsa-provenance/overview.en.md) and [container images](../../supply-chain/container-image-security/playbook.en.md). A single document does not establish a SLSA level.
3. Assess workload roles and short-lived credentials with [Cloud IAM](../../platform-security/cloud-iam-workload-identity/playbook.en.md). Separately examine secrets, registry access and runner compromise.
4. Fill in the test matrix and [release decision record](../../review/release-governance/playbook.en.md). Use [vulnerability management](../../review/vulnerability-management/playbook.en.md) for reachability, impact and context-specific exceptions.
5. Optionally use [security-review and report triage](../catalogue/overview.en.md) locally; SARIF normalization inventories signals, not release safety. Our prompt/model tools are not provenance/container-signature verifiers. [Policy examples](../../../reference/security-policy-examples/overview.en.md) demonstrate individual OPA checks; passing them does not replace other admission conditions.
6. Assemble the result using the [synthetic example](../reviews/ci-cd-release/overview.en.md). Preserve finding IDs through repair and recheck. A human decides real release readiness, not this site or a green CI indicator.

## Applicability and result accounting

Record applicability, rationale and owner for REL-001 through REL-010. Signature/provenance verification and object binding are mandatory in this OCI model; another delivery model needs a documented alternative, not an empty `not-applicable`. Missing checks stay `not-run`; incomplete observations are `inconclusive`; `pass`/`fail` require observed evidence. Risk exceptions record requirement, artifact, environment, compensating measures, expiry and approving human without hiding the original check outcome.

The CSV separates finding IDs, baseline/repair revisions, repair state and recheck results. New runs do not overwrite history. Hand the matrix over with scope, digest, evidence, executed/unexecuted checks, exceptions, residual risk and a human owner. Establish an allowed baseline before negative scenarios; a rejection alone does not establish that a valid release works.

## Test matrix and result example

The downloadable matrix covers allowed, rejected and recovery cases: untrusted PR, foreign claims, substituted bytes, wrong signer/builder, mismatched provenance/SBOM, missing checks, tag replacement, expired exception and rollback. All initial statuses are `not-run`.

<!-- hub:release-downloads -->

The [release review example](../reviews/ci-cd-release/overview.en.md) contains three teaching findings, proposed repairs and expected rechecks. It is not a verified production-system report.

Original prose/templates: Defrixx, CC BY 4.0. [Usage and licenses](../usage/overview.en.md).
