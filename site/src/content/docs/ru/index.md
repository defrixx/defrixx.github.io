---
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

## Карта сайта

<div class="site-map-grid">
<section class="site-map-card">
<h3><a href="/Product-security-playbook/ru/review/overview/">Ревью и управление</a></h3>
<ul>
<li><a href="/Product-security-playbook/ru/review/architecture/checklist/">Архитектурное ревью</a></li>
<li><a href="/Product-security-playbook/ru/review/threat-modeling/playbook/">Моделирование угроз</a></li>
<li><a href="/Product-security-playbook/ru/review/release-governance/playbook/">Управление выпуском</a></li>
<li><a href="/Product-security-playbook/ru/review/vulnerability-management/playbook/">Управление уязвимостями</a></li>
</ul>
</section>
<section class="site-map-card">
<h3><a href="/Product-security-playbook/ru/application-security/overview/">Безопасность приложений</a></h3>
<ul>
<li><a href="/Product-security-playbook/ru/application-security/web/owasp-top-10/playbook/">OWASP Top 10</a></li>
<li><a href="/Product-security-playbook/ru/application-security/web/browser-security/playbook/">Защита в браузере</a></li>
<li><a href="/Product-security-playbook/ru/application-security/api/api-security-patterns/playbook/">Безопасность API</a></li>
<li><a href="/Product-security-playbook/ru/application-security/business-logic/business-logic-abuse/playbook/">Бизнес-логика</a></li>
<li><a href="/Product-security-playbook/ru/application-security/secure-coding/code-review/playbook/">Ревью кода</a></li>
<li><a href="/Product-security-playbook/ru/application-security/identity/oidc-oauth/playbook/">OIDC и OAuth</a></li>
</ul>
</section>
<section class="site-map-card">
<h3><a href="/Product-security-playbook/ru/platform-security/overview/">Безопасность платформы</a></h3>
<ul>
<li><a href="/Product-security-playbook/ru/platform-security/kubernetes/cluster-security-review/playbook/">Ревью кластера</a></li>
<li><a href="/Product-security-playbook/ru/platform-security/kubernetes/adversarial-validation/playbook/">Проверка защиты от атак</a></li>
<li><a href="/Product-security-playbook/ru/platform-security/kubernetes/pod-security/playbook/">Безопасность Pod</a></li>
<li><a href="/Product-security-playbook/ru/platform-security/kubernetes/secrets/playbook/">Секреты Kubernetes</a></li>
<li><a href="/Product-security-playbook/ru/platform-security/kubernetes/seccomp/checklist/">Проверка seccomp</a></li>
<li><a href="/Product-security-playbook/ru/platform-security/kubernetes/container-escape-capability-abuse/overview/">Выход из контейнера и capabilities</a></li>
<li><a href="/Product-security-playbook/ru/platform-security/secrets/vault/playbook/">Секреты в Vault</a></li>
</ul>
</section>
<section class="site-map-card">
<h3><a href="/Product-security-playbook/ru/supply-chain/overview/">Цепочка поставки</a></h3>
<ul>
<li><a href="/Product-security-playbook/ru/supply-chain/slsa-provenance/overview/">SLSA и происхождение сборок</a></li>
<li><a href="/Product-security-playbook/ru/supply-chain/container-image-security/playbook/">Контейнерные образы</a></li>
</ul>
</section>
<section class="site-map-card">
<h3><a href="/Product-security-playbook/ru/ai-security/overview/">Безопасность ИИ</a></h3>
<ul>
<li><a href="/Product-security-playbook/ru/ai-security/securing-ai/overview/">Защита функций ИИ</a></li>
<li><a href="/Product-security-playbook/ru/ai-security/owasp-llm-top-10/overview/">OWASP LLM Top 10</a></li>
<li><a href="/Product-security-playbook/ru/ai-security/agentic-ai/playbook/">Безопасность агентов</a></li>
<li><a href="/Product-security-playbook/ru/ai-security/mcp-security/playbook/">Безопасность MCP</a></li>
<li><a href="/Product-security-playbook/ru/ai-security/ai-assisted-development/playbook/">Разработка с ИИ</a></li>
</ul>
</section>
<section class="site-map-card">
<h3><a href="/Product-security-playbook/ru/ai-automation/security-skills/overview/">Скиллы и инструменты</a></h3>
<ul>
<li><a href="/Product-security-playbook/ru/ai-automation/security-skills/secure-development/overview/">Безопасная разработка</a></li>
<li><a href="/Product-security-playbook/ru/ai-automation/security-skills/security-review/overview/">Ревью безопасности</a></li>
<li><a href="/Product-security-playbook/ru/ai-automation/security-skills/sensitive-data-cleanup/overview/">Очистка чувствительных данных</a></li>
<li><a href="/Product-security-playbook/ru/ai-automation/security-skills/security-report-triage/overview/">Разбор отчетов безопасности</a></li>
<li><a href="/Product-security-playbook/ru/ai-automation/security-skills/security-fix-verification/overview/">Проверка исправлений</a></li>
<li><a href="/Product-security-playbook/ru/ai-automation/security-skills/workflow/overview/">Совместная работа скиллов</a></li>
<li><a href="/Product-security-playbook/ru/ai-automation/prompt-integrity/overview/">prompt-integrity</a></li>
</ul>
</section>
<section class="site-map-card">
<h3>Справочник</h3>
<ul>
<li><a href="/Product-security-playbook/ru/reference/infrastructure-technologies/infrastructure-technologies/">Инфраструктурные технологии</a></li>
</ul>
</section>
</div>
