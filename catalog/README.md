# Shared security requirements catalogue

The catalogue provides a versioned release and one index across the Analyzer requirements and Secure Development conditions. `current.json` identifies the release and its SHA-256 digest. Files in `releases/` retain the complete source text, source digests, identifier inventory, provenance and reviewed or provisional links for that version. Preserve older release files when issuing an update.

The index preserves the original namespaces and IDs. Analyzer consumes its existing pinned JSON format, while Secure Development remains independently installable with its Markdown topics. The release records both formats; the catalogue check ensures the files consumed by those components match the current release exactly. It does not substitute one component's requirements for the other's.

Look up a complete record or condition from the current release:

```sh
python3 scripts/shared_catalog.py --get PSH3-AI-ACDB98E9CB42
python3 scripts/shared_catalog.py --get SD-AI-001.C01
```

Run `python3 scripts/validate_catalog_inventory.py` and `python3 scripts/shared_catalog.py --check` to verify inventory coverage, release and source hashes, index contents, identifiers and the current playbook comparison. Lookup returns the same envelope for both namespaces, including the catalogue version, original source, content format, original content and any recorded relationships. It reads the checked release and index. The index can be regenerated with `python3 scripts/shared_catalog.py --write` when the selected release and inventory agree.

## Updating a release

1. Review source changes and their applicability, evidence, provenance, license and compatibility. Preserve existing identifiers and record the rationale for every accepted crosswalk relationship. Do not infer equivalence from similar titles or text.
2. Update the inventory, including source digests, records and reviewed relationships. Run `python3 scripts/shared_catalog.py --refresh-playbook-links` to record current playbook hashes, then review the changed sources; refreshing hashes is not semantic approval.
3. Run `python3 scripts/validate_catalog_inventory.py`, then `python3 scripts/shared_catalog.py --new-release VERSION` with a new version. The command refuses to overwrite an existing release and updates the current pointer and index. Review all generated changes and run `python3 scripts/shared_catalog.py --check` before committing.

The current release contains 821 Analyzer records and 126 Secure Development conditions. Four links are preliminary and marked `related`; the remaining relationships have not been reviewed. The sources use different units of guidance, and semantic reconciliation is unfinished. Preserve unknown relationships rather than treating them as equivalent or unrelated by default.

`playbook-links.json` records the comparison with the 26 pinned Analyzer source snapshots. Changed source files require review before updating the Analyzer catalogue; the release retains the source snapshots and the comparison captured at release creation.
