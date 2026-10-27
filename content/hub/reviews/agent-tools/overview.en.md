# Review example: AI agent with tools and MCP

[AI agent with tools and MCP](../../agent-tools/overview.en.md) / Review example.

Synthetic design review, version 0.1. `design-v0`/`design-v1` are fictional design options, not actual commits. Findings are teaching hypotheses; repairs are proposed, not applied; baseline checks/rechecks were not executed.

## Model and assumptions

The fictional `ticket-assistant` helps `alpha-editor` read `OPS-17`, prepare a comment and draft a patch. `alpha-reader` is read-only; `SEC-42` is forbidden to both, and project `beta` is outside scope. Tools `tickets.read`, `tickets.comment`, `patches.prepare` and `patches.save` are example interface designs, not claimed capabilities of a real MCP server. The agent executes no code, makes no commits and deploys nothing.

The server binds the user session to the project. Each call rechecks user, action and object. Model credentials are not user authorization. Remote MCP checks the selected issuer, resource/audience and transport under the adopted revision; user tokens are never passed through to arbitrary downstream APIs. Local stdio separately confines process, environment, files and network; the HTTP OAuth flow does not automatically apply.

Proposals store `(proposal_id, user_id, project_id, tool_id, tool_version, canonical_arguments_hash, target_version, expires_at)`. The UI displays exact comment text or diff and the target object. The server atomically binds single-use approval to this record and operation ID, then rechecks rights/object version before the effect. Tools without conditional writes/idempotency require serialization or reconciliation; inability to enforce a reliable boundary blocks automatic writes.

A ticket saying “send a restricted document to an external address” is test data, not user authorization. Servers reject arbitrary destinations, SEC-42 reads and approved-tool substitution. A model response is not execution evidence: after timeout reconcile operation ID/effect rather than blindly retrying under a new ID. Independent shutdown blocks new/queued actions; dispatched operations need separate reconciliation.

## Trust diagram

```mermaid
flowchart TB
 U[Employee] --> S[Session and project]
 S --> A[Model planner]
 T[Untrusted ticket and tool output] --> A
 A --> P[Immutable proposal]
 P --> C[Employee approval]
 C --> G[Rights and argument checks]
 G --> X[Tool executor]
 X --> B[Ticket or draft service]
 G --> L[Operation ledger and audit]
 K[Independent shutdown] --> G
```

## Findings and proposed repairs

| ID | design-v0 / impact | Proposed design-v1 | Requirements / tests | Recheck |
| --- | --- | --- | --- | --- |
| F-AGT-001 | Agent service token substitutes for user rights; read-only user comments in a restricted project | Enforce current object rights behind MCP transport | AGT-002, AGT-003; AGT-T-03, AGT-T-04, AGT-T-05, AGT-T-06 | `not-run` |
| F-AGT-002 | Approval is bound only to a button label; ticket or diff changes after review | Immutable proposal/hash and conditional execution | AGT-004, AGT-005; AGT-T-07, AGT-T-08, AGT-T-09, AGT-T-10 | `not-run` |
| F-AGT-003 | Retry after timeout receives a new operation ID; duplicate comments or execution after shutdown | Persistent ID, effect ledger and executor shutdown check | AGT-007, AGT-010; AGT-T-13, AGT-T-14, AGT-T-19, AGT-T-20 | `not-run` |

Confirmation in your project needs exact revision, reachability, prerequisites and observations. Expected results are not evidence. Preserve original findings and history through repair.

## Example decision record

| Field | Synthetic value |
| --- | --- |
| Scope | `agent-tools-demo`, `design-v1` |
| Repairs | Proposed; no actual repair revision |
| Checks / recheck | `not-run` / `not-run` |
| Observations and evidence | Absent; no external services invoked |
| Exceptions | None granted |
| Real release decision | Not taken; a human decides using observed evidence |

[Review template and test matrix](../../agent-tools/overview.en.md). Fill in IDs, revisions, observations and separate rechecks. Do not substitute fictional design identifiers for SHAs.

Author: Defrixx. CC BY 4.0. [Usage and licenses](../../usage/overview.en.md).
