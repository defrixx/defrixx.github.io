---
title: "Плейбук безопасности Agentic AI"
description: "Этот плейбук покрывает AI agents и multi-agent workflows, которые планируют действия, вызывают tools, используют memory, извлекают context, выполняют code, работают с web или ме..."
sidebar:
  order: 30
---
## 1. Область и цель

Этот плейбук покрывает AI agents и multi-agent workflows, которые планируют действия, вызывают tools, используют memory, извлекают context, выполняют code, работают с web или меняют business state.

Используйте этот документ для:
- security review autonomous и semi-autonomous workflows;
- release gates для agents с tools, memory, browser/email/file access или code execution;
- определения требований к policy enforcement, action tracing, approval, rollback и kill switch;
- подготовки negative tests для tool misuse, memory poisoning, delegation abuse и runaway loops.

Ответственность документа:
- Этот плейбук отвечает за автономию агентов, использование tools агентами, обработку memory/scratchpad/checkpoints, action traces, approvals, rollback и kill-switch behavior.
- Prompt injection, data leakage и excessive agency рассматриваются здесь через призму выполнения агентом действий и business impact.
- Общий AI control baseline находится в [обзоре безопасности AI](/Product-security-playbook/ru/ai-security/securing-ai/overview/), а таксономия угроз — в [обзоре OWASP LLM Top 10](/Product-security-playbook/ru/ai-security/owasp-llm-top-10/overview/).
- Этот плейбук не задает MCP protocol, server registry или transport governance controls; для них используйте [плейбук безопасности MCP](/Product-security-playbook/ru/ai-security/mcp-security/playbook/).

Вне области:
- MCP protocol-specific controls; используйте [плейбук безопасности MCP](/Product-security-playbook/ru/ai-security/mcp-security/playbook/);
- general LLM threat taxonomy; используйте [обзор OWASP LLM Top 10](/Product-security-playbook/ru/ai-security/owasp-llm-top-10/overview/);
- generic API, browser, Kubernetes и supply-chain controls, если они не являются частью agent runtime.

Цель:
- не позволить agents превращать неоднозначные, вредоносные или ошибочные инструкции в unauthorized access, unsafe execution, data leakage или uncontrolled business impact.

---

## 2. Threat Model агента

Минимальные компоненты для моделирования:
- model и prompt layer;
- orchestration loop, planner, router, policy engine и tool selector;
- working memory, scratchpad, long-term memory, retrieval stores и checkpoints;
- tools и downstream systems;
- user, workload и tool identities;
- browser, URL fetcher, file parser, code interpreter, shell или office/email integration;
- audit trail, approvals, rollback paths и kill switch.

Сценарии с высоким воздействием:
- prompt injection или poisoned retrieval content заставляет agent вызвать tool вне intended task;
- long-running workflow накапливает secrets, PII или tokens в scratchpad, memory, logs или serialized checkpoints;
- browser или code-execution tool скачивает malicious content, выполняет generated code или обращается к internal network destinations;
- один agent делегирует задачу более privileged agent или shared tool без сохранения исходного authorization context;
- agent выполняет технически валидные действия, нарушающие business intent, например bulk deletion, duplicate transaction или external disclosure.

---

## 3. Production Baseline

### 3.1 Agent Inventory and Classification

`Baseline`:
- Ведите inventory production agents, owners, runtime location, model/provider, autonomy level, tools, memory stores, retrieval sources, identities, data classes и business operations.
- Классифицируйте каждый agent по максимальному impact, а не по intended use. Read-only assistant с доступом к confidential data все равно sensitive; agent с одним write tool может быть high-impact.
- Делайте первичный triage по трем осям: attack surface, blast radius и доказуемость defense controls. Минимальный быстрый вопрос: выполняет ли agent tools, и если да, изолировано ли execution от host, internal network, credentials и production data.
- Оценивайте agent в двух состояниях: vendor-as-shipped/default configuration и фактически deployed configuration. Если безопасная posture зависит от opt-in settings, paid features, customer-managed gateway, sandbox или egress policy, это должно быть видно в release decision.
- Не засчитывайте vendor claim как control без evidence, что он принудительно применяется. Detection-only guardrail, который только логирует или предупреждает после irreversible action, является forensic signal, а не preventive control.
- Назначайте явный autonomy profile:
  - `Assistive`: нет tool execution или только user-visible draft output.
  - `Read-only tool user`: может извлекать данные, но не менять business state.
  - `State-changing agent`: может create, update, submit, trigger или delete.
  - `Execution agent`: может run code, browse, manipulate files или работать с external content.

`High-impact/regulated`:
- Требуйте named product owner, security owner, SRE/operations owner и data owner до запуска.
- Пересматривайте access и tool entitlements минимум ежеквартально и после каждого material model/provider/tool change.

### 3.2 Policy Enforcement and Authorization

`Baseline`:
- Размещайте policy enforcement layer между model output и tool execution. Model может предложить action; policy решает, можно ли его выполнить.
- Authorize каждый tool call по user/workload identity, tenant, role, data class, environment, action и workflow state.
- Никогда не считайте model reasoning, natural-language instructions, prompt text или tool descriptions authorization evidence.
- Разделяйте tools по risk: read/write/admin/bulk/export/destructive operations должны быть отдельными capabilities с отдельными scopes.
- Используйте short-lived, tool-specific credentials. Не используйте одну broad agent identity для unrelated tools.

`High-impact/regulated`:
- Требуйте step-up authentication или human approval для high-impact, irreversible, cross-tenant, financial, security, privacy или external-disclosure actions.
- Удаляйте active tokens, secrets и session cookies из checkpoints, scratchpads, persisted memory, tool outputs и execution traces до сохранения.
- Для multi-agent workflows передавайте original user/workload context и применяйте delegation boundaries на каждом hop.

Стартовые defaults:
- `max autonomous steps=5` для read-only workflows;
- `max autonomous steps=3` до re-authorization для state-changing workflows;
- `max tool-chain depth=3`;
- default state-changing execution flow: `preview -> explicit confirm -> execute`;
- kill-switch SLO `<=60s` для state-changing или execution agents.

### 3.3 Memory, Retrieval, and State

`Baseline`:
- Считайте working memory, scratchpads, long-term memory, vector stores, summaries, checkpoints и tool outputs data stores, на которые распространяются classification, access control, retention, deletion и audit requirements.
- Исключайте secrets, tokens, credentials, raw regulated data и unnecessary sensitive fields из memory по policy.
- Применяйте document-level и tenant-level authorization до попадания retrieved content в agent context.
- Помечайте untrusted retrieved content как untrusted. Он может влиять на answer, но не должен переопределять policy, identity или tool authorization.
- Версионируйте prompts, memory rules, retrieval policies, embedding models и dataset snapshots, чтобы incident response мог откатывать context, а не только code.

`High-impact/regulated`:
- Используйте memory write policies, которые валидируют, что agent может сохранять, кто сможет прочитать это позже и когда запись истекает.
- Quarantine или disable memory sources при признаках poisoning, unexpected sensitive data или abnormal write patterns.
- Тестируйте recovery на semantic integrity: restored vector stores и memory должны давать expected authorized retrieval behavior и не должны возвращать poisoned content.

Production defaults:
- no indefinite retention для working memory;
- raw session/scratchpad retention disabled by default вне forensic mode;
- memory entries с sensitive data требуют explicit retention class и deletion workflow;
- forensic raw payload capture retention `<=30 days`.

### 3.4 Browser, Email, File, and Code Execution Tools

`Baseline`:
- Запускайте browser automation, URL fetchers, file parsers и code interpreters в isolated sandboxes без default access к internal networks, host files, cloud metadata services или production credentials.
- Принудительно применяйте egress allowlists для agent-run browsers и fetch tools. Используйте deny-by-default для arbitrary public web access.
- Сканируйте и санитизируйте downloaded или retrieved content до попадания в memory, RAG pipelines или execution tools.
- Блокируйте high-risk file types по умолчанию: executables, scripts, archives, macros и active content, если workflow явно их не требует.
- Быстро patch browser engines, HTML/PDF/document parsers, sandbox images и execution runtimes.

`High-impact/regulated`:
- Требуйте human approval перед execution third-party code, generated code with external side effects, package installation, shell commands или file operations вне temporary workspace.
- Используйте ephemeral execution environments с network restrictions, CPU/memory/time limits, read-only base images where practical и central log export before teardown.
- Запрещайте agents autonomously navigating public web для state-changing workflows, если domain set, data handling и prompt-injection controls не прошли явное ревью.

### 3.5 Action Trace, Monitoring, and Incident Response

`Baseline`:
- Формируйте agent action trace, который фиксирует security-relevant decisions без хранения unnecessary raw sensitive content.
- Коррелируйте model calls, retrieval events, memory writes, tool invocations, policy decisions, approvals, downstream actions и final output.
- Настройте alerts на abnormal tool sequences, repeated policy denials, new tool combinations, unexpected memory writes, cross-tenant attempts, high token/request spend и behavior drift после model или prompt changes.
- Не храните raw prompts, context, tool payloads и scratchpads в обычных logs; используйте minimized metadata и redacted fields.

`High-impact/regulated`:
- Поддерживайте runbooks для data leakage, runaway agent, malicious tool use, poisoned memory/RAG source, компрометации учетных данных tool и unsafe state-changing action.
- Тестируйте kill switch и rollback paths до launch и после major runtime/tool changes.
- Проверяйте incident timelines на реальных log fields; runbook не готов, если responders не могут восстановить, кто или что вызвало downstream action.

---

## 4. Проверка

Обязательные подтверждения:
- agent inventory entry с autonomy profile, owner, tools, memory stores, identities и data classes;
- vendor-as-shipped vs deployed-configuration assessment, включая enabled tools, memory, connectors, sandboxing, egress controls, approval modes и paid/optional security features;
- policy matrix: `who/what/can-do` для каждого tool и memory source;
- action trace schema и sample redacted trace;
- sandbox configuration для browser/file/code tools;
- memory retention и deletion policy;
- approval и kill-switch drill results для high-impact agents.

Negative tests:
- prompt injection пытается вызвать forbidden tool и блокируется policy;
- retrieved document требует ignore policy и не может переопределить tool authorization;
- user from tenant A не может читать или изменять данные tenant B через memory, tools или delegated agents;
- write action не выполняется без preview и confirmation;
- serialized checkpoint не содержит active tokens или secrets;
- browser tool не может обратиться к cloud metadata, internal admin services или unapproved external domains;
- code execution не может получить доступ к host filesystem, учетным данным production-среды или unrestricted network egress;
- multi-agent delegation сохраняет original authorization context.

Операционные сигналы:
- percentage tool calls with policy decision logged;
- approval coverage для high-impact actions;
- denied tool calls per 1k sessions;
- memory write rejection rate и sensitive-data detections;
- mean time to kill runaway agents, target `<=60s`;
- behavior drift alerts после model, prompt, tool или memory-policy changes.

---

## 5. Review Decision

| Severity | Agent condition | Обязательное действие |
|---|---|---|
| Critical | Agent может autonomously выполнять irreversible, financial, administrative, cross-tenant или external-disclosure actions без policy enforcement и approval | Блокировать релиз |
| Critical | Execution/browser tool может обратиться к учетным данным production-среды, host filesystem, cloud metadata или internal network by default | Блокировать релиз и изолировать runtime |
| High | Memory/checkpoints могут сохранять активные учетные данные, secrets или regulated data без retention и deletion controls | Блокировать high-impact workflows до исправления |
| High | Multi-agent workflow теряет original authorization context или допускает privilege escalation through delegation | Блокировать релиз для privileged workflows |
| High | Action traces не позволяют reconstruct high-impact downstream actions | Исправить до production launch |
| High | Tool-executing agent зависит от vendor-claimed, opt-in или detection-only controls без доказуемого sandboxing, egress control и authorization enforcement в deployed configuration | Блокировать state-changing/execution workflows до подтверждения controls |
| Medium | Inventory или policy matrix incomplete для read-only или low-impact agents | Завести remediation с owner и due date |
| Medium | Behavior drift monitoring отсутствует после model/prompt changes | Требовать compensating review и test evidence |
| Low | Prompt, tool или memory metadata без consistent naming, но access или logging не затронуты | Исправить opportunistically |

Релиз считается одобренным только когда agent имеет bounded autonomy, explicit policy enforcement, safe memory handling, isolated execution surfaces, usable forensic traces и tested kill-switch behavior.

---

## 6. Связанные материалы

- [Обзор безопасности AI](/Product-security-playbook/ru/ai-security/securing-ai/overview/)
- [Плейбук безопасности MCP](/Product-security-playbook/ru/ai-security/mcp-security/playbook/)
- [Обзор OWASP LLM Top 10](/Product-security-playbook/ru/ai-security/owasp-llm-top-10/overview/)
- [Плейбук моделирования угроз](/Product-security-playbook/ru/review/threat-modeling/playbook/)
- [Плейбук безопасности браузера и frontend-части](/Product-security-playbook/ru/application-security/web/browser-security/playbook/)
- [Плейбук безопасности API](/Product-security-playbook/ru/application-security/api/api-security-patterns/playbook/)
