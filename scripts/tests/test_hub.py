"""Exercise the public link registry boundary and portable local draft outputs."""
import copy
import csv
import importlib.util
import io
from html.parser import HTMLParser
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('hub_sync', Path(__file__).resolve().parents[1] / 'sync_starlight_content.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class HubTests(unittest.TestCase):
    def test_registry_rejects_remote_fetches_floating_revisions_and_unapproved_paths(self):
        original = sync.load_hub_registry()
        mutations = [
            lambda v: v.update(imports=True),
            lambda v: v.update(revision='main'),
            lambda v: v.update(repository='https://example.invalid/untrusted'),
            lambda v: v['entries'][0].update(path='artifacts/private'),
            lambda v: v['entries'][0].update(path='../../reports/private'),
            lambda v: v['entries'][0].update(license='CC-BY-4.0'),
            lambda v: v['entries'][0].update(version='commit:other'),
            lambda v: v['entries'][0]['inputs'].pop('ru'),
            lambda v: v['entries'].append(copy.deepcopy(v['entries'][0])),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'registry.json'
            for mutate in mutations:
                value = copy.deepcopy(original)
                mutate(value)
                path.write_text(json.dumps(value))
                with self.subTest(value=value), self.assertRaises(ValueError):
                    sync.load_hub_registry(path)

    def test_cards_link_to_pinned_sources_and_license_at_same_revision(self):
        registry = sync.load_hub_registry()
        for lang in ('ru', 'en'):
            html = sync.hub_catalogue_content(lang)
            self.assertNotIn('/main/', html)
            for entry in registry['entries']:
                self.assertIn(f'/tree/{registry["revision"]}/{entry["path"]}', html)
                self.assertIn(f'/blob/{registry["revision"]}/LICENSE', html)
                guide = sync.ROOT / 'site/src/content/docs' / lang / (entry['guide'] + '.md')
                self.assertTrue(guide.is_file(), guide)

    def test_explicit_preview_base_applies_to_hub_links_and_downloads(self):
        with patch.object(sync, 'SITE_BASE', '/preview'):
            for lang in ('ru', 'en'):
                body = sync.index_content(lang)
                self.assertIn(f'/preview/{lang}/hub/api-integration/overview/', body)
                self.assertNotIn('href="/' + lang + '/', body)
                self.assertIn('/preview/downloads/api-integration/', sync.hub_downloads_content(lang))
                self.assertIn(f'/preview/{lang}/ai-automation/', sync.hub_catalogue_content(lang))

    def test_only_explicit_authored_templates_are_rendered_to_public_directory(self):
        rendered = sync.render_all()
        public = {path: value for path, value in rendered.items() if path.is_relative_to(sync.ROOT / 'site/public')}
        self.assertEqual(len(public), len(sync.PUBLIC_DOWNLOADS) * (1 + len(sync.SCENARIO_DOWNLOAD_DIRS)) + len(sync.RELEASE_DOWNLOADS))
        self.assertEqual({path.name for path in public}, set(sync.PUBLIC_DOWNLOADS + sync.RELEASE_DOWNLOADS))
        expected = {Path(directory) / name for directory in ('api-integration', *sync.SCENARIO_DOWNLOAD_DIRS) for name in sync.PUBLIC_DOWNLOADS}
        expected.update(Path('ci-cd-release') / name for name in sync.RELEASE_DOWNLOADS)
        self.assertEqual({path.relative_to(sync.ROOT / 'site/public/downloads') for path in public}, expected)
        for path, value in public.items():
            self.assertEqual(value, (sync.ROOT / 'downloads' / path.parent.name / path.name).read_text())
            self.assertIn('Defrixx', value)
            if path.suffix == '.csv':
                rows = list(csv.DictReader(io.StringIO(value)))
                self.assertGreaterEqual(len(rows), 10)
                self.assertTrue(all(r['status'] == 'not-run' and not r['observed'] for r in rows))
            else:
                self.assertIn('creativecommons.org/licenses/by/4.0/', value)

    def test_symlink_cannot_turn_a_public_template_into_a_private_import(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'downloads/api-integration'
            source.mkdir(parents=True)
            private = root / 'private.md'
            private.write_text('not public')
            (source / sync.PUBLIC_DOWNLOADS[0]).symlink_to(private)
            with patch.object(sync, 'ROOT', root), patch.object(sync, 'source_files', return_value=[]), patch.object(sync, 'load_hub_registry', return_value={}), patch.object(sync, 'index_content', return_value='home'):
                with self.assertRaisesRegex(ValueError, 'Invalid public template'):
                    sync.render_all()

    def test_symlinked_template_directory_cannot_import_other_local_material(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            elsewhere = root / 'reports'
            elsewhere.mkdir()
            (elsewhere / sync.PUBLIC_DOWNLOADS[0]).write_text('not public')
            (root / 'downloads').mkdir()
            (root / 'downloads/api-integration').symlink_to(elsewhere, target_is_directory=True)
            with patch.object(sync, 'ROOT', root), patch.object(sync, 'source_files', return_value=[]), patch.object(sync, 'load_hub_registry', return_value={}), patch.object(sync, 'index_content', return_value='home'):
                with self.assertRaisesRegex(ValueError, 'Invalid public template'):
                    sync.render_all()


    def test_library_directory_preserves_every_existing_localized_resource_once(self):
        class Links(HTMLParser):
            def __init__(self, text):
                super().__init__(); self.hrefs = []; self.feed(text)
            def handle_starttag(self, tag, attrs):
                attributes = dict(attrs)
                if tag == 'a' and attributes.get('href', '').startswith('/'):
                    self.hrefs.append(attributes['href'])
        for language in ('ru', 'en'):
            expected = {sync.source_route(path) for path in sync.source_files()
                        if sync.source_info(path)[0] == language
                        and sync.source_info(path)[1].split('/', 1)[0] in sync.LIBRARY_DESCRIPTIONS}
            actual = Links(sync.site_map_content(language)).hrefs
            self.assertEqual(set(actual), expected)
            self.assertEqual(len(actual), len(expected))
            with patch.object(sync, 'SITE_BASE', '/preview'):
                preview = Links(sync.site_map_content(language)).hrefs
            self.assertEqual(set(preview), {'/preview' + route for route in expected})


    def test_scenario_registry_rejects_unready_missing_and_incomplete_routes(self):
        original = {'schema_version': 1, 'scenarios': sync.load_hub_scenarios()}
        mutations = [
            lambda v: v['scenarios'][0].update(status='candidate'),
            lambda v: v['scenarios'][0].update(route='hub/not-written/overview'),
            lambda v: v['scenarios'][0].update(route='https://example.invalid/route'),
            lambda v: v['scenarios'][0]['title'].pop('en'),
            lambda v: v['scenarios'].append(copy.deepcopy(v['scenarios'][0])),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'scenarios.json'
            for mutate in mutations:
                value = copy.deepcopy(original); mutate(value)
                path.write_text(json.dumps(value))
                with self.subTest(value=value), self.assertRaises(ValueError):
                    sync.load_hub_scenarios(path)

    def test_scenario_links_use_existing_localized_targets_and_preview_base(self):
        class Links(HTMLParser):
            def __init__(self, text):
                super().__init__(); self.hrefs = []; self.feed(text)
            def handle_starttag(self, tag, attrs):
                attributes = dict(attrs)
                if tag == 'a': self.hrefs.append(attributes['href'])
        entries = sync.load_hub_scenarios()
        for language in ('ru', 'en'):
            expected = {f'/{language}/{entry["route"]}/' for entry in entries}
            self.assertEqual(set(Links(sync.hub_scenarios_content(language)).hrefs), expected)
            with patch.object(sync, 'SITE_BASE', '/preview'):
                actual = Links(sync.hub_scenarios_content(language)).hrefs
            self.assertEqual(set(actual), {'/preview' + route for route in expected})


    def test_route_downloads_preserve_ids_and_recheck_traceability(self):
        import re
        for directory, basename, requirement_source, prefix in (
            ('api-integration', 'test-matrix', 'content/hub/reviews/delivery-api/overview', 'API'),
            ('ci-cd-release', 'release-checks', 'content/hub/ci-cd-release/overview', 'REL'),
        ):
            localized = []
            for lang in ('ru', 'en'):
                source = (sync.ROOT / (requirement_source + '.' + lang + '.md')).read_text()
                requirements = set(re.findall(r'^\| (' + prefix + r'-\d{3}) \|', source, re.M))
                path = sync.ROOT / 'downloads' / directory / (basename + '.' + lang + '.csv')
                rows = list(csv.DictReader(io.StringIO(path.read_text())))
                by_id = {row['test_id']: row for row in rows}
                self.assertEqual(len(by_id), len(rows))
                self.assertEqual({row['requirement_id'] for row in rows}, requirements)
                self.assertTrue(all(row['status'] == row['retest_status'] == 'not-run' for row in rows))
                self.assertTrue(all(not row['observed'] and not row['retest_observed'] and not row['repair_revision'] for row in rows))
                self.assertTrue(all(row['template_version'] == '0.2' for row in rows))
                review_name = 'delivery-api' if prefix == 'API' else 'ci-cd-release'
                review = (sync.ROOT / f'content/hub/reviews/{review_name}/overview.{lang}.md').read_text()
                for referenced in re.findall(r'\b(?:REL-T-\d{2}|T-\d{3})\b', review):
                    self.assertIn(referenced, by_id)
                for row in rows:
                    if row['finding_ids']:
                        self.assertIn(row['finding_ids'], review)
                localized.append({key: (row['requirement_id'], row['finding_ids']) for key, row in by_id.items()})
            self.assertEqual(*localized)

    def test_tasks_list_every_available_route_from_the_registry(self):
        for lang in ('ru', 'en'):
            rendered = sync.getting_started_content(lang)
            for entry in sync.load_hub_scenarios():
                self.assertIn('/' + lang + '/' + entry['route'] + '/', rendered)
            self.assertEqual(rendered.count('<li><article>'), len(sync.load_hub_scenarios()))
            self.assertNotIn('route not assembled', rendered)
            self.assertNotIn('маршрут еще не собран', rendered)


    def test_added_registry_route_reaches_both_index_and_home_counter(self):
        import copy
        entries = copy.deepcopy(sync.load_hub_scenarios())
        added = copy.deepcopy(entries[0])
        added.update(id='test-next-route', route='hub/test-next-route/overview')
        added['title'] = {'ru': 'Тестовый маршрут', 'en': 'Test route'}
        entries.append(added)
        with patch.object(sync, 'load_hub_scenarios', return_value=entries):
            for lang in ('ru', 'en'):
                directory = sync.getting_started_content(lang)
                home = sync.hub_scenarios_content(lang)
                self.assertEqual(directory.count('<li><article>'), len(entries))
                self.assertIn('/' + lang + '/hub/test-next-route/overview/', directory)
                self.assertEqual(home.count('class="route-panel"'), len(entries))
                self.assertIn('1 / ' + str(len(entries)), home)


    def test_new_scenario_requirements_downloads_and_findings_are_bilingual(self):
        import re
        for directory, prefix in [('llm-rag', 'RAG'), ('agent-tools', 'AGT'), ('kafka-integration', 'KAF'), ('vulnerability-response', 'VUL'), ('secret-exposure-response', 'SEC')]:
            pairs = []
            for lang in ('ru', 'en'):
                route = (sync.ROOT / f'content/hub/{directory}/overview.{lang}.md').read_text()
                review = (sync.ROOT / f'content/hub/reviews/{directory}/overview.{lang}.md').read_text()
                template = (sync.ROOT / f'downloads/{directory}/review-template.{lang}.md').read_text()
                reqs = set(re.findall(r'^\| (' + prefix + r'-\d{3}) \|', route, re.M))
                rows = list(csv.DictReader(io.StringIO((sync.ROOT / f'downloads/{directory}/test-matrix.{lang}.csv').read_text())))
                self.assertEqual(len(reqs), 10)
                self.assertEqual(len(rows), 20)
                self.assertEqual({row['requirement_id'] for row in rows}, reqs)
                ids = {row['test_id'] for row in rows}
                self.assertEqual(len(ids), len(rows))
                for rid in reqs:
                    self.assertEqual(sum(row['requirement_id'] == rid for row in rows), 2)
                    self.assertIn(rid, template)
                for referenced in re.findall(prefix + r'-T-\d{2}', review):
                    self.assertIn(referenced, ids)
                for row in rows:
                    self.assertEqual(row['status'], 'not-run')
                    self.assertEqual(row['retest_status'], 'not-run')
                    self.assertFalse(row['observed'] or row['retest_observed'] or row['repair_revision'])
                    for finding in row['finding_ids'].split(';'):
                        if finding:
                            self.assertIn(finding, review)
                pairs.append({row['test_id']: (row['requirement_id'], row['finding_ids']) for row in rows})
            self.assertEqual(*pairs)


    def test_new_download_allowlist_rejects_symlinked_private_material(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, files in [('api-integration', sync.PUBLIC_DOWNLOADS), ('ci-cd-release', sync.RELEASE_DOWNLOADS), *[(item, sync.PUBLIC_DOWNLOADS) for item in sync.SCENARIO_DOWNLOAD_DIRS]]:
                folder = root / 'downloads' / name
                folder.mkdir(parents=True)
                for filename in files:
                    (folder / filename).write_text('public template fixture')
            private = root / 'private-report.md'
            private.write_text('synthetic private fixture')
            target = root / 'downloads' / sync.SCENARIO_DOWNLOAD_DIRS[0] / sync.PUBLIC_DOWNLOADS[0]
            target.unlink()
            target.symlink_to(private)
            with patch.object(sync, 'ROOT', root), patch.object(sync, 'source_files', return_value=[]), patch.object(sync, 'load_hub_registry', return_value={}), patch.object(sync, 'index_content', return_value='home'):
                with self.assertRaisesRegex(ValueError, 'Invalid public template'):
                    sync.render_all()


if __name__ == '__main__':
    unittest.main()
