---
template: splash
tableOfContents: false
prev: false
next: false
title: "Навыки и инструменты"
description: "Наши пять самостоятельных скиллов помогают ассистенту вести задачи безопасности; три Python-инструмента выполняют ограниченные локальные операции. Выберите задачу и ожидаемый ре..."
sidebar:
  order: 100
---
Наши пять самостоятельных скиллов помогают ассистенту вести задачи безопасности; три Python-инструмента выполняют ограниченные локальные операции. Выберите задачу и ожидаемый результат, затем откройте руководство выбранной ревизии.

<div class="hub-catalogue">
<section class="catalogue-group"><h2>Скиллы для ассистента</h2>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/ru/ai-automation/security-skills/secure-development/overview/">secure-development</a></h3>
<p>Писать или менять код</p></div>
<p class="catalogue-result">Применимые требования, реализация и проверки</p>
<details class="catalogue-details"><summary>Входные данные, запуск и версия</summary><dl>
<dt>Входные данные</dt><dd>Изменение, архитектура, границы доверия</dd>
<dt>Локальное выполнение</dt><dd>Ассистент в разрешенном локальном проекте</dd>
<dt>Ограничения</dt><dd>Выбирайте меры по архитектуре; изменение кода требует задания</dd>
<dt>Версия / источник</dt><dd>commit:55010b3f9484 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/skills/secure-development">Руководство этой ревизии</a></dd>
<dt>Лицензия</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/ru/ai-automation/security-skills/security-review/overview/">security-review</a></h3>
<p>Оценить PR или репозиторий</p></div>
<p class="catalogue-result">Замечания, гипотезы и приоритетные действия</p>
<details class="catalogue-details"><summary>Входные данные, запуск и версия</summary><dl>
<dt>Входные данные</dt><dd>Область и точные base/head либо ревизия проекта</dd>
<dt>Локальное выполнение</dt><dd>Ассистент; необязательный скрипт Python 3.9+ и Git</dd>
<dt>Ограничения</dt><dd>Оценка сама по себе не меняет код</dd>
<dt>Версия / источник</dt><dd>commit:55010b3f9484 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/skills/security-review">Руководство этой ревизии</a></dd>
<dt>Лицензия</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/ru/ai-automation/security-skills/sensitive-data-cleanup/overview/">sensitive-data-cleanup</a></h3>
<p>Подготовить материалы к передаче</p></div>
<p class="catalogue-result">Отдельная очищенная копия и обезличенный реестр</p>
<details class="catalogue-details"><summary>Входные данные, запуск и версия</summary><dl>
<dt>Входные данные</dt><dd>Согласованный каталог, режим и политика</dd>
<dt>Локальное выполнение</dt><dd>Ассистент; скрипт Python 3.9+, POSIX</dd>
<dt>Ограничения</dt><dd>Текст UTF-8/JSON/JSONL/CSV; у JPEG/PNG только метаданные; оригиналы сохраняются</dd>
<dt>Версия / источник</dt><dd>commit:55010b3f9484 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/skills/sensitive-data-cleanup">Руководство этой ревизии</a></dd>
<dt>Лицензия</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/ru/ai-automation/security-skills/security-report-triage/overview/">security-report-triage</a></h3>
<p>Разобрать сигналы сканера</p></div>
<p class="catalogue-result">Учтенные сигналы и очередь действий</p>
<details class="catalogue-details"><summary>Входные данные, запуск и версия</summary><dl>
<dt>Входные данные</dt><dd>Происхождение отчета, ревизия цели и область</dd>
<dt>Локальное выполнение</dt><dd>Ассистент; ограниченный SARIF скрипт Python 3.9+, POSIX</dd>
<dt>Ограничения</dt><dd>Нормализация учитывает сигналы; для вывода нужен контекст</dd>
<dt>Версия / источник</dt><dd>commit:55010b3f9484 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/skills/security-report-triage">Руководство этой ревизии</a></dd>
<dt>Лицензия</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/ru/ai-automation/security-skills/security-fix-verification/overview/">security-fix-verification</a></h3>
<p>Перепроверить выбранное исправление</p></div>
<p class="catalogue-result">Вердикт по замечанию, штатные и обходные случаи</p>
<details class="catalogue-details"><summary>Входные данные, запуск и версия</summary><dl>
<dt>Входные данные</dt><dd>ID замечания, исходные данные и ревизия исправления</dd>
<dt>Локальное выполнение</dt><dd>Ассистент в выбранной локальной области</dd>
<dt>Ограничения</dt><dd>Разделяйте историю оценки и текущий итог проверки</dd>
<dt>Версия / источник</dt><dd>commit:55010b3f9484 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/skills/security-fix-verification">Руководство этой ревизии</a></dd>
<dt>Лицензия</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
</section>
<section class="catalogue-group"><h2>Локальные инструменты</h2>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/ru/ai-automation/prompt-integrity/overview/">prompt-integrity</a></h3>
<p>Проверить статические инструкции перед отправкой</p></div>
<p class="catalogue-result">Блокировка несовпадения либо отправка проверенного снимка</p>
<details class="catalogue-details"><summary>Входные данные, запуск и версия</summary><dl>
<dt>Входные данные</dt><dd>Защищенный эталон и запрос приложения</dd>
<dt>Локальное выполнение</dt><dd>Python 3.11+, POSIX; CLI/библиотека</dd>
<dt>Ограничения</dt><dd>Ограниченные адаптеры Ollama/LM Studio; охватите все пути отправки</dd>
<dt>Версия / источник</dt><dd>0.1.0 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/tools/prompt-integrity">Руководство этой ревизии</a></dd>
<dt>Лицензия</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/ru/ai-automation/prompt-guard/overview/">prompt-guard</a></h3>
<p>Проверить входной контекст и ответ модели</p></div>
<p class="catalogue-result">allow/block/review/error; явно разрешенная очищенная копия</p>
<details class="catalogue-details"><summary>Входные данные, запуск и версия</summary><dl>
<dt>Входные данные</dt><dd>Текст UTF-8/JSON, доверенный источник и политика</dd>
<dt>Локальное выполнение</dt><dd>Python 3.11+, POSIX; CLI/библиотека</dd>
<dt>Ограничения</dt><dd>Лексические правила дают ложные блокировки; полномочия на действия проверяются отдельно</dd>
<dt>Версия / источник</dt><dd>0.3.0 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/tools/prompt-guard">Руководство этой ревизии</a></dd>
<dt>Лицензия</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/ru/ai-automation/model-security-eval/overview/">model-security-eval</a></h3>
<p>Проверить регрессии безопасности локальной модели</p></div>
<p class="catalogue-result">Вердикт CI, события и локальные закрытые результаты</p>
<details class="catalogue-details"><summary>Входные данные, запуск и версия</summary><dl>
<dt>Входные данные</dt><dd>Локальная модель, синтетический профиль и бюджеты</dd>
<dt>Локальное выполнение</dt><dd>Python 3.11+ и локальная конечная точка LM Studio/Ollama</dd>
<dt>Ограничения</dt><dd>Фиксированные сценарии и виртуальные действия; лимиты могут дать неопределенный итог</dd>
<dt>Версия / источник</dt><dd>0.4.0 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/tools/model-security-eval">Руководство этой ревизии</a></dd>
<dt>Лицензия</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
</section>
</div>

## Версии и выполнение

Каталог закрепляет публичные пути Product-security-skills за одной ревизией. Это реестр ссылок, без автоматического скачивания или запуска. В каждом пункте доступны руководство этой ревизии и связанный плейбук. Установка и обработка данных выполняются в выбранном пользователем локальном окружении.

Для скиллов версия означает SHA всего пакета, а не номер Python-пакета. При копировании сохраняйте весь каталог скилла и корневое уведомление MIT из исходного репозитория. Соседние скиллы не обязательны. Версии инструментов указаны в метаданных пакетов; наличие номера не означает публикацию в PyPI.
