# Shared security requirements catalogue

The catalogue provides a versioned release and one index across the Analyzer requirements and Secure Development conditions. `current.json` identifies the release and its SHA-256 digest. Files in `releases/` retain the complete source text, source digests, identifier inventory, provenance and reviewed or provisional links for that version. Preserve older release files when issuing an update.

The index preserves the original namespaces and IDs. Analyzer consumes its existing pinned JSON format, while Secure Development remains independently installable with its Markdown topics. The release records both formats; the catalogue check ensures the files consumed by those components match the current release exactly. It does not substitute one component's requirements for the other's.

Look up a complete record or condition from the current release:

```sh
python3 scripts/shared_catalog.py --get PSH3-AI-ACDB98E9CB42
python3 scripts/shared_catalog.py --get SD-AI-001.C01
```

Run `python3 scripts/validate_catalog_inventory.py` and `python3 scripts/shared_catalog.py --check` to verify inventory coverage, release and source hashes, index contents, identifiers and the current playbook comparison. The check lists differing playbooks; use `python3 scripts/shared_catalog.py --check-aligned` when a release requires byte-identical sources. A difference requires review and is not automatically an error in a pinned historical catalogue. Lookup returns the same envelope for both namespaces, including the catalogue version, original source, content format, original content and any recorded relationships. It reads the checked release and index. The index can be regenerated with `python3 scripts/shared_catalog.py --write` when the selected release and inventory agree.

## Updating a release

1. Review source changes and their applicability, evidence, provenance, license and compatibility. Preserve existing identifiers and record the rationale for every accepted crosswalk relationship. Do not infer equivalence from similar titles or text.
2. Update the inventory, including source digests, records and reviewed relationships. Run `python3 scripts/shared_catalog.py --refresh-playbook-links` to record current playbook hashes, then review the changed sources; refreshing hashes is not semantic approval.
3. Run `python3 scripts/validate_catalog_inventory.py`, then `python3 scripts/shared_catalog.py --new-release VERSION` with a new version. The command refuses to overwrite an existing release and updates the current pointer and index. Review all generated changes and run `python3 scripts/shared_catalog.py --check` before committing.

The current release contains 821 Analyzer records and 126 Secure Development conditions. Twenty-one links are marked `related`, including session, CI/CD and agentic application overlaps. Each describes a specific overlap, not equivalence between complete records. The remaining relationships have not been reviewed. The sources use different units of guidance, and semantic reconciliation is unfinished. Preserve unknown relationships rather than treating them as equivalent or unrelated by default.

`playbook-links.json` records the comparison with the 26 pinned Analyzer source snapshots. Changed source files require review before updating the Analyzer catalogue. Each release embeds the Analyzer catalogue, skill topic files, inventory and comparison captured at release creation; the separate playbook snapshot files remain in `analyzer/sources/` and the Git history. Retain or archive those files when publishing a release independently.


## Agentic V2 crosswalk

The following **related** relationships are included in release 2026.11.27.1; they are not claims of equivalence. Use the Analyzer record keys to resolve stable IDs from its source catalogue. The Analyzer catalogue and its pinned sources remain unchanged; the updated Secure Development source is identified by its SHA-256 and local catalogue revision.

| Skill condition | Analyzer record key | Shared area |
| --- | --- | --- |
| SD-AI-001.C01 | agentic.tool-content-isolation | Instruction provenance and trust separation |
| SD-AI-001.C02 | agentic.tool-policy-auth | Authorization outside model output |
| SD-AI-001.C02 | agentic.approval-binding | Approved operation and current authority |
| SD-AI-001.C02 | agentic.delegation | Delegated authority |
| SD-AI-001.C04 | agentic.memory-governance | Protected context and persistent state |
| SD-AI-001.C05 | agentic.shared-budgets | Work limits across an agent lifecycle |
| SD-AI-001.C06 | agentic.reproducible-review-evidence | Evidence linked to the reviewed revision |

Keep original applicability predicates and evidence requirements intact. The crosswalk remains partial; review future changes against both complete source records before releasing them.
