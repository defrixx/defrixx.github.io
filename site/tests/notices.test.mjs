import test from 'node:test';
import assert from 'node:assert/strict';
import { prebundledNames, renderNotices } from '../plugins/third-party-notices.mjs';

test('license publication fails closed when actual library notices are absent', () => {
  assert.throws(() => renderNotices([]), /omits Mermaid/);
  assert.throws(() => renderNotices([{ name: 'mermaid', version: 'test', identifier: 'MIT' }]), /Missing license text/);
});
test('notices preserve original permission text and exact version identifiers', () => {
  const permission = 'Copyright upstream\nPermission is hereby granted\nAll applicable conditions';
  const output = renderNotices([{ name: 'mermaid', version: '12.1.0', identifier: 'MIT', text: permission }]);
  assert.ok(output.includes(permission));
  assert.ok(output.includes('mermaid — 12.1.0'));
  assert.ok(output.includes('MIT'));
});
test('prebundled modules include scoped dependencies and deduplicate source sections', () => {
  assert.deepEqual(prebundledNames('// node_modules/svelte/runtime.js\n// node_modules/@scope/component/a.js\n// node_modules/svelte/other.js\nconst ignored = "node_modules/unrelated";'), ['@scope/component', 'svelte']);
});
