# Review template: Event integration with Kafka

Defrixx · CC BY 4.0 · https://creativecommons.org/licenses/by/4.0/
Source: https://defrixx.github.io/en/hub/kafka-integration/overview/
Version: 0.1. Indicate changes when adapting.

## Scope, inputs and decisions

Project/repository/SHA/working-tree state, run_id, time, reviewer and decision owner:

Broker/client versions; clusters/listeners/environments; principals and TLS/SASL; Topic/Group/TransactionalId/API matrix; schema/subject/compatibility; fields/tenant/event ID; outbox/database/offset; retry/rebalance; DLQ/re-drive; retention/copies/recovery.

Trust diagram, allowed scenario, prohibited transitions and stop conditions:

Principal/environment/Topic/Group/operation matrix and default deny; safe event fields; outbox/database/offset order; ID/hash duplicate rule; DLQ recipient/re-drive approval; retained history available for recovery.

## Requirements and applicability

| ID | Area | Applicability/reason | Implementation/revision | Test IDs | Status | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| KAF-001 | Identity and transport | | | KAF-T-01, KAF-T-02 | not-run | |
| KAF-002 | Producer permissions | | | KAF-T-03, KAF-T-04 | not-run | |
| KAF-003 | Consumer and group permissions | | | KAF-T-05, KAF-T-06 | not-run | |
| KAF-004 | Environments and business boundaries | | | KAF-T-07, KAF-T-08 | not-run | |
| KAF-005 | Schemas and untrusted data | | | KAF-T-09, KAF-T-10 | not-run | |
| KAF-006 | Publication and retry | | | KAF-T-11, KAF-T-12 | not-run | |
| KAF-007 | Effect and offset | | | KAF-T-13, KAF-T-14 | not-run | |
| KAF-008 | Versions and transaction visibility | | | KAF-T-15, KAF-T-16 | not-run | |
| KAF-009 | DLQ and re-drive | | | KAF-T-17, KAF-T-18 | not-run | |
| KAF-010 | Retention and recovery | | | KAF-T-19, KAF-T-20 | not-run | |

## Finding, repair and recheck

Finding/requirement IDs; hypothesis/confirmation; prerequisites/impact; baseline revision/evidence; proposed/applied repair; repair revision; original/bypass/allowed test; separate recheck observation/verdict:

CSV: test_id/requirement_id link tests/rules; finding_ids links findings; baseline_revision/repair_revision and fix_state separate history/application. retest_id/retest_status/retest_observed/retest_evidence_ref record new checks. Machine keys match in RU/EN. Preserve runs separately and split compound cases before execution.

## Exceptions and human decision

Applicability/reason; exception to an applicable requirement, scope/object/revision, risk, measures, expiry and approving human:

Release / block / more evidence needed; residual risk, unexecuted checks, owner/date:

Initial checks/rechecks are not-run. pass/fail require observations; inconclusive retains uncertainty; not-applicable needs a reason/owner. Include no real secrets or restricted source data.
