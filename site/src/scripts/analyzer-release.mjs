export const RELEASE_API = 'https://api.github.com/repos/defrixx/SDD-security-analyzer/releases/latest';

export function parseRelease(value) {
  if (!value || value.draft !== false || value.prerelease !== false ||
      typeof value.tag_name !== 'string' || !value.tag_name.trim() ||
      typeof value.published_at !== 'string' || !Number.isFinite(Date.parse(value.published_at))) {
    throw new Error('Invalid published release');
  }
  const url = new URL(value.html_url);
  if (url.origin !== 'https://github.com' || url.username || url.password ||
      !url.pathname.startsWith('/defrixx/SDD-security-analyzer/releases/tag/') ||
      !url.pathname.slice('/defrixx/SDD-security-analyzer/releases/tag/'.length) || url.search || url.hash) {
    throw new Error('Unexpected release URL');
  }
  return {
    tag: value.tag_name.slice(0, 200),
    name: typeof value.name === 'string' && value.name.trim() ? value.name.slice(0, 300) : value.tag_name.slice(0, 200),
    date: value.published_at,
    notes: typeof value.body === 'string' ? value.body.slice(0, 1800) + (value.body.length > 1800 ? '…' : '') : '',
    url: url.href,
  };
}

// Share a request between cards. Never embed credentials or execute release Markdown.
let pending;
export function loadLatestRelease(fetcher = fetch) {
  if (!pending) {
    pending = (async () => {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 8000);
      try {
        const response = await fetcher(RELEASE_API, {
          headers: { Accept: 'application/vnd.github+json' },
          credentials: 'omit', signal: controller.signal,
        });
        if (!response.ok) throw new Error(`GitHub returned ${response.status}`);
        return parseRelease(await response.json());
      } finally { clearTimeout(timeout); }
    })();
    pending.catch(() => { pending = undefined; });
  }
  return pending;
}
