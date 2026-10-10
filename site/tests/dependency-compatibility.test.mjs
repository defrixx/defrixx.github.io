import assert from 'node:assert/strict';
import { test } from 'node:test';
import postcss from 'postcss';
import nested from 'postcss-nested';
import katex from 'katex';
import CachePolicy from 'http-cache-semantics';

test('the updated nesting plugin preserves code-block selectors and media queries', async () => {
  const source = '.code { color: red; & .token, &:focus { color: blue; } @media (min-width: 40rem) { & .token { color: green; } } }';
  const result = await postcss([nested()]).process(source, { from: undefined });
  const selectors = [];
  result.root.walkRules(rule => selectors.push(rule.selector));
  assert.deepEqual(selectors, ['.code', '.code .token, .code:focus', '.code .token']);
  const media = [];
  result.root.walkAtRules('media', rule => media.push(rule.params));
  assert.deepEqual(media, ['(min-width: 40rem)']);
  assert.equal(result.warnings().length, 0);
});

test('KaTeX retains the MathML rendering interface used by Mermaid', () => {
  const output = katex.renderToString(String.raw`\frac{a^2}{b} + \sqrt{c}`, {
    displayMode: true, output: 'mathml', trust: false, throwOnError: true,
  });
  assert.match(output, /<math\b/);
  assert.match(output, /<mfrac>/);
  assert.match(output, /<msqrt>/);
});

test('untrusted formulas cannot introduce a link through the KaTeX trust interface', () => {
  const output = katex.renderToString(String.raw`\href{https://example.invalid}{x}`, {
    output: 'mathml', trust: false, strict: 'ignore', throwOnError: false,
  });
  assert.doesNotMatch(output, /<a\b|href="https:/);
});

test('the updated HTTP cache retains static caching and rejects private shared responses', () => {
  const request = { url: 'https://example.invalid/static', method: 'GET', headers: {} };
  const publicResponse = { status: 200, headers: { 'cache-control': 'public, max-age=60' } };
  const policy = new CachePolicy(request, publicResponse, { shared: true });
  assert.equal(policy.storable(), true);
  assert.equal(policy.satisfiesWithoutRevalidation(request), true);
  assert.equal(new CachePolicy(request, {
    status: 200, headers: { 'cache-control': 'private, max-age=60' },
  }, { shared: true }).storable(), false);
});
