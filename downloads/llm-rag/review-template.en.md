# Review template: external LLM and RAG

Defrixx · CC BY 4.0 · https://creativecommons.org/licenses/by/4.0/
Source: https://defrixx.github.io/en/hub/llm-rag/overview/
Version: 0.1. Indicate changes when adapting.

## Scope, inputs and decisions

Project/repository/SHA/working-tree state, run_id, time, reviewer and decision owner:

Sources/data classes and owners; ACL/groups; chunk schema/revisions; embedding/ranking/generation providers; disclosure/retention contract; outgoing request content; cache/history; revocation/deletion and receipts; safe citations; budgets/shutdown.

Trust diagram, allowed scenario, prohibited transitions and stop conditions:

Source/document/ACL/class/external-recipient matrix; observed request fields; index/group revisions; cache key/history; revocation timing and in-flight outcome; derived-copy inventory/deletion receipts.

## Requirements and applicability

| ID | Area | Applicability/reason | Implementation/revision | Test IDs | Status | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| RAG-001 | Identity and scope | | | RAG-T-01, RAG-T-02 | not-run | |
| RAG-002 | Authorization before disclosure | | | RAG-T-03, RAG-T-04 | not-run | |
| RAG-003 | Source binding | | | RAG-T-05, RAG-T-06 | not-run | |
| RAG-004 | Provider contract | | | RAG-T-07, RAG-T-08 | not-run | |
| RAG-005 | Untrusted context | | | RAG-T-09, RAG-T-10 | not-run | |
| RAG-006 | Output and links | | | RAG-T-11, RAG-T-12 | not-run | |
| RAG-007 | Cache and history | | | RAG-T-13, RAG-T-14 | not-run | |
| RAG-008 | Revocation and deletion | | | RAG-T-15, RAG-T-16 | not-run | |
| RAG-009 | Secrets and observability | | | RAG-T-17, RAG-T-18 | not-run | |
| RAG-010 | Evaluation and shutdown | | | RAG-T-19, RAG-T-20 | not-run | |

## Finding, repair and recheck

Finding/requirement IDs; hypothesis/confirmation; prerequisites/impact; baseline revision/evidence; proposed/applied repair; repair revision; original/bypass/allowed test; separate recheck observation/verdict:

CSV: test_id/requirement_id link tests/rules; finding_ids links findings; baseline_revision/repair_revision and fix_state separate history/application. retest_id/retest_status/retest_observed/retest_evidence_ref record new checks. Machine keys match in RU/EN. Preserve runs separately and split compound cases before execution.

## Exceptions and human decision

Applicability/reason; exception to an applicable requirement, scope/object/revision, risk, measures, expiry and approving human:

Release / block / more evidence needed; residual risk, unexecuted checks, owner/date:

Initial checks/rechecks are not-run. pass/fail require observations; inconclusive retains uncertainty; not-applicable needs a reason/owner. Include no real secrets or restricted source data.
