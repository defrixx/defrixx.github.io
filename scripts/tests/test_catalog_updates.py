"""Regression checks for the targeted built-in catalogue update."""
import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':'), allow_nan=False).encode()).hexdigest()


class CatalogUpdateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'analyzer/catalog/requirements.full.json').read_text())
        cls.records = {r['record_key']: r for r in cls.data['requirements']}

    def test_revision_sources_and_review_hashes(self):
        for key in ('oidc-cookie-policy', 'oidc-exchange-residual-access',
                    'release.dependencies', 'cicd-21'):
            r = self.records[key]
            self.assertEqual(r['version'], '1.2.0')
            raw = (ROOT / 'analyzer' / r['origin']['source_snapshot']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), r['origin']['file_sha256'])
            lines = raw.decode().splitlines()
            for ref in r['source_refs']:
                self.assertEqual('\n'.join(lines[ref['line_start']-1:ref['line_end']]), ref['quote'])
            semantic = {k: v for k, v in r.items() if k not in {'review', 'normativity_review', 'dependencies'}}
            self.assertEqual(r['review']['content_sha256'], digest(semantic))
            self.assertEqual(r['normativity_review']['annotation_sha256'], digest(r['clause_normativity']))

    def test_bff_recommendation_is_conditional_and_not_mandatory(self):
        r = self.records['oidc-cookie-policy']
        self.assertEqual(r['clause_normativity']['bff-profile']['force'], 'recommended')
        self.assertIn({'when': {'predicate': 'p-bff'}, 'then': {'clause': 'bff-profile'},
                       'else': 'not_applicable_branch'}, r['clause_logic']['all'])

    def test_reusable_workflows_require_separate_pin_even_with_lock(self):
        for key in ('release.dependencies', 'cicd-21'):
            r = self.records[key]
            self.assertIn({'when': {'predicate': 'p-reusable'}, 'then': {'clause': 'reusable-sha'},
                           'else': 'not_applicable_branch'}, r['clause_logic']['all'])
            self.assertEqual(r['clause_normativity']['reusable-sha']['force'], 'required')
        branch = self.records['release.dependencies']['clause_logic']['all'][2]['when']['all']
        self.assertIn({'predicate': 'p-actions'}, branch)

    def test_token_expiry_is_assessed_when_exchange_applies(self):
        r = self.records['oidc-exchange-residual-access']
        self.assertIn({'clause': 'token-expiry'}, r['clause_logic']['all'])
        self.assertEqual(r['clause_normativity']['token-expiry']['force'], 'required')
        for plan in ('specification', 'source_level'):
            self.assertTrue(any('token-expiry' in step['clause_ids']
                                for step in r['verification'][plan]['steps']))


if __name__ == '__main__':
    unittest.main()
