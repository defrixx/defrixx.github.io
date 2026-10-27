# Event integration with Kafka

Local learning route, version 0.1. The example is synthetic; checks on your system are not executed here.

Design event exchange as a boundary between products. Kafka access, authority to emit a business event and a single business effect are separate checks.

## When to use and expected result

Products exchange order events and need scoped topic/group access and safe reprocessing.

Identity/ACL matrix, event contract, idempotent processing, DLQ, synthetic review and tests.

## Inputs

- Broker/client versions, managed or self-hosted platform, listeners, TLS/SASL and certificate/account-to-principal mapping.
- Clusters/environments, topics, consumer groups and transactional.id if used; owners, producer/consumer/admin identities and effective ACLs.
- Event schema, schema-registry subject/version, partition key, tenant/order/event IDs, object version, size and compatibility limits.
- Source/consumer stores, write/offset ordering, retries, rebalance, recovery and reachable external effects.
- Retention/compaction, copies/exports, data classes, DLQ, operator access, retry budgets and re-drive rules.

## Decisions and trust boundaries

| Decision | Boundary |
| --- | --- |
| What ACLs protect | Kafka ACLs authorize resource operations, not tenant-level record filtering. Consumers unable to see all topic records need a different topic/cluster/application boundary. |
| What delivery means | Producer acknowledgement is not a consumer database update. Commit offsets after a durable effect and deduplicate with persistent event IDs. |
| What transactions provide | Idempotent production/Kafka transactions do not automatically make an external API/database atomic. Select a concrete model rather than an exactly-once label. |
| Who re-drives DLQ | DLQ is a separately protected flow with the same data sensitivity. Re-drive checks schema, scope, reason and duplicate effects. |

## Workflow

1. Record topics, groups, environments and principals. Test allowed operations and forbidden group/topic access using the same clients.
2. Agree the business contract and minimal event fields. Check producer authority in the source product: a tenant_id string in a record is not authorization.
3. Select durable publication/processing with persistent event IDs. Exercise crashes around effects/offsets, restart and rebalance.
4. Test incompatible/malicious events, version order and DLQ; perform authorized re-drive retaining original IDs.
5. Test credential rotation/revocation, recovery and retention for every copy. Hand matrix, findings and decisions to owners of both products.

## Requirements and observable expectations

IDs belong to the chosen model, not a corporate standard. Establish applicability and test allowed/rejected cases for each requirement.

| ID | Area | Requirement | Allowed case / result | Negative case / result |
| --- | --- | --- | --- | --- |
| KAF-001 | Identity and transport | Verify TLS/server identity, chosen authentication, principal mapping, rotation and revocation without logging secrets. | Allowed application certificate: Expected principal and protected connection | Foreign certificate, wrong hostname or revoked access: No unauthorized connection/operation |
| KAF-002 | Producer permissions | Limit writes to selected topic/APIs; separate topic creation, ACL changes and administration. | orders-writer publishes to the allowed topic: Publication succeeds with minimal rights | Write foreign topic or request administration: Operations rejected; no publication |
| KAF-003 | Consumer and group permissions | Scope reads by topic and group; test both boundaries including supporting client APIs. | billing-reader uses the selected group: Read and offset commit allowed | Allowed topic with foreign group or vice versa: Unauthorized read/group operation rejected |
| KAF-004 | Environments and business boundaries | Separate environments/identities; topic ACLs neither authorize source business actions nor filter tenant records. | Authorized source approves its own order: Consumer receives the minimal allowed fields | Test principal in prod or forged tenant in source command: Reject access/command before publication |
| KAF-005 | Schemas and untrusted data | Bind topic/type to allowed schema/version, validate size/fields with a safe parser and protect registry changes. | Compatible event version: Schema and business fields accepted | Foreign schema, unknown type or oversized record: No execution/database mutation; controlled failure/DLQ |
| KAF-006 | Publication and retry | Coordinate source change with outbox; retain event ID on retry and verify selected producer settings. | Normal dispatch of a persisted event: Event binds to the source mutation | Crash before/after producer acknowledgement and restart: No lost business event; duplicates retain their ID |
| KAF-007 | Effect and offset | Atomically bind ID/hash ledger and DB effect, then offset; do not infer external exactly-once from Kafka transactions. | One allowed event ID: One committed effect with accounted offset | Crash after DB before offset, rebalance or same ID with changed body: Retry is safe; changed contents rejected |
| KAF-008 | Versions and transaction visibility | Validate object order/version; if Kafka transactions are used, separately choose/test read_committed under the required model. | Next order version; committed transaction if applicable: Allowed transition occurs once | Old version, new ID for same operation or aborted transaction: No duplicate/invalid effect; transactional cases require a reason if non-applicable |
| KAF-009 | DLQ and re-drive | Scope DLQ data/rights/retention, retry budget and authorized re-drive with original ID; never hide dropped events. | Fix the cause and re-drive the selected event: Original ID/history retained; effect remains idempotent | Unauthorized operator, invalid schema or unavailable DLQ: No check bypass; error/unprocessed event remains visible |
| KAF-010 | Retention and recovery | Record data classes, retention/compaction, copies and deletion timing; test quotas, recovery and revocation. | Recover processing from agreed history: Available data and repeated effects are accounted for | Retention expired, quota exhausted or access revoked: No false recovery/immediate-erasure promise; record outcome and decision |

## Example, templates and evidence

[Open synthetic review example](../reviews/kafka-integration/overview.en.md).

<!-- hub:kafka-integration-downloads -->

The matrix contains 20 starter cases with IDs. Split compound scenarios into separate runs/observations before execution. Establish a valid allowed baseline: rejections alone do not establish usefulness.

Link requirement, test ID, finding, baseline revision, proposed/applied repair and a separate recheck. Initial outcomes are `not-run` with empty observations. `pass`/`fail` need observed evidence; `inconclusive` preserves uncertainty. `not-applicable` needs a reason/owner and is not an exception to an applicable rule.

Exceptions record scope, objects/revision, expiry, compensating measures and approving human. They cannot make an access-boundary failure pass. Hand residual risk/unexecuted checks to a human; the site makes no real release decision.

## Working references

- [Kafka infrastructure reference](../../../reference/infrastructure-technologies/infrastructure-technologies.en.md#kafka)
- [Business logic and retries](../../application-security/business-logic/business-logic-abuse/playbook.en.md)
- [Threat modeling](../../review/threat-modeling/playbook.en.md)
- [Our skills and tools](../catalogue/overview.en.md)

Use our independent skills for integration review and repair verification. Supply the Kafka configuration and observations from authorized local checks; the catalogue describes the inputs.

Author: Defrixx. Original prose, diagram and templates: CC BY 4.0. [Usage and licenses](../usage/overview.en.md).
