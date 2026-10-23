---
template: splash
tableOfContents: false
prev: false
next: false
title: "AI agent with tools and MCP"
description: "Local learning route, version 0.1. The example is synthetic; checks on your system are not executed here."
sidebar:
  order: 100
---
Local learning route, version 0.1. The example is synthetic; checks on your system are not executed here.

Review an assistant that invokes tools as well as answering. Separate model proposals, user authority, action approval and actual execution.

## When to use and expected result

An assistant reads tickets and prepares changes, with selected actions on an employee’s behalf.

Read/action boundaries, per-call authorization, exact-parameter approvals, replay and shutdown checks.

## Inputs

- Tool catalog, schema/server revisions: read, draft preparation, write and external side effects; allowed projects/objects.
- User/agent/server identities, delegation, token scopes, object rules and current authorization source.
- MCP transport/revision if used; trusted servers/metadata/endpoints, local processes and their accessible secrets/files.
- Approval UI, parameter canonicalization, target-object version, approval expiry/single use, execution queue and operation ledger.
- Allowed network destinations, execution environments, audit, budgets, shutdown, uncertain-outcome reconciliation and rollback rules.

## Decisions and trust boundaries

| Decision | Boundary |
| --- | --- |
| Read or action | tickets.read does not grant tickets.comment; patches.prepare proposes a change without executing code or automatically saving it. |
| Who authorizes | The tool server checks current user/object rights. MCP tokens limit transport access rather than replacing business authorization. |
| What is approved | The user sees tool, project, object, action and exact contents. Material argument/version changes require new approval. |
| What has executed | A timeout does not establish absence of effects. Reconcile by persistent operation ID before retrying. |

## Workflow

1. Split tools into read, preparation and side effects; exclude code execution and deployment from this model.
2. Carry trusted identity through server-side project/ticket checks; assess MCP transport separately from business permissions.
3. Define immutable proposals and atomic approval consumption; test argument substitution and object changes after review.
4. Exercise injected tool/ticket content, forbidden egress, duplicates and timeouts.
5. Disable the agent with queued work and verify no new effects; complete findings and recheck records.

## Requirements and observable expectations

IDs belong to the chosen model, not a corporate standard. Establish applicability and test allowed/rejected cases for each requirement.

| ID | Area | Requirement | Allowed case / result | Negative case / result |
| --- | --- | --- | --- | --- |
| AGT-001 | Authority separation | Separate read, preparation and write; models cannot grant authority or turn drafts into execution. | Read OPS-17 and prepare a proposal: No write before a separately authorized stage | Reader invokes tickets.comment or requests patch execution: Server rejects the action |
| AGT-002 | User and object | Check current user rights on project/object at every call, delegation and queued execution. | Editor acts in alpha: Only selected object/action allowed | Spoof user/project or revoke role while queued: Reject foreign context; no effect |
| AGT-003 | Transport and server | Pin server/schema/revision, validate token resource and prohibit inbound-token passthrough. | Trusted server and matching token: Transport and business checks run separately | Wrong audience, substituted server or malicious metadata: Reject without token disclosure/SSRF |
| AGT-004 | Exact approval | Approve canonical arguments, tool/version, user, object and expiry; approval is single-use. | Approve the displayed comment: Execute precisely the reviewed content | Change text, path, tool or user after approval: New approval required; old approval is invalid |
| AGT-005 | Races and object version | Bind rights/version checks to effects through conditional mutation or reliable serialization. | Object unchanged after review: Allowed change occurs once | Object changes or rights revoked before write: Stale approval cannot modify new state |
| AGT-006 | Untrusted outputs | Tickets/descriptions/tool outputs cannot grant authority; bound schemas/size and render safely. | Ordinary ticket quoting a command: Quoted command remains data | Tool output requests SEC-42 and token export: No new authority/read or secret disclosure |
| AGT-007 | Retries and uncertainty | Persist operation ID, account for approval atomically and reconcile effects after timeout; retries retain parameters. | Retrieve result of an already executed operation: Return the same result without another effect | Double approval, concurrent execution, crash after write: One effect or visible uncertainty pending reconciliation |
| AGT-008 | Network and execution boundary | Constrain executor destinations/files/secrets; models cannot choose arbitrary URLs/commands. | Allowed ticket service: Only selected destination reachable | Metadata/internal URL or path outside draft directory: Request/path blocked without execution |
| AGT-009 | Audit and evidence | Link user/proposal/argument hash/decision/operation/outcome without logging secrets. | Reconstruct a synthetic action history: Proposal, approval, effect and recheck are distinct | Attempt to log a token or missing outcome record: No secret appears in the log; missing outcome is not success |
| AGT-010 | Budgets and shutdown | Independently block new and queued actions; bound steps/cost/impact and account for already dispatched work. | Operation within agreed budgets: Allowed result and observable accounting | Disable with queued work or exhaust budget: No new effects; dispatched operations reconciled separately |

## Example, templates and evidence

[Open synthetic review example](/en/hub/reviews/agent-tools/overview/).

<ul class="hub-downloads"><li><a download href="/downloads/agent-tools/review-template.en.md">Review template</a></li><li><a download href="/downloads/agent-tools/test-matrix.en.csv">Test matrix</a></li></ul>

The matrix contains 20 starter cases with IDs. Split compound scenarios into separate runs/observations before execution. Establish a valid allowed baseline: rejections alone do not establish usefulness.

Link requirement, test ID, finding, baseline revision, proposed/applied repair and a separate recheck. Initial outcomes are `not-run` with empty observations. `pass`/`fail` need observed evidence; `inconclusive` preserves uncertainty. `not-applicable` needs a reason/owner and is not an exception to an applicable rule.

Exceptions record scope, objects/revision, expiry, compensating measures and approving human. They cannot make an access-boundary failure pass. Hand residual risk/unexecuted checks to a human; the site makes no real release decision.

## Working references

- [Agent security](/en/ai-security/agentic-ai/playbook/)
- [MCP security](/en/ai-security/mcp-security/playbook/)
- [AI-assisted development](/en/ai-security/ai-assisted-development/playbook/)
- [Our skills and tools](/en/hub/catalogue/overview/)

Our independent skills support review and separately authorized repair verification. Consult the catalogue for inputs/tool limits; a skill does not automatically connect to your model, MCP server or Kafka.

Author: Defrixx. Original prose, diagram and templates: CC BY 4.0. [Usage and licenses](/en/hub/usage/overview/).
