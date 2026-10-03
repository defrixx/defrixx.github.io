---
title: "Product Security Playbook"
description: "Практическая база знаний по безопасности приложений, платформы, цепочки поставки и ИИ."
tableOfContents: false
sidebar:
  order: 0
---

Практическая база знаний для проверки архитектуры, кода, платформы и инженерных процессов.

Здесь собраны плейбуки, чеклисты и методики ревью, которые помогают применять отраслевые стандарты и инженерные практики к конкретным задачам безопасности продукта.

Материалы обновляются по мере развития технологий и способов атак. При работе с ними учитывайте архитектуру, версии компонентов и модель угроз своего проекта.

<section class="home-getting-started" aria-labelledby="home-start-title">
<h2 id="home-start-title">С чего начать</h2>
<div class="site-map-grid">
<section class="site-map-card">
<h3>Проверить архитектуру</h3>
<p>Определите границы доверия и сценарии атак, затем проверьте проектные решения.</p>
<ul>
<li><a href="/Product-security-playbook/ru/review/threat-modeling/playbook/">Моделирование угроз</a></li>
<li><a href="/Product-security-playbook/ru/review/architecture/checklist/">Архитектурное ревью</a></li>
</ul>
</section>
<section class="site-map-card">
<h3>Разработать или проверить код</h3>
<p>Выберите применимые требования, проверьте защитные меры и зафиксируйте результаты.</p>
<ul>
<li><a href="/Product-security-playbook/ru/application-security/secure-coding/code-review/playbook/">Ревью кода</a></li>
<li><a href="/Product-security-playbook/ru/ai-automation/security-skills/secure-development/overview/">Скилл безопасной разработки</a></li>
</ul>
</section>
<section class="site-map-card">
<h3>Подготовить выпуск в рабочую среду</h3>
<p>Проверьте платформу, права развертывания и условия допуска релиза.</p>
<ul>
<li><a href="/Product-security-playbook/ru/platform-security/kubernetes/cluster-security-review/playbook/">Ревью Kubernetes-кластера</a></li>
<li><a href="/Product-security-playbook/ru/review/release-governance/playbook/">Управление выпуском</a></li>
</ul>
</section>
<section class="site-map-card">
<h3>Защитить ИИ-систему</h3>
<p>Начните с общих мер защиты, затем выберите проверки для агентов и интеграций.</p>
<ul>
<li><a href="/Product-security-playbook/ru/ai-security/securing-ai/overview/">Защита функций ИИ</a></li>
<li><a href="/Product-security-playbook/ru/ai-security/overview/">Выбор плейбука по задаче</a></li>
</ul>
</section>
</div>
</section>

<section class="home-site-map" aria-labelledby="home-site-map-title">
<h2 id="home-site-map-title">Карта сайта</h2>
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
<div class="site-map-group">
<h4>Код, API и доступ</h4>
<ul>
<li><a href="/Product-security-playbook/ru/application-security/api/api-security-patterns/playbook/">Безопасность API</a></li>
<li><a href="/Product-security-playbook/ru/application-security/business-logic/business-logic-abuse/playbook/">Бизнес-логика</a></li>
<li><a href="/Product-security-playbook/ru/application-security/secure-coding/code-review/playbook/">Ревью кода</a></li>
<li><a href="/Product-security-playbook/ru/application-security/identity/oidc-oauth/playbook/">OIDC и OAuth</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Веб и браузер</h4>
<ul>
<li><a href="/Product-security-playbook/ru/application-security/web/owasp-top-10/playbook/">OWASP Top 10</a></li>
<li><a href="/Product-security-playbook/ru/application-security/web/browser-security/playbook/">Защита в браузере</a></li>
</ul>
</div>
</section>
<section class="site-map-card">
<h3><a href="/Product-security-playbook/ru/platform-security/overview/">Безопасность платформы</a></h3>
<div class="site-map-group">
<h4>Kubernetes</h4>
<ul>
<li><a href="/Product-security-playbook/ru/platform-security/kubernetes/cluster-security-review/playbook/">Ревью кластера</a></li>
<li><a href="/Product-security-playbook/ru/platform-security/kubernetes/adversarial-validation/playbook/">Проверка защиты от атак</a></li>
<li><a href="/Product-security-playbook/ru/platform-security/kubernetes/pod-security/playbook/">Безопасность Pod</a></li>
<li><a href="/Product-security-playbook/ru/platform-security/kubernetes/secrets/playbook/">Секреты Kubernetes</a></li>
<li><a href="/Product-security-playbook/ru/platform-security/kubernetes/seccomp/checklist/">Проверка seccomp</a></li>
<li><a href="/Product-security-playbook/ru/platform-security/kubernetes/container-escape-capability-abuse/overview/">Выход из контейнера и capabilities</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Управление секретами</h4>
<ul>
<li><a href="/Product-security-playbook/ru/platform-security/secrets/vault/playbook/">Секреты в Vault</a></li>
</ul>
</div>
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
<div class="site-map-group">
<h4>Защита ИИ и типовые угрозы</h4>
<ul>
<li><a href="/Product-security-playbook/ru/ai-security/securing-ai/overview/">Защита функций ИИ</a></li>
<li><a href="/Product-security-playbook/ru/ai-security/owasp-llm-top-10/overview/">OWASP LLM Top 10</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Агенты и интеграции</h4>
<ul>
<li><a href="/Product-security-playbook/ru/ai-security/agentic-ai/playbook/">Безопасность агентов</a></li>
<li><a href="/Product-security-playbook/ru/ai-security/mcp-security/playbook/">Безопасность MCP</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Разработка с ИИ</h4>
<ul>
<li><a href="/Product-security-playbook/ru/ai-security/ai-assisted-development/playbook/">Разработка с ИИ</a></li>
</ul>
</div>
</section>
<section class="site-map-card">
<h3><a href="/Product-security-playbook/ru/ai-automation/security-skills/overview/">Скиллы и инструменты</a></h3>
<div class="site-map-group">
<h4>Скиллы</h4>
<ul>
<li><a href="/Product-security-playbook/ru/ai-automation/security-skills/secure-development/overview/">Безопасная разработка</a></li>
<li><a href="/Product-security-playbook/ru/ai-automation/security-skills/security-review/overview/">Ревью безопасности</a></li>
<li><a href="/Product-security-playbook/ru/ai-automation/security-skills/sensitive-data-cleanup/overview/">Очистка чувствительных данных</a></li>
<li><a href="/Product-security-playbook/ru/ai-automation/security-skills/security-report-triage/overview/">Разбор отчетов безопасности</a></li>
<li><a href="/Product-security-playbook/ru/ai-automation/security-skills/security-fix-verification/overview/">Проверка исправлений</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Совместная работа скиллов</h4>
<ul>
<li><a href="/Product-security-playbook/ru/ai-automation/security-skills/workflow/overview/">Совместная работа скиллов</a></li>
</ul>
</div>
<div class="site-map-group">
<h4>Инструменты</h4>
<ul>
<li><a href="/Product-security-playbook/ru/ai-automation/prompt-integrity/overview/">prompt-integrity</a></li>
<li><a href="/Product-security-playbook/ru/ai-automation/model-security-eval/overview/">model-security-eval</a></li>
<li><a href="/Product-security-playbook/ru/ai-automation/prompt-guard/overview/">prompt-guard</a></li>
</ul>
</div>
</section>
<section class="site-map-card">
<h3>Справочник</h3>
<ul>
<li><a href="/Product-security-playbook/ru/reference/infrastructure-technologies/infrastructure-technologies/">Инфраструктурные технологии</a></li>
</ul>
</section>
</div>
</section>
