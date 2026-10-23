#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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

    # The published repository is defrixx.github.io. Keep generation identical
    # locally and in CI rather than deriving links from the checkout context.
    return ""


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
    "supply-chain/ci-cd-security/playbook": 30,
    "platform-security/cloud-iam-workload-identity/playbook": 80,
    "reference/security-policy-examples/overview": 20,
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
    "ai-automation/model-security-eval/overview": 90,
    "ai-automation/prompt-guard/overview": 100,
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


def description_from(body: str, lang: str = "en") -> str:
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("#", "-", "|", "```", "---")):
            continue
        if len(line) > 180:
            return line[:177].rstrip() + "..."
        return line
    return "Плейбук безопасности продукта." if lang == "ru" else "Product security playbook."


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
    body = expand_hub_content(body, lang)
    order = PAGE_ORDER.get(logical_key, TOP_LEVEL_ORDER.get(logical_key.split("/", 1)[0], 100))
    description = description_from(body, lang)

    frontmatter = [
        "---",
        f"title: {yaml_quote(title)}",
        f"description: {yaml_quote(description)}",
        "sidebar:",
        f"  order: {order}",
        "---",
        "",
    ]
    if logical_key.startswith("hub/"):
        frontmatter[1:1] = ["template: splash", "tableOfContents: false", "prev: false", "next: false"]
    return "\n".join(frontmatter) + body.rstrip() + "\n"


# Short navigation labels; new documents fall back to their translated H1.
SITE_MAP_LABELS = {
 'supply-chain/ci-cd-security/playbook': ('Безопасность CI/CD', 'CI/CD security'),
 'platform-security/cloud-iam-workload-identity/playbook': ('Cloud IAM и доступ рабочих нагрузок', 'Cloud IAM and workload access'),
 'reference/security-policy-examples/overview': ('Примеры политик безопасности', 'Security policy examples'),
 'review/overview': ('Обзор', 'Overview'),
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
 'ai-security/owasp-llm-top-10/overview': ('OWASP LLM Top 10 (2026)', 'OWASP LLM Top 10 (2026)'),
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
 'ai-automation/prompt-integrity/overview': ('prompt-integrity', 'prompt-integrity'),
 'ai-automation/model-security-eval/overview': ('model-security-eval', 'model-security-eval'),
 'ai-automation/prompt-guard/overview': ('prompt-guard', 'prompt-guard')}

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
        ("Код, API и доступ", "Code, APIs, and access control",
         ("application-security/secure-coding/", "application-security/api/",
          "application-security/business-logic/", "application-security/identity/")),
        ("Веб и браузер", "Web and browser", ("application-security/web/",)),
    ),
    "platform-security": (
        ("Доступ к облаку", "Cloud access", ("platform-security/cloud-iam-workload-identity/",)),
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
        ("Инструменты", "Tools", ("ai-automation/prompt-integrity/", "ai-automation/model-security-eval/", "ai-automation/prompt-guard/")),
    ),
}


LIBRARY_DESCRIPTIONS = {
    "review": ("Границы доверия, сценарии атак и решения по риску. От архитектурного разбора до допуска релиза и работы с уязвимостями.",
               "Trust boundaries, attack scenarios and risk decisions. From architecture review to release acceptance and vulnerability management."),
    "application-security": ("Код и пользовательские потоки: API, OIDC/OAuth, бизнес-логика и защита в браузере. Проверки доступа и обработки недоверенных данных.",
               "Code and user flows: APIs, OIDC/OAuth, business logic and browser security. Verify access and untrusted data handling."),
    "platform-security": ("Облачные права, Kubernetes и управление секретами. Разбор конфигурации, изоляции и поведения платформы при атаке.",
               "Cloud permissions, Kubernetes and secrets management. Assess configuration, isolation and platform behavior under attack."),
    "supply-chain": ("Доверие от коммита до развертывания: исполнители CI/CD, происхождение сборок, контейнерные образы и проверка артефактов.",
               "Trust from commit to deployment: CI/CD executors, build provenance, container images and artifact verification."),
    "ai-security": ("Модели, агенты, MCP и разработка с ИИ. Выбор границ автономности, доступа к инструментам и проверок недоверенного контекста.",
               "Models, agents, MCP and AI-assisted development. Assess autonomy boundaries, tool access and untrusted context."),
    "ai-automation": ("Практическое применение наших пяти скиллов и трех локальных инструментов: входные данные, установка, результаты и совместная работа.",
               "Practical guides to our five skills and three local tools: inputs, setup, outputs and combined workflows."),
    "reference": ("Контекст инфраструктурных технологий и исполняемые примеры политик: сопоставьте инженерное решение с проверяемой конфигурацией.",
               "Infrastructure operating context and executable policy examples: connect engineering decisions to verifiable configuration."),
}


def site_map_content(lang: str) -> str:
    from html import escape

    ix = 0 if lang == "ru" else 1
    documents = {source_info(p)[1]: p for p in source_files()
                 if source_info(p)[0] == lang and source_info(p)[1].split("/", 1)[0] in LIBRARY_DESCRIPTIONS}
    count = len(documents)
    label = "материала" if lang == "ru" else "resources"
    search = "Найти по слову или технологии" if lang == "ru" else "Search a topic or technology"
    nav_label = "Направления библиотеки" if lang == "ru" else "Library domains"
    lines = [f'<div class="library-toolbar"><span class="library-stats">{count} {label} · 7 ' + ("направлений" if lang == "ru" else "domains") + ' · RU / EN</span>',
             f'<button type="button" class="library-search" data-open-library-search>{search}<span aria-hidden="true">⌕</span></button></div>',
             f'<nav class="library-index" aria-label="{nav_label}">']
    for prefix, rt, et, _ in SITE_MAP_SECTIONS:
        lines.append(f'<a href="#library-{prefix}">{escape(rt if ix == 0 else et)}</a>')
    lines += ['</nav>', '<div class="library-directory">']
    for number, (prefix, rt, et, overview) in enumerate(SITE_MAP_SECTIONS, 1):
        keys = sorted((key for key in documents if key.startswith(prefix + "/")), key=lambda k: (PAGE_ORDER.get(k, 100), k))
        lines += [f'<section class="library-section" id="library-{prefix}"><header>',
                  f'<p class="eyebrow">{number:02d}</p><h2>{escape(rt if ix == 0 else et)}</h2>',
                  f'<p class="library-description">{escape(LIBRARY_DESCRIPTIONS[prefix][ix])}</p>',
                  '<p class="library-count">' + ("Материалов: " if ix == 0 else "Resources: ") + str(len(keys)) + '</p>']
        if overview in documents:
            route = escape(source_route(documents[overview]), quote=True)
            lines.append(f'<a class="library-overview" href="{route}">' + ("Обзор направления" if ix == 0 else "Domain overview") + '</a>')
        lines += ['</header>', '<div class="library-links">']
        remaining = [key for key in keys if key != overview]
        groups = list(SITE_MAP_GROUPS.get(prefix, ()))
        groups.append(("Материалы", "Resources", (prefix + "/",)))
        for gr, ge, prefixes in groups:
            selected = [key for key in remaining if key.startswith(prefixes)]
            if not selected:
                continue
            lines += ['<div class="library-group">', f'<h3>{gr if ix == 0 else ge}</h3><ul>']
            for key in selected:
                path = documents[key]
                label = SITE_MAP_LABELS.get(key, (None, None))[ix]
                if label is None:
                    label, _ = extract_title_and_body(path, path.read_text(encoding="utf-8"))
                kind = (("Плейбук", "Playbook") if path.name.startswith("playbook.") else
                        ("Чеклист", "Checklist") if path.name.startswith("checklist.") else
                        ("Справочник", "Reference") if key.startswith("reference/") else ("Руководство", "Guide"))[ix]
                route = escape(source_route(path), quote=True)
                lines.append(f'<li><a class="library-resource" href="{route}"><span class="library-resource-title">{escape(label)}</span><span class="library-resource-kind">{kind}</span></a></li>')
            lines += ['</ul></div>']
            remaining = [key for key in remaining if key not in selected]
        lines += ['</div></section>']
    return "\n".join(lines + ['</div>']) + "\n"


def getting_started_content(lang: str) -> str:
    from html import escape

    ru = lang == "ru"
    lines = ['<ol class="scenario-directory">']
    for entry in load_hub_scenarios():
        route = f'{SITE_BASE}/{lang}/{entry["route"]}/'
        lines += ['<li><article>', f'<h2>{escape(entry["title"][lang])}</h2>',
                  '<dl class="scenario-facts"><div><dt>' + ("Когда применять" if ru else "When to use") + f'</dt><dd>{escape(entry["applies"][lang])}</dd></div>',
                  '<div><dt>' + ("Результат" if ru else "Result") + f'</dt><dd>{escape(entry["result"][lang])}</dd></div></dl>',
                  f'<a href="{route}">' + ("Открыть маршрут" if ru else "Open route") + '</a></article></li>']
    return "\n".join(lines + ['</ol>'])


REGISTRY_PATHS = {
    "secure-development": "skills/secure-development",
    "security-review": "skills/security-review",
    "sensitive-data-cleanup": "skills/sensitive-data-cleanup",
    "security-report-triage": "skills/security-report-triage",
    "security-fix-verification": "skills/security-fix-verification",
    "prompt-integrity": "tools/prompt-integrity",
    "prompt-guard": "tools/prompt-guard",
    "model-security-eval": "tools/model-security-eval",
}
PUBLIC_DOWNLOADS = tuple(f"{name}.{lang}.{extension}" for lang in ("ru", "en")
                         for name, extension in (("review-template", "md"), ("test-matrix", "csv")))


def load_hub_registry(path: Path | None = None) -> dict:
    """Validate a link-only allowlist; never fetch or copy the sibling repository."""
    value = json.loads((path or ROOT / "config/hub-sources.json").read_text(encoding="utf-8"))
    if (set(value) != {"schema_version", "repository", "revision", "imports", "entries"}
            or value["schema_version"] != 1 or value["imports"] is not False
            or value["repository"] != "https://github.com/defrixx/Product-security-skills"
            or not isinstance(value["revision"], str)
            or not re.fullmatch(r"[0-9a-f]{40}", value["revision"])):
        raise ValueError("Invalid pinned hub source registry")
    seen = set()
    for entry in value["entries"]:
        required = {"id", "kind", "path", "guide", "version", "license", "applies", "inputs", "result", "local", "limits"}
        if not isinstance(entry, dict) or set(entry) != required:
            raise ValueError("Invalid hub catalogue entry")
        identifier = entry["id"]
        if identifier not in REGISTRY_PATHS or identifier in seen or entry["path"] != REGISTRY_PATHS[identifier]:
            raise ValueError("Unapproved or duplicate hub source path")
        seen.add(identifier)
        skill = entry["path"].startswith("skills/")
        guide = (f"ai-automation/security-skills/{identifier}/overview" if skill
                 else f"ai-automation/{identifier}/overview")
        if (entry["kind"] != ("skill" if skill else "tool") or entry["license"] != "MIT"
                or entry["guide"] != guide or not isinstance(entry["version"], str)
                or not entry["version"]):
            raise ValueError("Invalid hub source metadata")
        if skill and entry["version"] != "commit:" + value["revision"][:12]:
            raise ValueError("Skill version must match the pinned revision")
        for field in ("applies", "inputs", "result", "local", "limits"):
            localized = entry[field]
            if (not isinstance(localized, dict) or set(localized) != {"ru", "en"}
                    or any(not isinstance(v, str) or not v.strip() for v in localized.values())):
                raise ValueError("Missing localized hub card field")
    if seen != set(REGISTRY_PATHS):
        raise ValueError("Incomplete hub source registry")
    return value


def hub_catalogue_content(lang: str) -> str:
    from html import escape

    registry = load_hub_registry()
    ru = lang == "ru"
    sha, repo = registry["revision"], registry["repository"]
    labels = (("inputs", "Входные данные", "Inputs"), ("local", "Локальное выполнение", "Local execution"),
              ("limits", "Ограничения", "Limits"))
    lines = ['<div class="hub-catalogue">']
    for kind in ("skill", "tool"):
        heading = ("Скиллы для ассистента" if ru else "Skills for your assistant") if kind == "skill" else ("Локальные инструменты" if ru else "Local tools")
        lines += [f'<section class="catalogue-group"><h2>{heading}</h2>']
        for entry in registry["entries"]:
            if entry["kind"] != kind:
                continue
            source = f'{repo}/tree/{sha}/{entry["path"]}'
            license_url = f'{repo}/blob/{sha}/LICENSE'
            lines += ['<article class="catalogue-item">', '<div class="catalogue-summary">',
                      f'<h3><a href="{SITE_BASE}/{lang}/{entry["guide"]}/">{escape(entry["id"])}</a></h3>',
                      f'<p>{escape(entry["applies"][lang])}</p></div>',
                      f'<p class="catalogue-result">{escape(entry["result"][lang])}</p>',
                      '<details class="catalogue-details"><summary>' + ("Входные данные, запуск и версия" if ru else "Inputs, execution and version") + '</summary><dl>']
            for field, rt, et in labels:
                lines += [f'<dt>{rt if ru else et}</dt><dd>{escape(entry[field][lang])}</dd>']
            version_label = "Версия / источник" if ru else "Version / source"
            source_label = "Руководство этой ревизии" if ru else "Guide at this revision"
            license_label = "Лицензия" if ru else "License"
            lines += [f'<dt>{version_label}</dt><dd>{escape(entry["version"])} · <code>{sha[:12]}</code><br /><a href="{source}">{source_label}</a></dd>',
                      f'<dt>{license_label}</dt><dd><a href="{license_url}">MIT</a></dd></dl></details></article>']
        lines.append('</section>')
    return "\n".join(lines + ['</div>'])


def hub_downloads_content(lang: str) -> str:
    labels = (("review-template", "md", "Шаблон отчета (Markdown)", "Review template (Markdown)"),
              ("test-matrix", "csv", "Матрица проверок (CSV)", "Test matrix (CSV)"))
    lines = ['<ul class="hub-downloads">']
    for name, extension, rt, et in labels:
        route = f"{SITE_BASE}/downloads/api-integration/{name}.{lang}.{extension}"
        lines.append(f'<li><a href="{route}" download>{rt if lang == "ru" else et}</a></li>')
    return "\n".join(lines + ['</ul>'])


def hub_navigation_content(lang: str) -> str:
    links = (("tasks", "Сценарии", "Scenarios"), ("knowledge", "База знаний", "Knowledge base"),
             ("catalogue", "Навыки и инструменты", "Skills and tools"),
             ("reviews/delivery-api", "Примеры ревью", "Review examples"), ("usage", "Как использовать", "How to use"))
    label = "Разделы хаба" if lang == "ru" else "Hub sections"
    lines = [f'<nav class="hub-navigation" aria-label="{label}">']
    for key, rt, et in links:
        lines.append(f'<a href="{SITE_BASE}/{lang}/hub/{key}/overview/">{rt if lang == "ru" else et}</a>')
    return "\n".join(lines + ['</nav>'])



def load_hub_scenarios(path: Path | None = None) -> list[dict]:
    """Publish only ready routes whose localized source documents already exist."""
    value = json.loads((path or ROOT / "config/hub-scenarios.json").read_text(encoding="utf-8"))
    if not isinstance(value, dict) or set(value) != {"schema_version", "scenarios"} or value["schema_version"] != 1:
        raise ValueError("Invalid scenario registry")
    entries = value["scenarios"]
    if not isinstance(entries, list) or not entries:
        raise ValueError("Scenario registry needs an existing ready route")
    identifiers, routes = set(), set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"id", "status", "route", "title", "applies", "result"}:
            raise ValueError("Invalid scenario entry")
        identifier, route = entry["id"], entry["route"]
        if (not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9-]+", identifier)
                or not isinstance(route, str) or not re.fullmatch(r"hub/[a-z0-9/-]+/overview", route)
                or identifier in identifiers or route in routes or entry["status"] != "ready"):
            raise ValueError("Duplicate, unready or invalid scenario route")
        identifiers.add(identifier); routes.add(route)
        for field in ("title", "applies", "result"):
            localized = entry[field]
            if (not isinstance(localized, dict) or set(localized) != {"ru", "en"}
                    or any(not isinstance(v, str) or not v.strip() for v in localized.values())):
                raise ValueError("Scenario fields need RU and EN text")
        for language in ("ru", "en"):
            source = ROOT / "content" / (route + f".{language}.md")
            if not source.is_file() or source.resolve() != ROOT.resolve() / "content" / (route + f".{language}.md"):
                raise ValueError("Scenario route is missing localized source material")
    return entries


RELEASE_DOWNLOADS = tuple(f"{name}.{lang}.{ext}" for lang in ("ru", "en") for name, ext in (("release-template", "md"), ("release-checks", "csv")))

def hub_scenarios_content(lang: str) -> str:
    from html import escape
    ru = lang == "ru"
    entries = load_hub_scenarios()
    label = "Учебные маршруты" if ru else "Learning routes"
    previous = "Предыдущий маршрут" if ru else "Previous route"
    following = "Следующий маршрут" if ru else "Next route"
    lines = [f'<div class="route-explorer" data-lang="{lang}" role="region" aria-label="{label}">',
             '<div class="route-stage">',
             f'<button type="button" class="route-arrow route-previous" data-route-action="previous" aria-label="{previous}" hidden><span aria-hidden="true">←</span></button>',
             '<div class="route-panels">',
             f'<span class="route-counter" role="img" aria-live="off" aria-label="' + (f'Сценарий 1 из {len(entries)}' if ru else f'Scenario 1 of {len(entries)}') + f'">1 / {len(entries)}</span>']
    for i, entry in enumerate(entries):
        route = f'{SITE_BASE}/{lang}/{entry["route"]}/'
        lines += [f'<article class="route-panel" id="route-panel-{i}" data-title="{escape(entry["title"][lang], quote=True)}">',
                  f'<h3>{escape(entry["title"][lang])}</h3><dl class="scenario-facts">',
                  '<div><dt>' + ("Когда применять" if ru else "When to use") + f'</dt><dd>{escape(entry["applies"][lang])}</dd></div>',
                  '<div><dt>' + ("Результат" if ru else "Result") + f'</dt><dd>{escape(entry["result"][lang])}</dd></div></dl>',
                  f'<a class="landing-cta scenario-action" href="{escape(route, quote=True)}">' + ("Открыть маршрут" if ru else "Open route") + ' <span aria-hidden="true">↗</span></a></article>']
    lines.append(f'</div><button type="button" class="route-arrow route-next" data-route-action="next" aria-label="{following}" hidden><span aria-hidden="true">→</span></button></div><div class="route-controls" hidden>')
    for action, label in [('play', 'Отключить автосмену' if ru else 'Disable automatic switching')]:
        lines.append(f'<button type="button" data-route-action="{action}">{label}</button>')
    lines.append('</div></div>')
    return "\n".join(lines)


SCENARIO_DOWNLOAD_DIRS = ("llm-rag", "agent-tools", "kafka-integration")


def scenario_downloads_content(lang: str, scenario: str) -> str:
    if scenario not in SCENARIO_DOWNLOAD_DIRS:
        raise ValueError("Unknown public scenario download directory")
    labels = (("review-template", "md", "Шаблон ревью" if lang == "ru" else "Review template"),
              ("test-matrix", "csv", "Матрица проверок" if lang == "ru" else "Test matrix"))
    return '<ul class="hub-downloads">' + ''.join(f'<li><a download href="{SITE_BASE}/downloads/{scenario}/{name}.{lang}.{ext}">{label}</a></li>' for name, ext, label in labels) + '</ul>'


def release_downloads_content(lang: str) -> str:
    labels = [("release-template", "md", "Шаблон решения" if lang == "ru" else "Decision template"),
              ("release-checks", "csv", "Матрица проверок" if lang == "ru" else "Test matrix")]
    return '<ul class="hub-downloads">' + ''.join(f'<li><a download href="{SITE_BASE}/downloads/ci-cd-release/{name}.{lang}.{ext}">{label}</a></li>' for name, ext, label in labels) + '</ul>'


def review_breadcrumb_content(lang: str) -> str:
    ru = lang == "ru"
    route = f"{SITE_BASE}/{lang}/hub/api-integration/overview/"
    label = "Навигационная цепочка" if ru else "Breadcrumb"
    title = "Внешняя API-интеграция" if ru else "External API integration"
    current = "Пример ревью" if ru else "Review example"
    return (f'<nav class="review-breadcrumb" aria-label="{label}"><ol><li><a href="{route}">{title}</a></li>'
            f'<li aria-current="page"><span aria-hidden="true">/</span> {current}</li></ol></nav>')


def expand_hub_content(body: str, lang: str) -> str:
    # Expand only known authored markers. No arbitrary paths or external imports.
    fragments = {"navigation": hub_navigation_content, "tasks": getting_started_content,
                 "library": site_map_content, "catalogue": hub_catalogue_content,
                 "downloads": hub_downloads_content, "scenarios": hub_scenarios_content,
                 "review-breadcrumb": review_breadcrumb_content, "release-downloads": release_downloads_content,
                 **{name + "-downloads": (lambda language, directory=name: scenario_downloads_content(language, directory))
                    for name in SCENARIO_DOWNLOAD_DIRS}}
    for name, function in fragments.items():
        marker = f"<!-- hub:{name} -->"
        if marker in body:
            body = body.replace(marker, function(lang))
    if SITE_BASE:
        for language in ("ru", "en"):
            body = body.replace(f'href="/{language}/', f'href="{SITE_BASE}/{language}/')
    return body


def index_content(lang: str) -> str:
    source = ROOT / "content" / "hub" / f"overview.{lang}.md"
    title, body = extract_title_and_body(source, source.read_text(encoding="utf-8"))
    body = expand_hub_content(rewrite_markdown_links(source, body), lang)
    description = "От инженерной задачи к проверяемому решению по безопасности." if lang == "ru" else "From engineering tasks to evidence-based security decisions."
    return (f"---\ntitle: {yaml_quote(title)}\ndescription: {yaml_quote(description)}\n"
            "template: splash\ntableOfContents: false\nprev: false\nnext: false\nsidebar:\n  order: 0\n---\n\n" + body.rstrip() + "\n")


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
    load_hub_registry()
    files = source_files()
    errors = validate_pairs(files)
    if errors:
        raise ValueError("\n".join(errors))

    rendered: dict[Path, str] = {}
    for source in files:
        rendered[target_path(source)] = generated_content(source)

    rendered[DOCS_ROOT / "ru" / "index.md"] = index_content("ru")
    rendered[DOCS_ROOT / "en" / "index.md"] = index_content("en")
    for name in PUBLIC_DOWNLOADS:
        source = ROOT / "downloads" / "api-integration" / name
        expected = ROOT.resolve() / "downloads" / "api-integration" / name
        if source.resolve() != expected or not source.is_file():
            raise ValueError(f"Invalid public template source: {name}")
        rendered[ROOT / "site/public/downloads/api-integration" / name] = source.read_text(encoding="utf-8")
    for name in RELEASE_DOWNLOADS:
        source = ROOT / "downloads/ci-cd-release" / name
        if source.resolve() != ROOT.resolve() / "downloads/ci-cd-release" / name or not source.is_file():
            raise ValueError(f"Invalid public template source: {name}")
        rendered[ROOT / "site/public/downloads/ci-cd-release" / name] = source.read_text(encoding="utf-8")
    for directory in SCENARIO_DOWNLOAD_DIRS:
        for name in PUBLIC_DOWNLOADS:
            source = ROOT / "downloads" / directory / name
            if source.resolve() != ROOT.resolve() / "downloads" / directory / name or not source.is_file():
                raise ValueError(f"Invalid public template source: {directory}/{name}")
            rendered[ROOT / "site/public/downloads" / directory / name] = source.read_text(encoding="utf-8")
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

    print(f"Generated {len(rendered) - (len(PUBLIC_DOWNLOADS) * (1 + len(SCENARIO_DOWNLOAD_DIRS)) + len(RELEASE_DOWNLOADS))} Starlight documents and {(len(PUBLIC_DOWNLOADS) * (1 + len(SCENARIO_DOWNLOAD_DIRS)) + len(RELEASE_DOWNLOADS))} public downloads.")
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
