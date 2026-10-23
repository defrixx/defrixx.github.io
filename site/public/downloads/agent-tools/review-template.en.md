# Review template: AI agent with tools and MCP

Defrixx · CC BY 4.0 · https://creativecommons.org/licenses/by/4.0/
Source: https://defrixx.github.io/en/hub/agent-tools/overview/
Version: 0.1. Indicate changes when adapting.

## Scope, inputs and decisions

Project/repository/SHA/working-tree state, run_id, time, reviewer and decision owner:

User/project and authorization source; read/prepare/write catalog and revisions; MCP transport/issuer/resource; downstream API authority; canonical arguments/object version; approval record; operation ID/ledger; network/files; queues/shutdown.

Trust diagram, allowed scenario, prohibited transitions and stop conditions:

Tool/action/object/user matrix; exact displayed contents; canonical_arguments_hash and target_version; expiry/single use; operation ID/reconciliation method; distinguish dispatched and queued actions.

## Requirements and applicability

| ID | Area | Applicability/reason | Implementation/revision | Test IDs | Status | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| AGT-001 | Authority separation | | | AGT-T-01, AGT-T-02 | not-run | |
| AGT-002 | User and object | | | AGT-T-03, AGT-T-04 | not-run | |
| AGT-003 | Transport and server | | | AGT-T-05, AGT-T-06 | not-run | |
| AGT-004 | Exact approval | | | AGT-T-07, AGT-T-08 | not-run | |
| AGT-005 | Races and object version | | | AGT-T-09, AGT-T-10 | not-run | |
| AGT-006 | Untrusted outputs | | | AGT-T-11, AGT-T-12 | not-run | |
| AGT-007 | Retries and uncertainty | | | AGT-T-13, AGT-T-14 | not-run | |
| AGT-008 | Network and execution boundary | | | AGT-T-15, AGT-T-16 | not-run | |
| AGT-009 | Audit and evidence | | | AGT-T-17, AGT-T-18 | not-run | |
| AGT-010 | Budgets and shutdown | | | AGT-T-19, AGT-T-20 | not-run | |

## Finding, repair and recheck

Finding/requirement IDs; hypothesis/confirmation; prerequisites/impact; baseline revision/evidence; proposed/applied repair; repair revision; original/bypass/allowed test; separate recheck observation/verdict:

CSV: test_id/requirement_id link tests/rules; finding_ids links findings; baseline_revision/repair_revision and fix_state separate history/application. retest_id/retest_status/retest_observed/retest_evidence_ref record new checks. Machine keys match in RU/EN. Preserve runs separately and split compound cases before execution.

## Exceptions and human decision

Applicability/reason; exception to an applicable requirement, scope/object/revision, risk, measures, expiry and approving human:

Release / block / more evidence needed; residual risk, unexecuted checks, owner/date:

Initial checks/rechecks are not-run. pass/fail require observations; inconclusive retains uncertainty; not-applicable needs a reason/owner. Include no real secrets or restricted source data.
