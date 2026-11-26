#!/usr/bin/env python3
"""Build, validate and query the versioned shared requirements catalogue."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'catalog/requirements.index.json'
CURRENT = ROOT / 'catalog/current.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def build():
    inventory = read_json(ROOT / 'catalog/inventory.json')
    current = read_json(CURRENT)
    records = []
    for item in inventory['analyzer']['records']:
        records.append({'id': item['id'], 'namespace': 'analyzer',
                        'source': 'analyzer/catalog/requirements.full.json',
                        'version': item['version'], 'status': item['status'],
                        'domain': item['domain'], 'legacy_ids': item['legacy_ids']})
    for item in inventory['skills']['records']:
        records.append({'id': item['id'], 'namespace': 'secure-development',
                        'source': item['path'], 'source_sha256': item['sha256'],
                        'source_revision': inventory['skills']['revision']})
    return {'schema_version': '1.0', 'catalog_version': current['catalog_version'],
            'release': current['release'], 'release_sha256': current['sha256'],
            'relations_status': inventory['crosswalk']['status'],
            'relations': inventory['crosswalk']['relations'], 'records': records}


def verify_release(index):
    current = read_json(CURRENT)
    expected_path = 'catalog/releases/' + current['catalog_version'] + '.json'
    if (not re.fullmatch(r'[0-9A-Za-z][0-9A-Za-z.-]*', current['catalog_version'])
            or current['release'] != expected_path):
        raise ValueError('Invalid catalogue release path')
    raw = (ROOT / current['release']).read_bytes()
    if digest(raw) != current['sha256']:
        raise ValueError('Catalogue release digest mismatch')
    release = json.loads(raw)
    if release['catalog_version'] != current['catalog_version']:
        raise ValueError('Catalogue release version mismatch')
    inventory = read_json(ROOT / 'catalog/inventory.json')
    if release['inventory'] != inventory:
        raise ValueError('Catalogue inventory differs from release')
    paths = {'analyzer/catalog/requirements.full.json'} | {r['path'] for r in inventory['skills']['records']}
    if set(release['sources']) != paths:
        raise ValueError('Catalogue release source set mismatch')
    for path, item in release['sources'].items():
        content = item['text'].encode('utf-8')
        if digest(content) != item['sha256'] or (ROOT / path).read_bytes() != content:
            raise ValueError('Catalogue source differs from release: ' + path)
    if release['relations'] != index['relations'] or release['relations_status'] != index['relations_status']:
        raise ValueError('Catalogue relation set differs from release')
    return release


def resolve(index, release, identifier):
    matches = [r for r in index['records'] if r['id'] == identifier]
    if len(matches) != 1:
        raise ValueError('Unknown or duplicate requirement ID')
    item = matches[0]
    source = release['sources'][item['source']]
    text = source['text']
    if item['namespace'] == 'analyzer':
        matches = [r for r in json.loads(text)['requirements'] if r['id'] == identifier]
        if len(matches) != 1:
            raise ValueError('Analyzer requirement not found uniquely')
        content_format, content = 'analyzer-json', matches[0]
        revision = release['inventory']['analyzer']['revision']
    else:
        match = re.search(r'^### ' + re.escape(identifier) + r'(?=\s|$)[^\n]*\n.*?(?=^## |^### |\Z)', text, re.M | re.S)
        if not match:
            raise ValueError('Skill requirement not found')
        content_format, content = 'secure-development-markdown', match.group(0).strip()
        revision = release['inventory']['skills']['revision']
    relations = [r for r in index['relations'] if identifier in (r['analyzer_id'], r['skills_id'])]
    return {'schema_version': '1.0', 'catalog_version': index['catalog_version'],
            'id': identifier, 'namespace': item['namespace'],
            'source': {'path': item['source'], 'sha256': source['sha256'], 'revision': revision},
            'content_format': content_format, 'content': content,
            'relations_status': index['relations_status'], 'relations': relations}


def check_links():
    links = read_json(ROOT / 'catalog/playbook-links.json')
    inventory = read_json(ROOT / 'catalog/inventory.json')
    expected = {s['id'] for s in inventory['analyzer']['sources']}
    if {v['source_id'] for v in links['links']} != expected or len(links['links']) != len(expected):
        raise ValueError('Playbook comparison source set mismatch')
    sources = {s['id']: s for s in inventory['analyzer']['sources']}
    for item in links['links']:
        source = sources[item['source_id']]
        if item['pinned_path'] != 'analyzer/sources/' + source['path'] or item['playbook_path'] != source['path']:
            raise ValueError('Invalid playbook comparison paths')
        pinned = digest((ROOT / item['pinned_path']).read_bytes())
        current = digest((ROOT / item['playbook_path']).read_bytes())
        if (pinned != source['sha256'] or item['pinned_sha256'] != pinned or
                item['current_sha256'] != current or item['status'] != ('same' if pinned == current else 'changed')):
            raise ValueError('Playbook comparison is stale: ' + item['source_id'])


def changed_playbooks():
    check_links()
    return [item['playbook_path'] for item in read_json(ROOT / 'catalog/playbook-links.json')['links']
            if item['status'] == 'changed']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true', help='regenerate the index from the current inventory')
    group.add_argument('--check', action='store_true')
    group.add_argument('--get', metavar='ID')
    group.add_argument('--new-release', metavar='VERSION', help='create a new immutable local release')
    group.add_argument('--refresh-playbook-links', action='store_true', help='record current playbook hashes for review')
    group.add_argument('--check-aligned', action='store_true', help='fail if a pinned playbook source differs from the current file')
    args = parser.parse_args()
    if args.refresh_playbook_links:
        path = ROOT / 'catalog/playbook-links.json'
        links = read_json(path)
        for item in links['links']:
            pinned = digest((ROOT / item['pinned_path']).read_bytes())
            current = digest((ROOT / item['playbook_path']).read_bytes())
            item.update(pinned_sha256=pinned, current_sha256=current,
                        status='same' if pinned == current else 'changed')
        path.write_text(json.dumps(links, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        check_links()
        print('Refreshed playbook comparisons; review changed sources')
        return
    if args.new_release:
        version = args.new_release
        if not re.fullmatch(r'[0-9A-Za-z][0-9A-Za-z.-]*', version):
            raise ValueError('Invalid catalogue release version')
        from validate_catalog_inventory import main as validate_inventory
        validate_inventory()
        check_links()
        inventory = read_json(ROOT / 'catalog/inventory.json')
        paths = {'analyzer/catalog/requirements.full.json'} | {r['path'] for r in inventory['skills']['records']}
        sources = {}
        for path in sorted(paths):
            raw = (ROOT / path).read_bytes()
            sources[path] = {'sha256': digest(raw), 'text': raw.decode('utf-8')}
        release = {'schema_version': '1.0', 'catalog_version': version, 'sources': sources,
                   'relations_status': inventory['crosswalk']['status'],
                   'relations': inventory['crosswalk']['relations'], 'inventory': inventory,
                   'playbook_links': read_json(ROOT / 'catalog/playbook-links.json')}
        release_path = ROOT / 'catalog/releases' / (version + '.json')
        encoded = (json.dumps(release, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
        with release_path.open('xb') as file:
            file.write(encoded)
        current = {'schema_version': '1.0', 'catalog_version': version,
                   'release': release_path.relative_to(ROOT).as_posix(), 'sha256': digest(encoded)}
        CURRENT.write_text(json.dumps(current, indent=2) + '\n', encoding='utf-8')
        INDEX.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print('Created local catalogue release ' + version)
        return
    expected = build()
    if args.write:
        verify_release(expected)
        INDEX.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return
    index = read_json(INDEX)
    if index != expected:
        raise ValueError('Shared catalogue index is out of date')
    release = verify_release(index)
    if args.check or args.check_aligned:
        changed = changed_playbooks()
        if changed and args.check_aligned:
            raise ValueError('Pinned playbook sources differ from current files; semantic review required: ' + ', '.join(changed))
        if changed:
            print('Playbook sources requiring semantic review: ' + ', '.join(changed))
        ids = [r['id'] for r in index['records']]
        if len(ids) != len(set(ids)):
            raise ValueError('Duplicate shared catalogue identifier')
        analyzer_ids = [r['id'] for r in json.loads(release['sources']['analyzer/catalog/requirements.full.json']['text'])['requirements']]
        if analyzer_ids != [r['id'] for r in index['records'] if r['namespace'] == 'analyzer']:
            raise ValueError('Analyzer release IDs differ from index')
        for item in index['records']:
            if item['namespace'] == 'secure-development':
                resolve(index, release, item['id'])
        print(f"Shared catalogue verified: {len(index['records'])} requirements")
    else:
        print(json.dumps(resolve(index, release, args.get), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
