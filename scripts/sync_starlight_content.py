#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOTS = (ROOT / "content", ROOT / "reference")
DOCS_ROOT = ROOT / "site" / "src" / "content" / "docs"
def configured_site_base() -> str:
    explicit = os.environ.get("PUBLIC_SITE_BASE")
    if explicit is not None:
        return explicit.rstrip("/")

    repository = os.environ.get("GITHUB_REPOSITORY", "")
    if repository.endswith("/defrixx.github.io"):
        return ""

    return "/Product-security-playbook"


SITE_BASE = configured_site_base()

LANG_RE = re.compile(r"^(?P<stem>.+)\.(?P<lang>ru|en)\.md$")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")

TOP_LEVEL_ORDER = {
    "review": 10,
    "application-security": 20,
    "platform-security": 30,
    "supply-chain": 40,
    "ai-security": 50,
    "ai-automation": 55,
    "reference": 60,
}

PAGE_ORDER = {
    "supply-chain/overview": 5,
    "platform-security/overview": 5,
    "application-security/overview": 5,
    "review/overview": 5,
    "review/architecture/checklist": 10,
    "review/threat-modeling/playbook": 20,
    "review/release-governance/playbook": 30,
    "review/vulnerability-management/playbook": 40,
    "application-security/web/owasp-top-10/playbook": 10,
    "application-security/web/browser-security/playbook": 20,
    "application-security/api/api-security-patterns/playbook": 30,
    "application-security/business-logic/business-logic-abuse/playbook": 40,
    "application-security/secure-coding/code-review/playbook": 50,
    "application-security/identity/oidc-oauth/playbook": 60,
    "platform-security/kubernetes/cluster-security-review/playbook": 10,
    "platform-security/kubernetes/adversarial-validation/playbook": 20,
    "platform-security/kubernetes/pod-security/playbook": 30,
    "platform-security/kubernetes/secrets/playbook": 40,
    "platform-security/kubernetes/seccomp/checklist": 50,
    "platform-security/kubernetes/container-escape-capability-abuse/overview": 60,
    "platform-security/secrets/vault/playbook": 70,
    "supply-chain/slsa-provenance/overview": 10,
    "supply-chain/container-image-security/playbook": 20,
    "ai-automation/security-skills/overview": 10,
    "ai-automation/security-skills/secure-development/overview": 20,
    "ai-automation/security-skills/security-review/overview": 30,
    "ai-automation/security-skills/sensitive-data-cleanup/overview": 40,
    "ai-automation/security-skills/security-report-triage/overview": 50,
    "ai-automation/security-skills/security-fix-verification/overview": 60,
    "ai-automation/security-skills/workflow/overview": 70,
    "ai-automation/prompt-integrity/overview": 80,
    "ai-security/overview": 5,
    "ai-security/securing-ai/overview": 10,
    "ai-security/owasp-llm-top-10/overview": 20,
    "ai-security/agentic-ai/playbook": 30,
    "ai-security/mcp-security/playbook": 40,
    "reference/infrastructure-technologies/infrastructure-technologies": 10,
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def source_files() -> list[Path]:
    files: list[Path] = []
    for source_root in SOURCE_ROOTS:
        if source_root.exists():
            files.extend(sorted(source_root.rglob("*.md")))
    return files


def source_info(path: Path) -> tuple[str, str, Path]:
    match = LANG_RE.match(path.name)
    if not match:
        raise ValueError(f"{rel(path)} does not use .ru.md or .en.md suffix")

    lang = match.group("lang")
    stem = match.group("stem")

    if path.is_relative_to(ROOT / "content"):
        relative = path.relative_to(ROOT / "content")
        logical = relative.with_name(stem)
    elif path.is_relative_to(ROOT / "reference"):
        relative = path.relative_to(ROOT / "reference")
        logical = Path("reference") / relative.with_name(stem)
    else:
        raise ValueError(f"{rel(path)} is outside supported source roots")

    logical_no_suffix = logical.with_suffix("")
    return lang, logical_no_suffix.as_posix(), logical


def source_route(path: Path, anchor: str = "") -> str:
    lang, logical_key, _ = source_info(path)
    route = f"{SITE_BASE}/{lang}/{logical_key}/" if SITE_BASE else f"/{lang}/{logical_key}/"
    if anchor:
        route += f"#{anchor}"
    return route


def target_path(path: Path) -> Path:
    lang, logical_key, _ = source_info(path)
    return DOCS_ROOT / lang / f"{logical_key}.md"


def peer_path(path: Path) -> Path:
    if path.name.endswith(".ru.md"):
        return path.with_name(path.name.replace(".ru.md", ".en.md"))
    if path.name.endswith(".en.md"):
        return path.with_name(path.name.replace(".en.md", ".ru.md"))
    raise ValueError(f"{rel(path)} does not use a supported language suffix")


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def extract_title_and_body(path: Path, text: str) -> tuple[str, str]:
    match = H1_RE.search(text)
    if not match:
        raise ValueError(f"{rel(path)} has no H1 title")

    title = match.group(1).strip()
    body = text[: match.start()] + text[match.end() :]
    body = body.lstrip("\n")
    return title, body


def description_from(body: str) -> str:
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("#", "-", "|", "```", "---")):
            continue
        if len(line) > 180:
            return line[:177].rstrip() + "..."
        return line
    return "Product security playbook."


def rewrite_markdown_links(source: Path, body: str) -> str:
    def replace(match: re.Match[str]) -> str:
        label = match.group(1)
        raw_target = match.group(2).strip()

        if not raw_target or raw_target.startswith("#"):
            return match.group(0)
        if re.match(r"^[a-z][a-z0-9+.-]*:", raw_target):
            return match.group(0)

        path_part, separator, anchor = raw_target.partition("#")
        if not path_part.endswith((".ru.md", ".en.md")):
            return match.group(0)

        target = (source.parent / unquote(path_part)).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            return match.group(0)

        if not target.exists() or not LANG_RE.match(target.name):
            return match.group(0)

        route = source_route(target, anchor if separator else "")
        return f"[{label}]({route})"

    return MARKDOWN_LINK_RE.sub(replace, body)


def generated_content(source: Path) -> str:
    text = source.read_text(encoding="utf-8")
    title, body = extract_title_and_body(source, text)
    body = rewrite_markdown_links(source, body)
    lang, logical_key, _ = source_info(source)
    order = PAGE_ORDER.get(logical_key, TOP_LEVEL_ORDER.get(logical_key.split("/", 1)[0], 100))
    description = description_from(body)

    frontmatter = [
        "---",
        f"title: {yaml_quote(title)}",
        f"description: {yaml_quote(description)}",
        "sidebar:",
        f"  order: {order}",
        "---",
        "",
    ]
    return "\n".join(frontmatter) + body.rstrip() + "\n"


# Short navigation labels; new documents fall back to their translated H1.
SITE_MAP_LABELS = {'review/overview': ('Обзор', 'Overview'),
 'review/architecture/checklist': ('Архитектурное ревью', 'Architecture review'),
 'review/threat-modeling/playbook': ('Моделирование угроз', 'Threat modeling'),
 'review/release-governance/playbook': ('Управление выпуском', 'Release governance'),
 'review/vulnerability-management/playbook': ('Управление уязвимостями', 'Vulnerability management'),
 'application-security/overview': ('Обзор', 'Overview'),
 'application-security/secure-coding/code-review/playbook': ('Ревью кода', 'Code review'),
 'application-security/api/api-security-patterns/playbook': ('Безопасность API', 'API security'),
 'application-security/business-logic/business-logic-abuse/playbook': ('Бизнес-логика', 'Business logic'),
 'application-security/identity/oidc-oauth/playbook': ('OIDC и OAuth', 'OIDC and OAuth'),
 'application-security/web/browser-security/playbook': ('Защита в браузере', 'Browser security'),
 'application-security/web/owasp-top-10/playbook': ('OWASP Top 10', 'OWASP Top 10'),
 'platform-security/overview': ('Обзор', 'Overview'),
 'platform-security/kubernetes/cluster-security-review/playbook': ('Ревью кластера', 'Cluster review'),
 'platform-security/kubernetes/pod-security/playbook': ('Безопасность Pod', 'Pod security'),
 'platform-security/kubernetes/secrets/playbook': ('Секреты Kubernetes', 'Kubernetes secrets'),
 'platform-security/kubernetes/seccomp/checklist': ('Проверка seccomp', 'Seccomp checklist'),
 'platform-security/kubernetes/container-escape-capability-abuse/overview': ('Выход из контейнера и '
                                                                             'capabilities',
                                                                             'Container escape and '
                                                                             'capabilities'),
 'platform-security/kubernetes/adversarial-validation/playbook': ('Проверка защиты от атак',
                                                                  'Adversarial validation'),
 'platform-security/secrets/vault/playbook': ('Секреты в Vault', 'Secrets in Vault'),
 'supply-chain/overview': ('Обзор', 'Overview'),
 'supply-chain/slsa-provenance/overview': ('SLSA и происхождение сборок', 'SLSA and build provenance'),
 'supply-chain/container-image-security/playbook': ('Контейнерные образы', 'Container images'),
 'ai-security/overview': ('Обзор', 'Overview'),
 'ai-security/securing-ai/overview': ('Защита функций ИИ', 'Securing AI features'),
 'ai-security/owasp-llm-top-10/overview': ('OWASP LLM Top 10', 'OWASP LLM Top 10'),
 'ai-security/agentic-ai/playbook': ('Безопасность агентов', 'Agent security'),
 'ai-security/ai-assisted-development/playbook': ('Разработка с ИИ', 'AI-assisted development'),
 'ai-security/mcp-security/playbook': ('Безопасность MCP', 'MCP security'),
 'reference/infrastructure-technologies/infrastructure-technologies': ('Инфраструктурные технологии',
                                                                       'Infrastructure technologies'),
 'ai-automation/security-skills/secure-development/overview': ('Безопасная разработка', 'Secure development'),
 'ai-automation/security-skills/security-review/overview': ('Ревью безопасности', 'Security review'),
 'ai-automation/security-skills/sensitive-data-cleanup/overview': ('Очистка чувствительных данных',
                                                                   'Sensitive data cleanup'),
 'ai-automation/security-skills/security-report-triage/overview': ('Разбор отчетов безопасности',
                                                                   'Security report triage'),
 'ai-automation/security-skills/security-fix-verification/overview': ('Проверка исправлений',
                                                                      'Fix verification'),
 'ai-automation/security-skills/workflow/overview': ('Совместная работа скиллов', 'Combined skill workflow'),
 'ai-automation/prompt-integrity/overview': ('prompt-integrity', 'prompt-integrity')}

SITE_MAP_SECTIONS = (
    ("review", "Ревью и управление", "Review and Governance", "review/overview"),
    ("application-security", "Безопасность приложений", "Application Security", "application-security/overview"),
    ("platform-security", "Безопасность платформы", "Platform Security", "platform-security/overview"),
    ("supply-chain", "Цепочка поставки", "Supply Chain", "supply-chain/overview"),
    ("ai-security", "Безопасность ИИ", "AI Security", "ai-security/overview"),
    ("ai-automation", "Скиллы и инструменты", "Skills and Tools", "ai-automation/security-skills/overview"),
    ("reference", "Справочник", "Reference", None),
)


# First matching path prefix wins; unmatched pages remain visible below the groups.
SITE_MAP_GROUPS = {
    "application-security": (
        ("Код, API и доступ", "Code and application interfaces",
         ("application-security/secure-coding/", "application-security/api/",
          "application-security/business-logic/", "application-security/identity/")),
        ("Веб и браузер", "Web and browser", ("application-security/web/",)),
    ),
    "platform-security": (
        ("Kubernetes", "Kubernetes", ("platform-security/kubernetes/",)),
        ("Управление секретами", "Secrets management", ("platform-security/secrets/",)),
    ),
    "ai-security": (
        ("Защита ИИ и типовые угрозы", "AI features and threats",
         ("ai-security/securing-ai/", "ai-security/owasp-llm-top-10/")),
        ("Агенты и интеграции", "Agents and integrations",
         ("ai-security/agentic-ai/", "ai-security/mcp-security/")),
        ("Разработка с ИИ", "AI-assisted development", ("ai-security/ai-assisted-development/",)),
    ),
    "ai-automation": (
        ("Скиллы", "Skills",
         tuple("ai-automation/security-skills/" + name + "/" for name in (
             "secure-development", "security-review", "security-report-triage",
             "security-fix-verification", "sensitive-data-cleanup"))),
        ("Совместная работа скиллов", "Combined workflow", ("ai-automation/security-skills/workflow/",)),
        ("Инструменты", "Tools", ("ai-automation/prompt-integrity/",)),
    ),
}


def site_map_content(lang: str) -> str:
    from html import escape

    language_index = 0 if lang == "ru" else 1
    title = "Карта сайта" if lang == "ru" else "Site map"
    documents = {}
    for path in source_files():
        source_lang, key, _ = source_info(path)
        if source_lang == lang:
            documents[key] = path
    lines = [f"\n## {title}\n", '<div class="site-map-grid">']
    for prefix, ru_label, en_label, overview in SITE_MAP_SECTIONS:
        label = ru_label if lang == "ru" else en_label
        heading = escape(label)
        if overview in documents:
            heading = f'<a href="{escape(source_route(documents[overview]), quote=True)}">{heading}</a>'
        lines.extend(['<section class="site-map-card">', f'<h3>{heading}</h3>'])
        keys = sorted(
            (key for key in documents if key.startswith(prefix + "/") and key != overview),
            key=lambda key: (PAGE_ORDER.get(key, 100), key),
        )
        def append_links(group_keys: list[str]) -> None:
            lines.append('<ul>')
            for key in group_keys:
                path = documents[key]
                label = SITE_MAP_LABELS.get(key, (None, None))[language_index]
                if label is None:
                    label, _ = extract_title_and_body(path, path.read_text(encoding="utf-8"))
                route = escape(source_route(path), quote=True)
                lines.append(f'<li><a href="{route}">{escape(label)}</a></li>')
            lines.append('</ul>')

        remaining = keys[:]
        groups = SITE_MAP_GROUPS.get(prefix, ())
        for group_ru, group_en, path_prefixes in groups:
            group_keys = [key for key in remaining if key.startswith(path_prefixes)]
            if not group_keys:
                continue
            group_label = group_ru if lang == "ru" else group_en
            lines.append('<div class="site-map-group">')
            lines.append(f'<h4>{escape(group_label)}</h4>')
            append_links(group_keys)
            lines.append('</div>')
            remaining = [key for key in remaining if key not in group_keys]
        if remaining:
            if groups:
                label = "Другие материалы" if lang == "ru" else "Other material"
                lines.append(f'<h4>{label}</h4>')
            append_links(remaining)
        lines.append('</section>')
    lines.append('</div>')
    return "\n".join(lines) + "\n"


def index_content(lang: str) -> str:
    base = SITE_BASE
    if lang == "ru":
        return """---
title: "Product Security Playbook"
description: "Практическая база знаний по безопасности приложений, платформы, цепочки поставки и ИИ."
sidebar:
  order: 0
---

Практическая база знаний для проверки архитектуры, кода, платформы и инженерных процессов.

Этот проект представляет собой курируемую и постоянно обновляемую базу знаний по безопасности продуктов с акцентом на практическую инженерную работу.

Материалы объединяют отраслевые стандарты, открытые исследования, подходы к обеспечению безопасности и инженерный опыт в плейбуки, чеклисты и методики ревью, которые можно применять повторно.

Цель проекта состоит в том, чтобы переводить положения стандартов в рабочие процессы: архитектурное ревью, моделирование угроз, безопасную разработку, защиту платформ, оценку цепочки поставки ПО и проверку ИИ-систем.

Материалы уточняются по мере развития технологий, техник атак и инженерных практик. Подробные ссылки и указания на источники приводятся там, где это необходимо.

""".format(base=base).rstrip() + "\n" + site_map_content(lang)

    return """---
title: "Product Security Playbook"
description: "A practical knowledge base for AppSec, platform security, supply chain, and AI security."
sidebar:
  order: 0
---

A practical knowledge base for reviewing architecture, code, platforms, and engineering workflows.

This project is a curated and continuously maintained Product Security knowledge base focused on practical security engineering.

The content combines industry standards, public research, security frameworks, and hands-on engineering practices into reusable playbooks, checklists, and review approaches.

Its goal is not to reproduce existing standards, but to translate them into practical workflows that can be applied during architecture reviews, threat modeling, secure development, platform security, software supply chain assessments, and AI security reviews.

Materials are continuously refined as technologies, attack techniques, and engineering practices evolve.

Detailed references and source attribution are provided where applicable.

""".format(base=base).rstrip() + "\n" + site_map_content(lang)


def validate_pairs(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        if not LANG_RE.match(path.name):
            errors.append(f"{rel(path)} does not use .ru.md or .en.md suffix")
            continue
        peer = peer_path(path)
        if not peer.exists():
            errors.append(f"{rel(path)} is missing language pair {rel(peer)}")
    return errors


def render_all() -> dict[Path, str]:
    files = source_files()
    errors = validate_pairs(files)
    if errors:
        raise ValueError("\n".join(errors))

    rendered: dict[Path, str] = {}
    for source in files:
        rendered[target_path(source)] = generated_content(source)

    rendered[DOCS_ROOT / "ru" / "index.md"] = index_content("ru")
    rendered[DOCS_ROOT / "en" / "index.md"] = index_content("en")
    return rendered


def write_all(rendered: dict[Path, str], check: bool) -> int:
    if check:
        errors: list[str] = []
        for path, expected in sorted(rendered.items()):
            if not path.exists():
                errors.append(f"{rel(path)} is missing")
                continue
            actual = path.read_text(encoding="utf-8")
            if actual != expected:
                errors.append(f"{rel(path)} is not up to date")
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("Starlight generated content is up to date.")
        return 0

    DOCS_ROOT.mkdir(parents=True, exist_ok=True)

    for path, content in sorted(rendered.items()):
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")

    # Keep existing directories and unchanged files in place. Recreating the
    # entire tree causes unnecessary filesystem watcher and sync activity.
    for path in DOCS_ROOT.rglob("*.md"):
        if path not in rendered:
            path.unlink()
    for directory, _, _ in os.walk(DOCS_ROOT, topdown=False):
        path = Path(directory)
        if path != DOCS_ROOT and not any(path.iterdir()):
            path.rmdir()

    print(f"Generated {len(rendered)} Starlight document(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="check generated content without writing")
    args = parser.parse_args()

    try:
        rendered = render_all()
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    return write_all(rendered, args.check)


if __name__ == "__main__":
    raise SystemExit(main())
