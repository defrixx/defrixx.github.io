---
template: splash
tableOfContents: false
prev: false
next: false
title: "Secret exposure in a running service"
description: "Local learning route, version 0.1. This is a response-planning and review exercise. The synthetic example does not revoke credentials, rotate secrets or change your infrastructure."
sidebar:
  order: 100
---
Local learning route, version 0.1. This is a response-planning and review exercise. The synthetic example does not revoke credentials, rotate secrets or change your infrastructure.

## When to use and expected result

A service credential appears in a repository, build artifact or log. Establish what it could access, stop its use, restore the service with a safe replacement and verify old access separately from copy cleanup.

Result: an exposure timeline, issuer/consumer map, containment and recovery decisions, evidence of old-access denial, copy-cleanup register, synthetic review and reusable test matrix.

## Inputs

- Credential type, issuer, non-secret alias/version, owner, exposure location and earliest plausible exposure time.
- Effective resource permissions, shared consumers, derived tokens/sessions, audit availability and evidence access rules.
- Workload replicas, workers, scheduled jobs, reload behavior, pools, provider revocation semantics and propagation delays.
- Service continuity needs, safe failure behavior, approved incident authority, copy retention and recovery/rollback procedures.

## Decisions and trust boundaries

| Decision | Boundary |
| --- | --- |
| Is it containment or planned rotation? | Suspected compromise needs rapid effective denial; a routine overlap window must not silently prolong exposed access. |
| What invalidates the secret? | The accepting issuer/resource enforces revocation. Deleting a stored value only changes that copy. |
| What remains after revocation? | Existing connections, temporary credentials and sessions need their own provider-specific check. |
| What counts as cleanup? | Copy removal and protected retention are tracked separately from credential usability and service recovery. |

This route coordinates a service incident. The Vault, Kubernetes Secrets and Cloud IAM playbooks define the chosen platform controls; the CI/CD route governs artifact admission. Keep actual provider behavior and observed evidence in the assessment rather than copying a universal revocation deadline.

## Workflow

1. Preserve restricted evidence and an alias-based timeline; identify issuer, privileges, consumers and possible derived access.
2. Use the authorized compromise procedure to deny exposed access. Capture issuer state and any incomplete outcome; do not delay containment for source cleanup.
3. Repair the leak path, issue a scoped replacement and verify delivery/reload for each consumer. Record the service continuity decision.
4. Test old and replacement credentials, established sessions and derived access independently, in an authorized test environment. Exercise stale workers and failed replacement.
5. Track copies and evidence retention; test recovery without reactivation, then hand separate containment, recovery and cleanup decisions to the human owner.

## Requirements and observable expectations

IDs describe this scenario, not a universal corporate policy.

| ID | Area | Requirement | Allowed case / result | Negative case / result |
| --- | --- | --- | --- | --- |
| SEC-001 | Discovery and evidence | Record detection time, affected credential alias/version, exposure surface and protected evidence references. Keep raw values out of tickets, logs and public reports. | Authorized responder records an alias and restricted evidence reference: Timeline and evidence are available only to the incident team | Attempt to include a raw secret in a ticket, scanner export or chat: Further delivery is blocked; retain evidence in restricted storage and account for any disclosure that already occurred |
| SEC-002 | Scope and effective permissions | Map the issuer, principal, environments, resources, privileges, consumers and credentials/sessions obtainable from the exposed secret. Investigate the earliest plausible exposure through containment; absent logs remain an explicit gap. | A service credential is traced to its issuer, consumers and audit history: Resource and time scope include inherited rights and derived access | Only the visible file is inspected; a derived session or shared consumer is omitted: Scope remains incomplete with an owner and next investigation step |
| SEC-003 | Containment decision | For suspected or confirmed compromise, prioritize revocation or effective access denial at the issuer/resource boundary. Do not wait for repository cleanup or treat planned overlap rotation as containment. Record impact, accountable decision owner and any bounded continuity exception. | Responder applies the authorized procedure to test credentials and attempts a protected operation with the old version: The protected operation with old credentials is denied; service impact is recorded | Team waits for all replicas to migrate while exposed credentials retain access: Incident is not declared contained; escalate the remaining exposure and continuity decision |
| SEC-004 | Revocation at the issuer | Revoke or disable the exposed credential at the system that accepts it; record the exact credential/version and result. Deleting a Vault KV value, Kubernetes Secret or application configuration alone is not issuer-side revocation. | Issuer confirms revocation of the selected old credential: A fresh authentication attempt using the old version is denied | Only the stored copy is deleted or the revocation API times out: Revocation remains unconfirmed; verify issuer state and retain effective containment |
| SEC-005 | Replacement and least privilege | Issue a separate replacement with reviewed minimum permissions and secure delivery. Record its alias/version, never its value; verify that the original leak path cannot disclose it again. | Replacement is delivered to the selected workload through its approved secret mechanism: The intended operation succeeds with scoped permissions and no secret in output | Replacement reuses the exposed value or is printed by the same debug path: Replacement is rejected and the leak cause must be repaired |
| SEC-006 | Consumer switchover | Inventory replicas, workers, scheduled jobs, sidecars and connection pools. Verify actual credential reload or restart behavior per consumer; a changed secret object does not establish that a process uses its new value. | All inventoried consumers demonstrate successful use of the replacement: Version evidence and a normal service operation cover every active consumer | A stale worker, environment variable or pool still uses the old version: Recovery remains incomplete; the stale consumer is isolated or updated under the approved procedure |
| SEC-007 | Sessions and derived access | Check existing connections, sessions, leased secrets and temporary credentials separately from new logins. Use provider-specific invalidation/deny mechanisms and account for propagation; record residual access and deadlines instead of assuming immediate termination. | Pre-existing test sessions and newly attempted logins are checked independently: Old access is denied or explicitly contained with measured remaining lifetime | Fresh login fails but an established session or derived credential still performs a protected operation: Containment is not closed until that path is disabled or bounded by an approved residual-risk decision |
| SEC-008 | Copies and safe cleanup | After containment, track repository history, clones, artifacts, logs, caches and backups. Coordinate cleanup without destroying necessary evidence; retained copies have restricted access, owners and deletion dates. Re-encrypting a stored copy does not erase plaintext already disclosed. | Copy inventory records cleaned surfaces and protected retained evidence: Residual copies have access restrictions, deadlines and owners | Latest commit is clean but an old artifact or clone still contains the value: Cleanup remains open for that copy; revoked status and evidence retention remain separate |
| SEC-009 | Recovery and rollback | Validate service health and prevent old configuration, backups or rollback artifacts from re-enabling exposed credentials. If replacement fails, select a clean replacement or bounded safe mode; do not reactivate the compromised credential. | Recovery or rollback uses current authorized credentials: Service works and the compromised version remains unusable | Restored configuration or rollback requests the exposed version: Restore is blocked or isolated before reconnection; no old access is reactivated |
| SEC-010 | Closure and recurrence prevention | Close containment, recovery and cleanup as separate tracked decisions. Preserve issuer results, consumer coverage, old-access tests, protected audit evidence, leak-cause repair and a separate recheck. Unknown outcomes and exceptions retain an owner, deadline and human decision. | A human reviews observed evidence and the repaired leak path: Closure names completed stages and any bounded remaining work | Clean scan or successful deploy alone is used to close the incident: Closure is withheld; missing issuer, session or consumer evidence is explicit |

## Example, templates and evidence

[Open synthetic review example](/en/hub/reviews/secret-exposure-response/overview/).

<ul class="hub-downloads"><li><a download href="/downloads/secret-exposure-response/review-template.en.md">Review template</a></li><li><a download href="/downloads/secret-exposure-response/test-matrix.en.csv">Test matrix</a></li></ul>

The matrix contains 20 starter cases. Run the allowed case as well as the rejection/failure case; split compound cases into separate observations before execution. All initial results and rechecks are `not-run`, with empty observations.

Link requirement IDs, test IDs, findings, exact baseline/repair revisions, implementation state and separate recheck evidence. `pass`/`fail` require observations; use `inconclusive` for unknown outcomes. `not-applicable` requires a reason and owner and does not excuse an applicable rule. Keep credential values and private evidence out of shared templates.

An exception records the exact residual access or copy, owner, compensating measures, expiry and approving human. It cannot relabel working compromised credentials as revoked. Distinguish incident containment, service recovery and pending cleanup in the handoff; the site performs none of these actions.

## Working references

- [Vault response and rotation](/en/platform-security/secrets/vault/playbook/)
- [Kubernetes Secrets](/en/platform-security/kubernetes/secrets/playbook/)
- [Cloud IAM and issued credentials](/en/platform-security/cloud-iam-workload-identity/playbook/)
- [Fix verification](/en/ai-automation/security-skills/security-fix-verification/overview/)
- [Sensitive-data cleanup](/en/ai-automation/security-skills/sensitive-data-cleanup/overview/)
- [CI/CD release](/en/hub/ci-cd-release/overview/)

Use our independent skills to verify selected repairs and prepare cleaned handoff copies. The linked guides define their inputs and permitted scope.

Author: Defrixx. Original prose, diagram and templates: CC BY 4.0. [Usage and licenses](/en/hub/usage/overview/).
