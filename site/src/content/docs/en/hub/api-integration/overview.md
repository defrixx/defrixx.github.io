---
template: splash
tableOfContents: false
prev: false
next: false
title: "External API integration: requirements to verification"
description: "A complete learning route for an order service integrating a delivery provider. Produce a trust diagram, requirements, a test matrix and a decision record. Materials and expecte..."
sidebar:
  order: 100
---
A complete learning route for an order service integrating a delivery provider. Produce a trust diagram, requirements, a test matrix and a decision record. Materials and expected outcomes are synthetic; assess your own project locally.

## When to use

The system has multiple tenants, corporate employee login, OAuth access to a partner API and inbound webhooks. Bring data flows, membership and role rules, the partner's OAuth/webhook contract, order transition rules and the selected code revision. If the partner contract is unavailable, mark the relevant requirements unverified and obtain it first.

## Establish the contract before testing

Describe the OIDC client and backend OAuth client separately: trusted issuers, metadata/endpoints, redirect URIs, backend client authentication and scopes. Never obtain server/API addresses from user or webhook parameters; redirects must not disclose tokens to another origin. Do not assume the partner access token is a JWT or an ID Token.

Record OAuth transaction expiry/single use, integration generation, connection states, revocation and retry rules. Outbound calls need an idempotency and reconciliation contract for unknown outcomes; webhooks need exact signed bytes and retry rules. Teaching example numbers do not replace the provider contract.

## Three independent decisions

| Boundary | What it establishes | What to verify separately |
| --- | --- | --- |
| Corporate OIDC | Who signed in: issuer/subject pair and a current session | Tenant membership and permission to connect delivery |
| Employee authority | Whether this employee can manage the chosen tenant's integration | Current permission at initiation and completion |
| Partner OAuth | Which external API resources the backend may access | Partner account, scopes, expiry and revocation |

An ID Token is not a delivery API token. OAuth consent grants no internal administrative rights. A tenant value in a URL, form or webhook is not an authoritative membership source.

## Sequence

1. Record assets, actors and trust boundaries using the [review example](/en/hub/reviews/delivery-api/overview/). Bind tenant, integration, partner account and order.
2. Read the [API playbook](/en/application-security/api/api-security-patterns/playbook/) and [OIDC/OAuth](/en/application-security/identity/oidc-oauth/playbook/); select applicable API-001 through API-009 requirements from the example. These are scenario IDs, not standard clauses or universal corporate policy.
3. Agree the specific webhook contract. The example's synthetic contract is not a substitute for a real provider's documentation.
4. Fill in the template and matrix: allowed and rejected requests, replay, parallel delivery, permission and token revocation. Record revision, observation and verdict for each check. Before execution, the status is `not-run`.
5. Optionally use the [skills catalogue](/en/hub/catalogue/overview/): security-review for assessment, secure-development for separately authorized repairs, security-fix-verification for reassessment. Preserve finding IDs across stages.
6. Deliver the result and open questions to a human. The responsible human makes the real release decision under their team's policy.

## Applicability and result handoff

Record applicability and rationale for API-001 through API-009. `not-applicable` needs a confirmed reason and owner: missing implementation or testing is not non-applicability. An applicable unexecuted check remains `not-run`; insufficient or contradictory observations are `inconclusive`. `pass`/`fail` require observed evidence at the stated revision.

Link each requirement to `test_id`, finding ID, baseline revision, repair revision and a separate recheck outcome. Each run has its own record, preserving history. Track non-applicability separately from accepted exceptions. Scope exceptions by area, expiry, owner, compensating measures and human decision; they cannot make a foreign signature or broken tenant binding pass. Keep the affected operation blocked without a verified safe alternative.

## Download and work locally

<ul class="hub-downloads">
<li><a href="/downloads/api-integration/review-template.en.md" download>Review template (Markdown)</a></li>
<li><a href="/downloads/api-integration/test-matrix.en.csv" download>Test matrix (CSV)</a></li>
</ul>

The template includes trust boundaries, requirements, findings, repairs and rechecks; the CSV provides starter cases and blank results. Files download directly without registration or uploading a project. Use synthetic values in shared reports; exclude original tokens, payloads containing personal data and replacement maps.

## Result and limits

The completed package links requirements to checks and findings at an exact revision. Keep static analysis, expected outcomes and executed observations separate. This site runs no project checks and grants no release approval.

Route version: 0.2, sources in this repository; original prose, diagram and templates use CC BY 4.0 with Defrixx attribution. Code and complete skill packages use MIT. [License boundaries and usage](/en/hub/usage/overview/).
