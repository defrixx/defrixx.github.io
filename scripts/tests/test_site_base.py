"""Ensure a repository rename cannot change checked-in generated links in CI."""
import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    'starlight_sync', Path(__file__).resolve().parents[1] / 'sync_starlight_content.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class SiteBaseTests(unittest.TestCase):
    def test_generated_content_is_identical_locally_and_in_ci(self):
        expected = None
        for repository in ('', 'defrixx/Product-security-playbook', 'defrixx/defrixx.github.io'):
            with self.subTest(repository=repository), patch.dict(os.environ, {'GITHUB_REPOSITORY': repository}, clear=True):
                base = sync.configured_site_base()
                self.assertEqual(base, '')
                with patch.object(sync, 'SITE_BASE', base):
                    rendered = sync.render_all()
                if expected is None:
                    expected = rendered
                else:
                    self.assertEqual(rendered, expected)

    def test_explicit_base_override_is_preserved(self):
        for value, expected in [('', ''), ('/preview/', '/preview'), ('/preview', '/preview')]:
            with self.subTest(value=value), patch.dict(os.environ, {'PUBLIC_SITE_BASE': value}, clear=True):
                self.assertEqual(sync.configured_site_base(), expected)


if __name__ == '__main__':
    unittest.main()
