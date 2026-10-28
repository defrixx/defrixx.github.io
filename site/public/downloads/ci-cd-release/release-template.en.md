# Release decision template

Defrixx · CC BY 4.0 · https://creativecommons.org/licenses/by/4.0/
Source: https://defrixx.github.io/en/hub/ci-cd-release/overview/
Version: 0.2

## Scope and identities

Repository/SHA, workflow revision, run, environment, digest and OCI index/manifest relation:
Builder/signer identity, issuer/audience/subject and trust roots:
Verifier/policy/tool versions and observation time:

Expected predicateType, builder.id, canonical repository/SHA, buildType, allowed externalParameters and policy owner:
Trust origin for the attestation producer and verifier; protect their code/configuration from the artifact being verified:
Bind decision to digest, environment, policy revision and validity period; obtain a new decision when bytes or context change:

## Evidence chain

| ID | Area | Object/digest | Check and reference | Status | Owner |
| --- | --- | --- | --- | --- | --- |
| REL-001 | Source and workflow | | | not-run | |
| REL-002 | Isolation and caches | | | not-run | |
| REL-003 | Permissions and secrets | | | not-run | |
| REL-004 | Artifact integrity | | | not-run | |
| REL-005 | Provenance | | | not-run | |
| REL-006 | Signature and identity | | | not-run | |
| REL-007 | SBOM and scanning | | | not-run | |
| REL-008 | Risk and exceptions | | | not-run | |
| REL-009 | Deployment and rollback | | | not-run | |
| REL-010 | Evidence handoff | | | not-run | |

## Findings and rechecks

Finding ID, hypothesis/confirmation, impact, original revision, proposed/applied repair, new revision, original/bypass/allowed case, observation and verdict:

## Exception

Requirement, digest/revision/environment, risk, compensating measures, owner and approving human, review/expiry date:
A vulnerability exception does not waive provenance or integrity verification.

## Human decision

Release / block / more evidence needed:
Decision owner and date:
Unexecuted checks and limits:
Verified rollback artifact and its admission conditions:

Include no secrets. Never turn not-run or an error into pass. Indicate changes when adapting this template.

## Run, applicability and recheck

Record `run_id`, time, revision/working-tree state and template version 0.2. RU/EN CSV machine headers are identical: `test_id`/`requirement_id` link tests to requirements; `finding_ids` links findings; `baseline_revision`/`repair_revision` identify original/repaired state. `fix_state` separates proposed and applied repairs. `retest_id`, `retest_status`, `retest_observed`, `retest_evidence_ref` hold the separate recheck outcome. Save each new run separately rather than replacing baseline observations.

Fill in `applicability`, `applicability_reason`, `owner`. `not-applicable` needs a reason and owner; absent checks mean `not-run`, uncertain observations mean `inconclusive`. `pass`/`fail` require observed outcomes. Initial checks/rechecks remain `not-run`; empty fields are not evidence. Record exception scope, expiry, compensating measures and approving human separately from non-applicability.
