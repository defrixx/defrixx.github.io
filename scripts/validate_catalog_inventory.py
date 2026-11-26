#!/usr/bin/env python3
"""Read-only integrity check for the migrated catalogue inventory."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    data = json.loads((ROOT / 'catalog/inventory.json').read_text())
    analyzer = data['analyzer']
    skills = data['skills']
    pinned = ROOT / 'analyzer/catalog/requirements.full.json'
    require(sha(pinned) == analyzer['catalog_sha256'], 'Analyzer catalogue digest mismatch')
    source_catalog = json.loads(pinned.read_text())
    require(source_catalog['catalog_version'] == analyzer['catalog_version'], 'Catalogue version mismatch')
    source_ids = [r['id'] for r in source_catalog['requirements']]
    indexed_ids = [r['id'] for r in analyzer['records']]
    require(len(set(source_ids)) == len(source_ids), 'Duplicate Analyzer ID')
    require(source_ids == indexed_ids, 'Analyzer ID inventory mismatch')
    skill_ids = [r['id'] for r in skills['records']]
    require(len(set(skill_ids)) == len(skill_ids), 'Duplicate Skills ID')
    topic_files = sorted((ROOT / 'skills/secure-development/references/topics').glob('*.md'))
    actual_skill_ids = [identifier for path in topic_files
                        for identifier in re.findall(r'^### (SD-[A-Z0-9]+-\d{3}\.C\d{2})(?=\s|$)',
                                                     path.read_text(), re.M)]
    require(len(actual_skill_ids) == len(set(actual_skill_ids)), 'Duplicate source condition ID')
    require(set(actual_skill_ids) == set(skill_ids), 'Skill source condition inventory mismatch')
    for source in analyzer['sources']:
        require(sha(ROOT / 'analyzer/sources' / source['path']) == source['sha256'], 'Pinned source digest mismatch: ' + source['id'])
    for item in skills['records']:
        require(sha(ROOT / item['path']) == item['sha256'], 'Skill reference digest mismatch: ' + item['id'])
    for relation in data['crosswalk']['relations']:
        require(relation['skills_id'] in skill_ids and relation['analyzer_id'] in indexed_ids, 'Unresolved crosswalk ID')
        require(relation['relation'] in {'related','equivalent','narrower','broader','no equivalent'}, 'Invalid relation')
        require(bool(relation.get('rationale')), 'Crosswalk rationale missing')
    print(f'Inventory verified: {len(indexed_ids)} Analyzer IDs, {len(skill_ids)} Skill IDs, {len(analyzer["sources"])} source snapshots, {len(data["crosswalk"]["relations"])} provisional relations.')


if __name__ == '__main__':
    main()
