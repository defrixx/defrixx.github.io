# Плейбук безопасности браузера и frontend-части

## 1. Область и цель

Этот плейбук задает базу для рабочих сред для ревью приложений, работающих в браузере: CSP, CORS, cookies, browser storage, third-party scripts, embedded content и мер контроля frontend supply chain.

Используйте документ для:
- SPA, server-rendered web applications, BFF-backed browser flows, административных панелей и встраиваемых виджетов;
- релизного ревью security headers, browser session handling и third-party frontend dependencies;
- abuse-case testing для сценариев, где XSS, cross-origin exposure, утечка сессии или компрометация third-party script могут затронуть пользователей.

Вне области:
- дизайн OAuth/OIDC flows: используйте [плейбук OIDC + OAuth 2.0](../../identity/oidc-oauth/playbook.ru.md);
- API authorization и webhook controls: используйте [плейбук API security](../../api/api-security-patterns/playbook.ru.md);
- общее покрытие OWASP Top 10: используйте [плейбук защиты web application](../owasp-top-10/playbook.ru.md).

Цель:
- снизить риск кражи учетных записей и сессий, browser-side data exposure, межсайтовых утечек данных, clickjacking и компрометации third-party scripts;
- сделать browser controls проверяемыми перед релизом, а не воспринимать headers как формальное усиление только для сканеров.

---

## 2. Модель угроз

Активы:
- browser session cookies, CSRF tokens, OAuth/OIDC transient parameters, user profile data, admin UI actions, checkout/payment state и tenant-scoped data, отрисованные в DOM.

Атакующие и точки входа:
- внешний атакующий, внедряющий script через stored/reflected/DOM XSS;
- вредоносный или скомпрометированный third-party script/CDN/tag manager;
- hostile origin, пытающийся читать credentialed cross-origin responses;
- атакующий, встраивающий sensitive pages во frames;
- скомпрометированное расширение браузера или local malware; в таких случаях browser controls только снижают, но не устраняют риск.

High-impact сценарии:
- XSS крадет non-HttpOnly tokens из `localStorage`, вызывает privileged APIs через сессию жертвы или меняет checkout/admin actions.
- CORS отражает произвольные origins и разрешает credentialed reads из browser session жертвы.
- Скомпрометированный analytics или tag-manager script читает sensitive DOM content, session-adjacent data или payment fields.
- Clickjacking встраивает admin или approval screen и вынуждает пользователя выполнить destructive action.
- Third-party CDN script меняется после релиза и выполняет неожиданный код, потому что нет integrity или ownership control.

---

## 3. Базовый профиль

### 3.1 Content Security Policy

Рабочие настройки:
- Browser-facing applications должны задавать CSP через response header `Content-Security-Policy`, а не только через `<meta>` tag.
- Для новых приложений начинайте с `default-src 'none'` и явно разрешайте нужные классы: `script-src`, `style-src`, `img-src`, `font-src`, `connect-src`, `frame-ancestors`, `base-uri` и `form-action`.
- Используйте `frame-ancestors 'none'` по умолчанию для admin, account, checkout и internal tools. Явные origins допустимы только если embedding нужен по product requirement.
- Устанавливайте `base-uri 'none'`, если приложение намеренно не использует `<base>`.
- Устанавливайте `form-action 'self'` плюс явные payment/IdP endpoints, когда они нужны.
- Избегайте `unsafe-inline` и `unsafe-eval` для нового кода. Если legacy code требует их, фиксируйте owner, affected routes, expiry и компенсирующие меры.
- Используйте nonce- или hash-based script execution для приложений, где все еще нужны inline bootstrap scripts.
- Существенные изменения CSP сначала внедряйте через `Content-Security-Policy-Report-Only`, затем включайте enforcement после разбора false positives.

Верификация:
- Проверьте effective header на всех browser entry points, включая error pages, login/callback pages, admin pages и static shell routes.
- Пройдите representative user journey с включенным CSP reporting и разберите нарушения до enforcement.
- Негативный тест: injected inline script и unapproved external script не должны выполняться в enforced profile.

### 3.2 CORS и cross-origin data exposure

Рабочие настройки:
- Не включайте CORS глобально. Настраивайте его per route или для конкретной API surface, где browser cross-origin access действительно нужен.
- Credentialed CORS должен использовать exact origin allowlists. Нельзя совмещать reflected arbitrary `Origin` с `Access-Control-Allow-Credentials: true`.
- Не используйте `Access-Control-Allow-Origin: *` для responses с user, tenant, internal, payment или admin data.
- Трактуйте `Origin` только как browser signal. Non-browser clients могут его подделать; server-side authentication и authorization остаются обязательными.
- Ограничивайте allowed methods и headers до минимального operational set.
- Кэшируйте preflight responses только после стабилизации политики; для sensitive APIs используйте conservative `Access-Control-Max-Age`.

Верификация:
- Протестируйте allowed и denied origins с credentials и без них.
- Проверьте `null` origin, sibling subdomains, attacker-controlled subdomains и HTTP origins против HTTPS APIs.
- Убедитесь, что sensitive responses не содержат wildcard CORS headers.

### 3.3 Cookies, browser storage и session data

Рабочие настройки:
- Session cookies используют `HttpOnly`, `Secure` и явный `SameSite`.
- Используйте `SameSite=Lax` для обычных browser sessions, если flow не требует cross-site POST/iframe behavior.
- Используйте `SameSite=Strict` для high-risk admin или step-up cookies, если UX это допускает.
- Используйте `SameSite=None; Secure` только для документированных cross-site embed или federated flows.
- Сужайте `Domain` и `Path`. Не делите session cookies между unrelated subdomains.
- Не храните access tokens, refresh tokens, session IDs или long-lived secrets в `localStorage`.
- Для browser apps с durable authentication предпочитайте BFF/session-cookie patterns. Если SPA вынуждена хранить tokens, оформляйте risk decision и держите token lifetime коротким согласно OIDC/OAuth playbook.

Верификация:
- Проверьте `Set-Cookie` на login, refresh, step-up, logout и error paths.
- Подтвердите session ID rotation после login и privilege changes.
- Негативный тест: JavaScript не может читать session cookies; украденное local browser state не содержит reusable refresh tokens.

### 3.4 Third-party scripts и frontend supply chain

Рабочие настройки:
- Ведите inventory third-party scripts: owner, purpose, touched data и approval date.
- Не загружайте tag-manager или analytics scripts на admin, checkout, identity или sensitive data-entry pages без явного business approval и минимизации данных.
- Для critical frontend dependencies предпочитайте self-hosting или pinned versions.
- Используйте SRI для static third-party scripts/styles, если provider и update model это позволяют.
- Указывайте `crossorigin="anonymous"` для cross-origin SRI resources, когда это требуется browser behavior.
- Ревью lockfile changes для npm/package, если они затрагивают frontend build, bundler plugins, minifiers, auth/session packages и payment UI.
- Удаляйте unused scripts и stale feature flags; frontend supply-chain risk накапливается через забытые integrations.

Верификация:
- Сравните runtime-loaded scripts с approved inventory.
- Проверьте SRI hashes для static CDN resources.
- Убедитесь, что sensitive DOM fields не доступны scripts, которым они не нужны.

### 3.5 Embedded content и browser APIs

Рабочие настройки:
- Используйте `frame-ancestors` для anti-clickjacking. `X-Frame-Options` оставляйте только как compatibility defense, где это нужно.
- Для untrusted iframes используйте sandbox; capabilities выдавайте явно.
- Для `postMessage` всегда задавайте specific target origin и точно проверяйте `event.origin` на receive.
- Считайте `postMessage` data недоверенным input; не выполняйте его как code и не записывайте в DOM через unsafe sinks.
- Введите явную политику для clipboard, camera, microphone, geolocation, payment и file APIs.
- Используйте `Permissions-Policy`, чтобы по умолчанию отключать powerful browser features на admin, account, checkout, support и internal-tool pages. Начинайте с deny-by-default и открывайте только features, которые нужны конкретному route:

```http
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), serial=(), bluetooth=(), clipboard-read=(), display-capture=(), fullscreen=(self)
```

- Feature-исключения должны иметь owner, affected routes, allowed origins, business purpose, expiry или review date, а также negative test, который показывает, что unauthorized origins не могут использовать feature. Например, checkout может разрешать `payment=(self)` только на payment routes; video-verification flow может разрешать `camera=(self)` только для verification origin и только пока эта feature существует.
- Не выдавайте browser capabilities через iframe `allow` attributes, если parent page `Permissions-Policy` также не разрешает эту feature для embedded origin.

Верификация:
- Попробуйте встроить sensitive pages с untrusted origin.
- Протестируйте `postMessage` с attacker origins и malformed payloads.
- Проверьте iframe `sandbox` и `allow` attributes на least privilege.
- Проверьте effective `Permissions-Policy` response header на sensitive routes через browser DevTools или automated header check.
- Negative test: unapproved origins и unrelated routes не могут получить доступ к camera, microphone, geolocation, payment, display capture, USB/serial/Bluetooth или clipboard-read capabilities.

### 3.6 Transport, referrer и browser isolation headers

Рабочие настройки:
- Используйте `Strict-Transport-Security` для HTTPS-приложений после готовности certificate automation и rollback ownership. Production default: `max-age=31536000`; добавляйте `includeSubDomains` только когда все subdomains готовы к HTTPS, а `preload` — только после отдельного ревью владения domain.
- Задавайте `X-Content-Type-Options: nosniff` для script, style, JSON, file download и API responses, чтобы снизить риск MIME confusion и небезопасной интерпретации content.
- Задавайте `Referrer-Policy: strict-origin-when-cross-origin` как общий default. Используйте `no-referrer` или `same-origin` для admin, identity, payment, support и sensitive data-entry routes, где внешней analytics или partner redirects не нужен referrer context.
- Используйте `Cache-Control: no-store` для authenticated pages и responses с user, tenant, payment, admin или regulated data. Static assets могут иметь долгий cache lifetime только при filename/content hashing.
- Используйте `Cross-Origin-Opener-Policy: same-origin` для admin, account, checkout и internal-tool pages, если OAuth/payment popup behavior не требует `same-origin-allow-popups`.
- Используйте `Cross-Origin-Resource-Policy` для sensitive JSON, media, documents и downloads, чтобы unrelated origins не могли их embedding/consume. Начинайте с `same-origin`; `same-site` используйте только когда sharing между sibling subdomains намеренный.
- Требуйте `Cross-Origin-Embedder-Policy` только для приложений, которым intentionally нужна cross-origin isolation, например `SharedArrayBuffer` или high-resolution timing features. Не включайте его вслепую: каждый embedded script, worker, frame и media resource должен быть совместим через CORP или CORS.
- Не полагайтесь на `X-XSS-Protection`; держите его disabled или absent. Современная XSS-защита строится на output encoding, safe DOM APIs, CSP, Trusted Types там, где они поддерживаются, и ревью dangerous sinks.

Верификация:
- Проверяйте headers на success, error, redirect, login/callback, logout, API, file download и static asset responses; edge/CDN и application responses не должны конфликтовать.
- Валидируйте HSTS на staging domain перед включением `includeSubDomains` или `preload` на parent domain.
- Negative test: authenticated sensitive responses не сохраняются browser cache, CDN или shared proxy; cross-origin pages не сохраняют opener access к sensitive routes; unrelated origins не могут embed protected resources.

---

## 4. Связанные материалы

- [Плейбук OIDC + OAuth 2.0](../../identity/oidc-oauth/playbook.ru.md)
- [Плейбук безопасности API](../../api/api-security-patterns/playbook.ru.md)
- [Плейбук защиты web application по OWASP Top 10](../owasp-top-10/playbook.ru.md)
- [Плейбук безопасной разработки и ревью кода](../../secure-coding/code-review/playbook.ru.md)
- [Плейбук безопасности Agentic AI](../../../ai-security/agentic-ai/playbook.ru.md)
