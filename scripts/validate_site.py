#!/usr/bin/env python3
"""Check local links and fragments in the generated static site."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from sync_starlight_content import ROOT, configured_site_base


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=ROOT / "site" / "dist")
    parser.add_argument("--base", default=configured_site_base())
    args = parser.parse_args()
    root = args.dist.resolve()
    base = args.base.rstrip("/")
    pages = {
        path.resolve(): Page(path.read_text(encoding="utf-8"))
        for path in root.rglob("*.html")
    }
    if not pages:
        print(f"No HTML pages found in {root}; build the site first.")
        return 1

    errors: list[str] = []
    checked = 0
    for path, page in sorted(pages.items()):
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target_path = unquote(url.path)
            location = f"{path.relative_to(root)}: {link}"
            if not target_path:
                target = path
            elif target_path.startswith("/"):
                if base and not target_path.startswith(base + "/"):
                    errors.append(f"{location}: outside configured base {base}")
                    continue
                target = root / target_path[len(base):].lstrip("/")
            else:
                target = path.parent / target_path
            target = target.resolve()
            if not target.is_relative_to(root):
                errors.append(f"{location}: outside generated site")
                continue
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                errors.append(f"{location}: missing destination")
                continue
            if url.fragment and target in pages:
                if unquote(url.fragment) not in pages[target].ids:
                    errors.append(f"{location}: missing fragment")
            checked += 1
    for error in errors:
        print(error)
    print(f"Checked {len(pages)} pages and {checked} local links; {len(errors)} errors.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
