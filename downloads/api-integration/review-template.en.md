# External API integration review template

Template author: Defrixx. CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
Source: https://defrixx.github.io/en/hub/api-integration/overview/
Template version: 0.2. Indicate changes when adapting.

## Scope and status

- Project / repository / SHA / working-tree state:
- Mode: design review / code review / repair verification:
- Authorized scope and exclusions:
- Reviewer, date and decision owner:
- All checks start as not-run. Include no real secrets.

## Trust diagram

Describe browser -> corporate IdP -> backend -> partner OAuth -> API -> webhook -> backend -> stores.
Separate iss/sub identity, current employee authority and external API scopes.
Record tenant/integration/partner account/order binding, legal transitions and background job behavior after logout/role revocation.

## Provider contract

Document and version; verification date; callback URI and PKCE; account/scopes verification; token rotation and revocation.
Webhook: exact signed bytes, algorithm, key format/selection, time, retries, maximum size, schema and acknowledgement after commit.
Align retry horizon and deduplication retention. Do not copy teaching ShipCo numbers without a rationale.

OIDC endpoints/client and separate OAuth client, client authentication, transaction expiry, PKCE/session/server binding, integration state/generation:
Disconnect/new integration_id on reconnect, races with webhooks/jobs and already dispatched requests:
Outbound creation: persistent operation key, payload binding, provider idempotency retention, result lookup and stopping on uncertainty:

## Requirements

| ID | Applicability and rule | Rationale | Implementation | Verification | Limits/exception |
| --- | --- | --- | --- | --- | --- |
| API-001 | OIDC and session | | | | |
| API-002 | Current tenant authority | | | | |
| API-003 | OAuth transaction binding | | | | |
| API-004 | Account and minimal scopes | | | | |
| API-005 | Token storage, rotation and revocation | | | | |
| API-006 | Webhook signature and object binding | | | | |
| API-007 | Replay, parallel duplicates and failures | | | | |
| API-008 | Evidence and human decision | | | | |
| API-009 | Outbound delivery idempotency | | | | |

## Findings and rechecks

| ID | Requirement | Status/confidence | Prerequisites and impact | Original evidence/SHA | Repair/SHA | Original/bypass/allowed test | Observed outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F-001 | | hypothesis | | | not applied | not-run | inconclusive |

Separate defect confirmation, repair application and verification. Retain IDs; bind rechecks to exact revisions. Check state before retrying operations with uncertain outcomes.

## Decision

Executed checks and observations; unexecuted checks; remaining risks; exceptions, owners and review dates.
Real release decision, responsible human and date:

## Run, applicability and recheck

Record `run_id`, time, revision/working-tree state and template version 0.2. RU/EN CSV machine headers are identical: `test_id`/`requirement_id` link tests to requirements; `finding_ids` links findings; `baseline_revision`/`repair_revision` identify original/repaired state. `fix_state` separates proposed and applied repairs. `retest_id`, `retest_status`, `retest_observed`, `retest_evidence_ref` hold the separate recheck outcome. Save each new run separately rather than replacing baseline observations.

Fill in `applicability`, `applicability_reason`, `owner`. `not-applicable` needs a reason and owner; absent checks mean `not-run`, uncertain observations mean `inconclusive`. `pass`/`fail` require observed outcomes. Initial checks/rechecks remain `not-run`; empty fields are not evidence. Record exception scope, expiry, compensating measures and approving human separately from non-applicability.
