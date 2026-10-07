"""Failure-path tests for the policy runner; no Docker needed."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    'security_policy_runner', Path(__file__).resolve().parents[1] / 'test_security_policies.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class PolicyRunnerTests(unittest.TestCase):
    def test_only_explicit_true_allows(self):
        for value in (True, False, 1, 0, 'true', None, [], {}):
            with self.subTest(value=value):
                report = {'result': [{'expressions': [{'value': value}]}]}
                if value is True:
                    runner.validate_eval_report(report)
                else:
                    with self.assertRaises(SystemExit):
                        runner.validate_eval_report(report)

    def test_undefined_ambiguous_and_malformed_reports_fail(self):
        reports = [None, [], {}, {'errors': []}, {'result': []},
                   {'result': [None]}, {'result': [{}, {}]},
                   {'result': [{'expressions': []}]},
                   {'result': [{'expressions': [{'value': True}, {'value': True}]}]}]
        for report in reports:
            with self.subTest(report=report), self.assertRaises((ValueError, SystemExit)):
                runner.validate_eval_report(report)

    def test_complete_test_report_passes(self):
        runner.validate_test_report(self.report(), {'allowed', 'denied'})

    @staticmethod
    def report():
        return [{'package': 'data.examples.tests', 'name': 'test_fixture_cases',
                 'sub_results': {'allowed': {'name': 'allowed'}, 'denied': {'name': 'denied'}}}]

    def test_missing_extra_failed_skipped_and_wrong_tests_fail(self):
        for mutation in ('missing', 'extra', 'fail', 'skip', 'error', 'wrong-name', 'wrong-package', 'wrong-subname'):
            report = self.report()
            result = report[0]
            sub = result['sub_results']
            if mutation == 'missing':
                del sub['denied']
            elif mutation == 'extra':
                sub['other'] = {'name': 'other'}
            elif mutation in ('fail', 'skip', 'error'):
                sub['denied'][mutation] = True
            elif mutation == 'wrong-name':
                result['name'] = 'different_test'
            elif mutation == 'wrong-package':
                result['package'] = 'different.package'
            else:
                sub['denied']['name'] = 'allowed'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                runner.validate_test_report(report, {'allowed', 'denied'})
        for flag in ('fail', 'skip', 'error'):
            report = self.report()
            report[0][flag] = True
            with self.subTest(flag=flag), self.assertRaises(ValueError):
                runner.validate_test_report(report, {'allowed', 'denied'})

    def test_invalid_json_and_nonstandard_numbers_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.json'
            for text in ('{', '{"key":1,"key":2}', '{"value":NaN}', '{"value":Infinity}'):
                path.write_text(text)
                with self.subTest(text=text), self.assertRaises(ValueError):
                    runner.load_json(path)
            path.write_text('{"ok":true}')
            self.assertEqual(runner.load_json(path), {'ok': True})

    def test_timeout_removes_only_its_container(self):
        with patch.object(runner.subprocess, 'run') as run:
            run.side_effect = [subprocess.TimeoutExpired('docker', 1), subprocess.CompletedProcess([], 0)]
            with self.assertRaises(subprocess.TimeoutExpired):
                runner.run_opa(['run', '--server'], timeout=1)
            first = run.call_args_list[0].args[0]
            name = first[first.index('--name') + 1]
            self.assertTrue(name.startswith('security-policy-'))
            self.assertEqual(run.call_args_list[1].args[0], ['docker', 'rm', '--force', name])

    def test_interruption_removes_its_container(self):
        with patch.object(runner.subprocess, 'run') as run:
            run.side_effect = [KeyboardInterrupt(), subprocess.CompletedProcess([], 0)]
            with self.assertRaises(KeyboardInterrupt):
                runner.run_opa(['run', '--server'])
            self.assertEqual(run.call_args_list[1].args[0][:3], ['docker', 'rm', '--force'])

    def test_engine_error_is_propagated(self):
        with patch.object(runner.subprocess, 'run', side_effect=subprocess.CalledProcessError(2, 'docker')):
            with self.assertRaises(subprocess.CalledProcessError):
                runner.run_opa(['eval', 'invalid'])


if __name__ == '__main__':
    unittest.main()
