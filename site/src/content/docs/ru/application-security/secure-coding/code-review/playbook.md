---
title: "Плейбук безопасной разработки и ревью кода"
description: "Этот плейбук описывает ревью безопасности на уровне кода: валидацию входных данных, кодирование вывода, реализацию аутентификации и сессий, контроль доступа, защиту от инъекций,..."
sidebar:
  order: 50
---
## 1. Область и цель

Этот плейбук описывает ревью безопасности на уровне кода: валидацию входных данных, кодирование вывода, реализацию аутентификации и сессий, контроль доступа, защиту от инъекций, работу с файлами, журналирование, использование криптографии, зависимости и подтверждения, которые должны оставаться после ревью.

Используйте его при проверке:
- новых эндпоинтов, фоновых задач, парсеров, интеграций и путей обработки данных;
- изменений в логике аутентификации, авторизации, сессий, паролей, токенов или идентичности;
- кода, который обрабатывает файлы, внешние URL, шаблоны, запросы к хранилищам, shell-команды, секреты или криптографические операции;
- исправлений по результатам SAST, DAST, SCA, пентеста, bug bounty или инцидента.

Вне области:
- злоупотребление штатным поведением продукта: используйте [плейбук abuse бизнес-логики](/Product-security-playbook/ru/application-security/business-logic/business-logic-abuse/playbook/);
- архитектура OAuth/OIDC, токенов и протокольных потоков: используйте [плейбук OIDC + OAuth 2.0](/Product-security-playbook/ru/application-security/identity/oidc-oauth/playbook/);
- браузерные меры контроля, включая CSP, CORS, cookies и frontend supply chain: используйте [плейбук безопасности браузера и frontend-части](/Product-security-playbook/ru/application-security/web/browser-security/playbook/);
- API-паттерны для REST, SOAP/XML, GraphQL, Webhooks и gRPC: используйте [плейбук API security](/Product-security-playbook/ru/application-security/api/api-security-patterns/playbook/).

Цель:
- сделать решения по ревью кода конкретными и проверяемыми;
- находить уязвимости до релиза, не превращая ревью в формальное прохождение чек-листа;
- сохранять достаточно подтверждений, чтобы позже восстановить замечание, исправление и остаточный риск.

---

## 2. Модель угроз

Активы:
- пользовательские и tenant-данные, учетные данные, сессии, токены, секреты, бизнес-состояние, журналы, файлы, конфигурация и downstream-системы, до которых приложение может обращаться.

Атакующие и точки входа:
- неаутентифицированные пользователи, отправляющие специально сформированные HTTP/API-запросы;
- аутентифицированные пользователи, меняющие object ID, tenant ID, состояние workflow, фильтры, ключи сортировки или поля, влияющие на роль и доступ;
- партнерские системы, webhooks, очереди сообщений, загрузки файлов, импортируемые документы и сторонние API;
- скомпрометированные зависимости, вредоносные пакеты, утекшие секреты и входные данные этапа сборки.

Сценарии с высоким влиянием:
- пользовательский ввод попадает в интерпретатор: SQL, NoSQL, LDAP, XML, template engine, OS shell, browser, deserializer или expression evaluator;
- отсутствующая object-level authorization раскрывает данные другого tenant;
- слабая обработка сессии или токена позволяет replay, fixation, privilege escalation или использование после logout/revocation;
- загруженные файлы становятся исполняемым контентом, транспортом malware, помощником для SSRF или stored XSS payload;
- журналы, ошибки, трассировки или аналитика раскрывают секреты и регулируемые данные.

---

## 3. Базовый профиль

### 3.1 Валидация входных данных и canonicalization

Рабочие настройки:
- Валидируйте все недоверенные входные данные на серверной стороне до бизнес-логики, сохранения, построения запросов или вызова downstream-систем.
- Для каждого поля, контролируемого извне, задавайте ожидаемый тип, длину, формат, кодировку, диапазон, допустимые enum-значения и правила владения объектом.
- Выполняйте canonicalization до валидации там, где принимаются разные кодировки, path formats или эквивалентные представления одного значения.
- Используйте списки разрешенных значений для identifiers, enum values, sort keys, fields, redirect targets, callback URLs, MIME types и file extensions.
- По умолчанию отклоняйте данные, не прошедшие валидацию. Молчаливая нормализация допустима только если владелец продукта и security reviewer согласны, что неоднозначность не может изменить авторизацию, цену, состояние или выборку данных.

Верификация:
- Negative tests покрывают слишком длинные значения, encoded bypasses, неожиданный Unicode, duplicate parameters, nested JSON, array/object confusion и неподдерживаемые enum-значения.
- Server-side validation нельзя обойти отключением frontend checks или прямым вызовом API.

### 3.2 Кодирование вывода и границы интерпретаторов

Рабочие настройки:
- Кодируйте вывод под точный target context: HTML body, HTML attribute, JavaScript, CSS, URL, SQL, LDAP, XML, shell, template, log или CSV.
- Считайте output encoding контекстно-зависимой мерой контроля. Один общий escaping helper для всех интерпретаторов недопустим.
- Предпочитайте безопасные API: parameterized queries, prepared statements, structured logging, shell-free process invocation, безопасные шаблонизаторы и framework-native encoders.
- Запрещайте dangerous sinks: `eval`, dynamic template evaluation, unsafe deserialization и shell concatenation, если нет узкого, отдельно reviewed exception.

Верификация:
- Tests доказывают, что недоверенные строки отображаются как данные, а не как исполняемый код или синтаксис запроса.
- Ревью кода прослеживает user-controlled values от source до sink и фиксирует encoding или safe API на границе интерпретатора.

### 3.3 Аутентификация, сессии и контроль доступа

Рабочие настройки:
- Проверки аутентификации и сессий выполняются на серверной стороне и fail closed.
- Session identifiers ротируются после login, privilege change, recovery и sensitive account changes.
- Авторизация принудительно применяется в service/domain layer для каждого object и state transition, а не только в routing, UI или gateway rules.
- Resource ownership, tenant membership, role, scope и policy context оцениваются вместе. Valid token или session не является достаточной авторизацией.
- Privileged actions требуют step-up или explicit approval там, где impact высокий: admin changes, payout/payment changes, bulk export, destructive action, support impersonation и permission grant.

Верификация:
- Tests покрывают horizontal access, vertical access, cross-tenant access, stale session, logout/revocation behavior и direct calls to hidden routes.
- Batch, async job, GraphQL, webhook и export paths применяют ту же authorization model, что и single-object APIs.

### 3.4 Инъекции и безопасность запросов

Рабочие настройки:
- SQL, NoSQL, LDAP, XML, search и analytics queries используют parameterized или structured APIs.
- User-controlled identifiers, например column names, sort keys, index names, collection names и query operators, проходят через явные списки разрешенных значений.
- Shell commands следует избегать. Если process execution необходим, передавайте arguments как array, избегайте shell interpolation, ограничивайте executable paths и запускайте процесс с least privilege.
- XML parsing недоверенного ввода отключает DTDs, external entities, external DTD loading, XInclude и network access. Secure processing mode и ограничения entity/depth/size включаются там, где parser это поддерживает.
- XML schema validation не должен скачивать external schemas или DTDs в runtime. Нужные schemas закрепляются, проходят review и загружаются из trusted local или контролируемых источников.
- Если SOAP/XML, SAML-like payloads или partner XML требуют функций, ослабляющих default parser profile, exception фиксирует parser/library version, enabled features, external fetch behavior, payload size limit, владельца, срок действия и negative test evidence.

Верификация:
- Tests включают injection payloads для каждого интерпретатора, который использует измененный код.
- Review подтверждает, что ORM, query builder и serialization helpers не возвращают string-built query fragments.
- XML negative tests включают DOCTYPE rejection, external entity/file read payloads, external DTD/network fetch attempts, entity expansion/XML bomb payloads, oversized documents и schema import attempts.

### 3.5 Работа с файлами и внешними запросами

Рабочие настройки:
- Загрузка файлов должна enforce size limits, extension policy, MIME/content checks, malware scanning там, где применимо, случайные server-side имена и хранение вне исполняемых web roots.
- Upload limits задаются явно для каждого route: maximum file size, maximum multipart body size, maximum file count, accepted content types, storage class, retention, quarantine behavior и asynchronous scan timeout.
- Uploaded content отдается с безопасными `Content-Type`, `Content-Disposition: attachment`, если inline rendering не требуется, `X-Content-Type-Options: nosniff` и cache policy, соответствующей data class.
- Malware или content-policy scanning выполняется до trusted processing или широкой доступности файла. Scan failures, timeouts и unknown verdicts fail closed для high-risk file classes и отправляются в quarantine или manual review.
- Archive extraction защищает от path traversal, absolute paths, symlinks/hardlinks, special files, zip bombs, nested compression, excessive file count, excessive path length и overwrite of existing files. Extraction запускается в изолированном working directory с output-size и decompression-ratio limits.
- Server-side URL fetches используют allowlisted schemes и destinations, DNS resolution checks, IP range blocking, redirect limits, timeout limits, response size limits и блокировку metadata networks.
- SSRF defenses проверяют resolved target до connect и после redirects; блокируют localhost, loopback, link-local, cloud metadata, private, multicast и другие non-routable ranges, если destination не является явно утвержденной internal integration.
- Для DNS names учитывайте rebinding: выполняйте resolution через trusted resolvers, применяйте allowlists к final resolved IPs, не используйте stale validation после изменения connection target и предпочитайте egress proxy или network policy для high-risk fetchers.
- Не позволяйте fetched content запускать second-stage request, parser, archive extraction или template rendering без повторной validation для нового sink. Webhook и import handlers должны сохранять raw bodies, когда signature verification зависит от exact bytes; parsing, decompression, charset conversion или middleware mutation должны выполняться только после signature verification.

Верификация:
- Tests покрывают polyglot files, malware-test fixtures, path traversal, absolute paths, symlink archive entries, archive traversal, decompression bombs, excessive file count, oversized payloads, content-type confusion, scan timeout behavior и unsafe inline rendering.
- SSRF tests покрывают link-local и cloud metadata ranges, localhost, private IPv4 and IPv6 ranges, IPv4-mapped IPv6, decimal/hex/octal IP encodings там, где parsers их поддерживают, redirects to blocked ranges, DNS rebinding, slow responses, oversized responses и blocked egress logs.
- Для более глубоких API-specific controls по webhook, GraphQL, SOAP/XML и gRPC сверяйтесь с [плейбуком API security](/Product-security-playbook/ru/application-security/api/api-security-patterns/playbook/). Для browser rendering загруженного или generated content сверяйтесь с [плейбуком безопасности браузера и frontend-части](/Product-security-playbook/ru/application-security/web/browser-security/playbook/).

### 3.6 Журналирование, ошибки и privacy

Рабочие настройки:
- Журналы включают correlation ID, actor, tenant, object, action, result и reason там, где это полезно для расследования.
- Журналы не включают passwords, session IDs, refresh tokens, access tokens, private keys, raw authorization headers, reset tokens, payment secrets или лишние personal data.
- Error responses должны помогать legitimate clients, но не раскрывать stack traces, internal paths, SQL fragments, secret names или факт существования account.
- Security-relevant failures создают наблюдаемые события: denied authorization, validation rejection, suspicious upload, SSRF block, token validation failure и policy bypass attempt.

Верификация:
- Tests и ревью кода проверяют success и failure paths на утечку secrets или PII.
- Журналирование в рабочей среде имеет срок хранения, контроль доступа и маскирование, соответствующие data class.

### 3.7 Криптография и секреты

Рабочие настройки:
- Используйте vetted platform libraries и standard protocols. Не реализуйте custom encryption, signature, password hashing, random generation или token formats без явного cryptographic review.
- Passwords используют current password hashing scheme с per-password unique salt и stored algorithm/cost metadata. Default для новых систем: Argon2id минимум с `19 MiB` memory, `2` iterations и parallelism `1`; повышайте memory/time cost, когда login latency и capacity это позволяют.
- Используйте bcrypt только для compatibility или когда Argon2id/scrypt недоступны; настраивайте cost `>=10`, benchmark toward the highest tolerable cost и явно обрабатывайте bcrypt `72` byte input limit через library support или reviewed pre-hashing.
- Используйте PBKDF2 только когда этого требуют platform или FIPS constraints; применяйте PBKDF2-HMAC-SHA-256 минимум с `600,000` iterations, если более новый approved local standard не требует большего.
- Password verification должен enforce input length ceiling, достаточно высокий для passphrases, но ограниченный против hash-time DoS. Не допускайте silent truncation passwords.
- Выполняйте rehash on successful login, когда stored algorithm или cost ниже текущей baseline. Legacy hash migration должна держать old verifiers изолированными, observable и time-boxed.
- Pepper можно использовать как defense-in-depth только если он хранится отдельно в KMS/HSM или equivalent secret store, имеет rotation и emergency revocation procedures и не считается заменой strong hashing.
- Keys и secrets загружаются из secrets manager или protected runtime environment, а не из source code, images, client-side bundles, logs или default config.
- Encryption decisions описывают, что защищается, от кого, где живут keys, как работает rotation и какие audit-подтверждения доказывают доступ.

Верификация:
- Review подтверждает secure random generation, authenticated encryption там, где encryption используется для integrity-sensitive data, key separation, rotation path, отсутствие secret material в code или tests и password hash parameters, соответствующие approved baseline.
- Tests покрывают password verification для long inputs, Unicode normalization policy, legacy hash upgrade, отсутствие truncation, wrong-password timing behavior и rate limiting вокруг expensive hash operations.
- Secrets scanning покрывает историю репозитория, доступные CI variables, build logs, container layers и deployment manifests.

---

## 4. Overlay для ревью бизнес-логики

Даже безопасно написанный код может нарушить бизнес-инварианты. Для sensitive flows добавляйте этот overlay и сверяйтесь с [плейбуком abuse бизнес-логики](/Product-security-playbook/ru/application-security/business-logic/business-logic-abuse/playbook/).

Вопросы для ревью:
- Ownership checks: может ли пользователь действовать с object, которым он не владеет, через изменение ID, filter, export job, batch item или async task reference?
- Tenant isolation: выводится ли tenant context из authenticated membership и policy, а не только из request fields?
- Workflow state transitions: являются ли allowed transitions явными, и отклоняются ли direct calls к поздним states?
- Price, discount, promo и credit abuse: могут ли retries, изменение порядка операций, refund paths или coupon stacking создать value за пределами intended budgets?
- Idempotency и replay: дают ли duplicate requests, webhooks, queue messages и retries не больше одного external effect?
- Race conditions: могут ли concurrent requests обойти quotas, double spend, overbook, approve twice или выиграть stale authorization decision?
- Approval bypass: может ли actor с меньшими правами вызвать internal endpoint, background job или bulk operation, который пропускает human approval?
- Quota и rate-limit abuse: применяются ли limits по правильным actor dimensions: account, tenant, source, device/session signal, payment instrument, API client и time window?
- Privilege escalation through legitimate features: могут ли invite, support, impersonation, role change, export или integration features создать unintended authority?

Обязательные подтверждения:
- negative tests для каждого critical invariant;
- log/audit events для denied attempts;
- release decision, утвержденное владельцем, если invariant намеренно ослаблен.

---

## 5. Матрица решения review

| Severity | Когда использовать | Обязательное действие |
|---|---|---|
| Critical | Прямой exploitable path к credential/session compromise, cross-tenant data access, remote code execution, secret exposure, payment manipulation или unsafe релиз в рабочую среду | Блокировать релиз до исправления; исключение требует явного authorized risk acceptance, если policy это допускает |
| High | Реалистичная эксплуатация в рабочей среде injection, authorization bypass, sensitive data leakage, unsafe file handling, SSRF, crypto misuse или отсутствие security evidence для high-risk change | Владелец, срок, исправление или accepted risk и verification evidence |
| Medium | Значимый разрыв с bounded impact, lower likelihood или сильными компенсирующими мерами | Отслеживать устранение и проверить закрытие |
| Low | Hardening, clarity, test coverage или logging improvement с ограниченным direct impact | Исправить при ближайшей возможности |

Обязательный результат review:
- summary замечания и affected code path;
- attacker preconditions и impact;
- требуемое исправление или компенсирующая мера;
- verification method;
- владелец, due date и residual risk decision.

---

## 6. Связанные материалы

- [Плейбук abuse бизнес-логики](/Product-security-playbook/ru/application-security/business-logic/business-logic-abuse/playbook/)
- [Плейбук API security](/Product-security-playbook/ru/application-security/api/api-security-patterns/playbook/)
- [Плейбук безопасности браузера и frontend-части](/Product-security-playbook/ru/application-security/web/browser-security/playbook/)
- [Плейбук OIDC + OAuth 2.0](/Product-security-playbook/ru/application-security/identity/oidc-oauth/playbook/)
- [Плейбук управления уязвимостями](/Product-security-playbook/ru/review/vulnerability-management/playbook/)
- [Плейбук безопасности MCP](/Product-security-playbook/ru/ai-security/mcp-security/playbook/)
- [Плейбук безопасности Agentic AI](/Product-security-playbook/ru/ai-security/agentic-ai/playbook/)
