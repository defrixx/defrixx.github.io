#!/usr/bin/env python3
"""Run the policy examples with pinned OPA; errors and missing cases fail CI."""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / 'examples' / 'security-policies'
# OPA 1.21.1 static image; update the digest through a reviewed change.
OPA_IMAGE = 'openpolicyagent/opa@sha256:4675ab04ad1627f74741d2d9c5142698c79e18b7b09f192587d31d6dba20838e'


def docker_command() -> list[str]:
    return [
        'docker', 'run', '--rm', '--network', 'none', '--read-only',
        '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
        '-v', f'{EXAMPLES}:/policies:ro',
    ]


def run_opa(arguments: list[str], *, input_directory: str | None = None,
            timeout: float = 120) -> subprocess.CompletedProcess:
    name = f'security-policy-{uuid4().hex}'
    command = docker_command() + ['--name', name]
    if input_directory is not None:
        command += ['-v', f'{input_directory}:/input:ro']
    command += [OPA_IMAGE] + arguments
    try:
        return subprocess.run(command, check=True, capture_output=True,
                              text=True, timeout=timeout)
    except (subprocess.TimeoutExpired, KeyboardInterrupt):
        # Killing the Docker client does not guarantee container termination.
        # Remove only this invocation's uniquely named container.
        subprocess.run(['docker', 'rm', '--force', name], check=False,
                       capture_output=True, text=True, timeout=10)
        raise


def reject_constant(value):
    raise ValueError(f'Non-JSON numeric constant: {value}')


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'),
                      object_pairs_hook=unique_object, parse_constant=reject_constant)


def validate_eval_report(report) -> None:
    if not isinstance(report, dict) or 'errors' in report:
        raise ValueError('Invalid OPA evaluation report')
    results = report.get('result')
    if not isinstance(results, list) or len(results) != 1:
        raise SystemExit('DENY: missing or ambiguous policy decision')
    expressions = results[0].get('expressions') if isinstance(results[0], dict) else None
    if (not isinstance(expressions, list) or len(expressions) != 1
            or not isinstance(expressions[0], dict)
            or expressions[0].get('value') is not True):
        raise SystemExit('DENY: configuration did not satisfy the selected policy')


def validate_test_report(report, names: set[str]) -> None:
    if not isinstance(report, list) or len(report) != 1 or not isinstance(report[0], dict):
        raise ValueError('Unexpected OPA test report')
    result = report[0]
    if (result.get('package') != 'data.examples.tests'
            or result.get('name') != 'test_fixture_cases'
            or any(result.get(flag) for flag in ('fail', 'error', 'skip'))):
        raise ValueError('Unexpected, failed, or skipped OPA test')
    subresults = result.get('sub_results')
    if not isinstance(subresults, dict) or set(subresults) != names:
        raise ValueError('OPA did not execute the complete fixture set')
    for name, value in subresults.items():
        if (not isinstance(value, dict) or value.get('name') != name
                or any(value.get(flag) for flag in ('fail', 'error', 'skip'))):
            raise ValueError('Invalid, failed, or skipped policy scenario')


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f'Duplicate JSON key: {key}')
        value[key] = item
    return value


def check_input(policy: str, path: Path) -> None:
    value = load_json(path)
    # Serialized copy prevents changes to the original path during evaluation.
    with tempfile.TemporaryDirectory(prefix='security-policy-') as directory:
        copied = Path(directory) / 'input.json'
        copied.write_text(json.dumps(value), encoding='utf-8')
        result = run_opa([
            'eval', '--strict-builtin-errors', '--format=json',
            '-d', f'/policies/policies/{policy}.rego',
            '-d', '/policies/configuration.json', '-i', '/input/input.json',
            f'data.examples.{policy}.allow',
        ], input_directory=directory)
    report = json.loads(result.stdout)
    validate_eval_report(report)
    print(f'ALLOW: {path} satisfies {policy} (static configuration only)')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--policy', choices=['pod', 'aws_trust', 'slsa_build'])
    parser.add_argument('--input', type=Path)
    args = parser.parse_args()
    if bool(args.policy) != bool(args.input):
        parser.error('--policy and --input must be supplied together')
    if args.input:
        check_input(args.policy, args.input)
        return
    cases = load_json(EXAMPLES / 'fixtures.json')['fixtures']['cases']
    if not isinstance(cases, list) or not cases:
        raise ValueError('No policy scenarios found')
    names = set()
    for case in cases:
        if not isinstance(case, dict) or set(case) != {'name', 'policy', 'allowed', 'input'}:
            raise ValueError('Unexpected fixture schema')
        if not isinstance(case['name'], str) or not case['name'] or case['name'] in names:
            raise ValueError('Missing or duplicate scenario name')
        names.add(case['name'])
        if case['policy'] not in {'pod', 'aws_trust', 'slsa_build'} or type(case['allowed']) is not bool:
            raise ValueError('Unknown policy or non-boolean expected decision')
    for policy, manifest in [('pod', 'pod.json'), ('aws_trust', 'aws-trust.json'), ('slsa_build', 'slsa-build.json')]:
        selected = [case for case in cases if case['policy'] == policy]
        if {case['allowed'] for case in selected} != {True, False}:
            raise ValueError(f'{policy}: allow and deny cases are required')
        value = load_json(EXAMPLES / 'manifests' / manifest)
        if not any(case['allowed'] and case['input'] == value for case in selected):
            raise ValueError(f'{manifest}: example not covered by an allowed scenario')
    run_opa(['check', '--strict', '/policies'])
    result = run_opa(['test', '/policies', '--fail-on-empty', '--format=json'])
    validate_test_report(json.loads(result.stdout), names)
    print(f'PASS: {len(cases)} scenarios across 3 policies; OPA strict checks passed')


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.stderr.strip() or f'OPA failed with exit status {error.returncode}')
