import test from 'node:test';
import assert from 'node:assert/strict';
import { parseRelease, loadLatestRelease, RELEASE_API } from '../src/scripts/analyzer-release.mjs';
const sample = { draft: false, prerelease: false, tag_name: 'v0.2.0', name: 'UI improvements', published_at: '2026-11-09T19:18:00Z', body: '<script>alert(1)</script>', html_url: 'https://github.com/defrixx/SDD-security-analyzer/releases/tag/v0.2.0' };
test('valid release retains text without interpreting Markdown or HTML', () => {
  assert.equal(parseRelease(sample).notes, sample.body);
  assert.equal(parseRelease({...sample, name: null, body: null}).name, 'v0.2.0');
  assert.equal(parseRelease({...sample, body: 'x'.repeat(1900)}).notes.length, 1801);
});
test('rejects drafts, prereleases, missing fields and unexpected destinations', () => {
  for (const patch of [{draft:true}, {prerelease:true}, {tag_name:''}, {published_at:'bad'}, {html_url:'javascript:alert(1)'}, {html_url:'https://evil.example/releases/tag/v1'}, {html_url:'https://github.com/other/repo/releases/tag/v1'}]) {
    assert.throws(() => parseRelease({...sample, ...patch}));
  }
  assert.throws(() => parseRelease(null));
});
test('HTTP, JSON and network failures reject; successful requests use latest without credentials and are shared', async () => {
  for (const status of [403, 404, 429, 500]) await assert.rejects(loadLatestRelease(async () => ({ok:false,status})));
  await assert.rejects(loadLatestRelease(async () => { throw new Error('offline'); }));
  await assert.rejects(loadLatestRelease(async () => ({ok:true,json:async()=>{throw new Error('invalid JSON');}})));
  let calls = 0;
  const fetcher = async (url, options) => {
    calls++;
    assert.equal(url, RELEASE_API); assert.equal(options.credentials, 'omit'); assert.equal(options.headers.Authorization, undefined);
    return {ok:true,json:async()=>sample};
  };
  const [a,b] = await Promise.all([loadLatestRelease(fetcher), loadLatestRelease(fetcher)]);
  assert.equal(calls, 1); assert.equal(a.tag, 'v0.2.0'); assert.deepEqual(a,b);
});
