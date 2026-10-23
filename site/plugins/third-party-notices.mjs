import { readFile, readdir, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const siteRoot = fileURLToPath(new URL('../', import.meta.url));
const modules = path.join(siteRoot, 'node_modules');
const uiName = '@pagefind/default-ui';
const prebundled = new Set(['svelte', 'bcp-47', 'is-alphabetical', 'is-alphanumerical', 'is-decimal']);
const licenseName = /^(licen[cs]e|copying|notice|copyright)(?:$|[.-])/i;

async function manifest(name) {
  return JSON.parse(await readFile(path.join(modules, name, 'package.json'), 'utf8'));
}
async function licenseTexts(name) {
  const root = path.join(modules, name);
  const texts = [];
  for (const file of await readdir(root, { withFileTypes: true })) {
    if (!licenseName.test(file.name)) continue;
    const target = path.join(root, file.name);
    if (file.isFile()) texts.push(await readFile(target, 'utf8'));
    else if (file.isDirectory()) {
      for (const child of await readdir(target, { withFileTypes: true })) {
        if (child.isFile()) texts.push(await readFile(path.join(target, child.name), 'utf8'));
      }
    }
  }
  return texts.join('\n\n').trim();
}
export function prebundledNames(source) {
  return [...new Set([...source.matchAll(/^\/\/ node_modules\/((?:@[^/]+\/)?[^/]+)\//gm)].map(match => match[1]))].sort();
}
export function renderNotices(entries) {
  if (!entries.some(entry => entry.name === 'mermaid')) throw new Error('Client license inventory omits Mermaid');
  const sections = entries.map(entry => {
    if (!entry.name || !entry.version || !entry.text?.trim()) throw new Error(`Missing license text: ${entry.name ?? 'unknown'}`);
    return `## ${entry.name} — ${entry.version}\nLicense: ${entry.identifier ?? 'see original notice'}\n${entry.provenance ? `Source: ${entry.provenance}\n` : ''}\n${entry.text.trim()}\n`;
  });
  return '# Third-party notices\n\nOriginal copyright and permission notices for the distributed browser code and copied search runtime.\nPackage versions below refer to the actual client bundle unless explicitly marked as an upstream prebundle.\nNo font files are shipped; the site uses system fonts.\n\n' + sections.join('\n');
}
export default function thirdPartyNotices() {
  return {
    name: 'security-hub-third-party-notices',
    hooks: {
      'astro:build:done': async ({ dir }) => {
        const output = fileURLToPath(dir);
        const entries = JSON.parse(await readFile(path.join(output, 'third-party-licenses.json'), 'utf8'));
        const pagefind = await manifest('pagefind');
        const pagefindLicense = await licenseTexts('pagefind');
        for (const entry of entries) {
          const original = await licenseTexts(entry.name);
          if (original) entry.text = original;
          if (entry.name === uiName && !entry.text) entry.text = pagefindLicense;
        }
        entries.push({ name: 'pagefind copied search runtime', version: pagefind.version, identifier: pagefind.license,
          provenance: 'pagefind npm distribution LICENSE directory', text: pagefindLicense });
        const ui = await manifest(uiName);
        const uiSource = await readFile(path.join(modules, uiName, 'npm_dist/mjs/ui-core.mjs'), 'utf8');
        const fingerprint = createHash('sha256').update(uiSource).digest('hex');
        for (const name of prebundledNames(uiSource)) {
          if (!prebundled.has(name)) throw new Error(`Review new prebundled runtime notice: ${name}`);
          const text = name === 'svelte'
            ? await readFile(path.join(siteRoot, 'licenses/svelte-runtime-LICENSE.md'), 'utf8')
            : await licenseTexts(name);
          entries.push({ name, version: `upstream prebundle in ${uiName}@${ui.version}`, identifier: 'MIT',
            provenance: `UI artifact SHA-256 ${fingerprint}; exact embedded patch release is not declared by upstream. License reference: ${name === 'svelte' ? 'official Svelte 4.2.20 LICENSE.md' : `${name}@${(await manifest(name)).version} installed original license`}`, text });
        }
        const fonts = (await readdir(output, { recursive: true })).filter(file => /\.(?:woff2?|ttf|otf)$/i.test(file));
        if (fonts.length) throw new Error('Review newly distributed font licenses before publication');
        await writeFile(path.join(output, 'third-party-notices.txt'), renderNotices(entries));
        // Keep the public machine inventory consistent with the readable notices.
        await writeFile(path.join(output, 'third-party-licenses.json'), JSON.stringify(entries, null, 2) + '\n');
      },
    },
  };
}
