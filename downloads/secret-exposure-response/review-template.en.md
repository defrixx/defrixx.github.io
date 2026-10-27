# Review template: Secret exposure in a running service

Defrixx · CC BY 4.0 · https://creativecommons.org/licenses/by/4.0/
Source: https://defrixx.github.io/en/hub/secret-exposure-response/overview/
Version: 0.1. Indicate changes when adapting.

## Scope, inputs and decisions

Project/repository/SHA/working-tree state; run_id/time; incident owner and authorized responder; non-secret credential alias/version; issuer and consumer inventory; earliest exposure and audit gaps; provider/session behavior; continuity decision; protected evidence references:

Record containment, issuer revocation, replacement, consumer switchover, existing/derived access, copy cleanup and recovery/rollback separately. No credential values:

## Requirements and applicability

| ID | Area | Applicability/reason | Implementation/revision | Test IDs | Status | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SEC-001 | Discovery and evidence | | | SEC-T-01, SEC-T-02 | not-run | |
| SEC-002 | Scope and effective permissions | | | SEC-T-03, SEC-T-04 | not-run | |
| SEC-003 | Containment decision | | | SEC-T-05, SEC-T-06 | not-run | |
| SEC-004 | Revocation at the issuer | | | SEC-T-07, SEC-T-08 | not-run | |
| SEC-005 | Replacement and least privilege | | | SEC-T-09, SEC-T-10 | not-run | |
| SEC-006 | Consumer switchover | | | SEC-T-11, SEC-T-12 | not-run | |
| SEC-007 | Sessions and derived access | | | SEC-T-13, SEC-T-14 | not-run | |
| SEC-008 | Copies and safe cleanup | | | SEC-T-15, SEC-T-16 | not-run | |
| SEC-009 | Recovery and rollback | | | SEC-T-17, SEC-T-18 | not-run | |
| SEC-010 | Closure and recurrence prevention | | | SEC-T-19, SEC-T-20 | not-run | |

## Finding, repair and recheck

Finding/requirement IDs; hypothesis/confirmation; impact; baseline revision/evidence; proposed/applied repair; repair revision; original/bypass/allowed tests; separate recheck observation and verdict:

CSV: test_id/requirement_id link tests/rules; finding_ids links findings. baseline_revision/repair_revision and fix_state preserve repair history. retest_id/retest_status/retest_observed/retest_evidence_ref describe a separate check. Preserve runs separately; split compound cases before execution.

## Exceptions and human decision

Residual access/copy, scope, owner, measures, expiry and approving human; containment / recovery / cleanup status; unknown outcomes and next checks:

Initial checks/rechecks are not-run. pass/fail require observations; inconclusive preserves uncertainty; not-applicable requires a reason/owner. A clean scan alone does not close the incident. Include no real secrets or restricted source data.
