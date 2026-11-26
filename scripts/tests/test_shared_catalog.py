"""Focused checks for shared catalogue lookup and source-comparison drift."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('shared_catalog', Path(__file__).resolve().parents[1] / 'shared_catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class SharedCatalogueTests(unittest.TestCase):
    def test_related_records_resolve_from_both_namespaces(self):
        index = catalog.build()
        release = catalog.verify_release(index)
        left = catalog.resolve(index, release, 'SD-SESSION-001.C02')
        right = catalog.resolve(index, release, 'PSH3-APP-EB1E45F4B55A')
        shared = [r for r in left['relations'] if r['analyzer_id'] == right['id']]
        self.assertEqual(len(shared), 1)
        self.assertEqual(shared[0]['relation'], 'related')
        self.assertIn(shared[0], right['relations'])
        self.assertIn('SameSite', left['content'])
        self.assertIn('SameSite', right['content']['statement'])

    def test_lookup_uses_release_content(self):
        index = {'catalog_version': '1', 'relations_status': 'partial', 'relations': [], 'records': [{'id': 'SD-X-001.C01', 'namespace': 'secure-development', 'source': 'topic.md'}]}
        release = {'inventory': {'skills': {'revision': 'abc'}}, 'sources': {'topic.md': {'sha256': 'example', 'text': '### SD-X-001.C01 — title\n\nOriginal condition.\n\n### SD-X-001.C02 — other\nOther.'}}}
        result = catalog.resolve(index, release, 'SD-X-001.C01')
        self.assertIn('Original condition.', result['content'])
        self.assertNotIn('SD-X-001.C02', result['content'])
        with self.assertRaises(ValueError):
            catalog.resolve(index, release, 'missing')

    def test_playbook_comparison_detects_current_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'catalog').mkdir()
            (root / 'analyzer/sources/content').mkdir(parents=True)
            (root / 'content').mkdir()
            (root / 'analyzer/sources/content/a.md').write_text('source')
            (root / 'content/a.md').write_text('current')
            pinned = catalog.digest(b'source')
            current = catalog.digest(b'current')
            inventory = {'analyzer': {'sources': [{'id': 'a', 'path': 'content/a.md', 'sha256': pinned}]}}
            links = {'links': [{'source_id': 'a', 'pinned_path': 'analyzer/sources/content/a.md',
                                'playbook_path': 'content/a.md', 'pinned_sha256': pinned,
                                'current_sha256': current, 'status': 'changed'}]}
            (root / 'catalog/inventory.json').write_text(json.dumps(inventory))
            (root / 'catalog/playbook-links.json').write_text(json.dumps(links))
            with patch.object(catalog, 'ROOT', root):
                catalog.check_links()
                self.assertEqual(catalog.changed_playbooks(), ['content/a.md'])
                (root / 'content/a.md').write_text('changed again')
                with self.assertRaisesRegex(ValueError, 'stale'):
                    catalog.changed_playbooks()


if __name__ == '__main__':
    unittest.main()
