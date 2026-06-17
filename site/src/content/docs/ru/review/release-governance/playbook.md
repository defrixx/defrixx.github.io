---
title: "Плейбук управления релизами и security quality gates"
description: "Этот плейбук задает слой контроля релизов вокруг CI/CD: security quality gates, protected environments, deployment approvals, релизные подтверждения, обработку исключений и эска..."
sidebar:
  order: 30
---
## 1. Область и цель

Этот плейбук задает слой контроля релизов вокруг CI/CD: security quality gates, protected environments, deployment approvals, релизные подтверждения, обработку исключений и эскалацию.

Используйте документ для:
- релизов в рабочую среду и high-risk staging-релизов;
- GitLab, GitHub Actions, Argo CD, Jenkins или похожих delivery systems;
- сервисы, container images, infrastructure changes, Kubernetes manifests и security-sensitive configuration.

Вне области:
- детальный разбор уязвимостей, exploitability, SLA и lifecycle исключений: используйте [плейбук управления уязвимостями](/Product-security-playbook/ru/review/vulnerability-management/playbook/);
- детальная реализация SLSA provenance: используйте [SLSA provenance overview](/Product-security-playbook/ru/supply-chain/slsa-provenance/overview/);
- Kubernetes cluster admission и RBAC review: используйте [Kubernetes cluster security review playbook](/Product-security-playbook/ru/platform-security/kubernetes/cluster-security-review/playbook/);
- architecture threat modeling: используйте [Threat Modeling Playbook](/Product-security-playbook/ru/review/threat-modeling/playbook/).

Цель:
- отделить право merge code от права развертывать риск;
- сделать решения по релизам основанными на подтверждениях и повторяемыми;
- не допускать тихое развертывание в рабочую среду при high-risk замечаниях, непроверенных артефактах, неутвержденных исключениях и несанкционированных deployment paths.

---

## 2. Модель угроз

Активы:
- право развертывания в рабочую среду, релизные артефакты, provenance/attestations, environment secrets, CI/CD runners, approval records, решения по исключениям, audit logs и customer-impacting состояние рабочей среды.

Атакующие и точки входа:
- compromised developer или maintainer account;
- malicious или compromised CI job, runner, reusable workflow, plugin или build dependency;
- insider, обходящий security checks через manual deployment или environment permission drift;
- атакующий, подменяющий артефакты между build и deploy;
- delivery pressure, превращающий исключения в undocumented release debt.

High-impact сценарии:
- Один человек может писать код, менять pipeline, approve deployment и deploy в рабочую среду без independent review.
- Развертывание в рабочую среду использует mutable tag или артефакт, который не был создан trusted release workflow.
- Critical-замечание сканера подавлено без owner, expiry, compensating control или подтверждений.
- Untrusted fork или branch получает доступ к signing, deployment или environment secrets.
- Untrusted pull request, issue, comment, branch name, tag name или release note text интерполируется в privileged workflow step и приводит к command/script injection.
- Emergency release обходит normal gates и не оставляет следов post-release review.

---

## 3. Модель контроля релизов

### 3.1 Классы релизов

| Класс релиза | Примеры | Минимальный набор gate |
|---|---|---|
| Low-risk internal | Internal tool, no sensitive data, bounded blast radius | CI checks pass, owner approval, подтверждения сохранены |
| Standard live release | Customer-facing service, normal API или UI release | Security gates, protected environment, deployment approval, artifact immutability |
| High-risk live release | Auth, payment, tenant isolation, admin, secrets, platform, CI/CD, Kubernetes control plane | Independent security approval, stricter gates, rollback plan, пакет релизных подтверждений |
| Emergency | Incident fix, срочное восстановление рабочей среды, patch для KEV/public exploit, response при broken embargo | Expedited approval, narrow scope, с сохранением подтверждений, mandatory post-release review within `2 business days` |

Recommended control:
- Для каждого repository или deployable service задается default-класс релиза.
- Change может повысить класс конкретного релиза, если затрагивает auth, tenant isolation, payment, secrets, CI/CD, IaC, Kubernetes policy или privileged admin paths.

### 3.2 Separation of duties

Рабочие настройки:
- Protected рабочие среды должны быть доступны для deploy только dedicated CD identities или явно authorized release roles.
- Direct human deployment допускается только как break-glass.
- Один человек не должен быть sole author, sole approver и sole deploy approver для high-risk релиза в рабочую среду.
- Изменения pipeline definitions, reusable workflows, deployment manifests, IaC modules, signing configuration и environment protection rules требуют review by owners из CODEOWNERS или эквивалентной политики.
- Build, sign, publish и deploy jobs используют отдельные identities и permissions. Build job может публиковать unsigned candidate artifact, но не должен одновременно иметь unrestricted production deploy или signing authority, если workflow явно не прошел review как trusted release builder.

Верификация:
- Получите список users/groups/service accounts, которым разрешен deploy в рабочую среду.
- Подтвердите, что environment secrets доступны только jobs, ссылающимся на protected environments после прохождения required rules.
- Проверьте audit events для изменений protected environment rules и deployment approvals.

### 3.3 Hardening CI/CD execution plane

Рабочие настройки:
- Default workflow token permission — read-only; write permissions, `id-token: write`, package publish, signing и deployment permissions выдаются только jobs, которым они нужны.
- OIDC federation для CI/CD привязывает trust policy к issuer, audience, repository или immutable repository ID там, где это доступно, protected ref или environment, workflow identity и ожидаемому trigger. Wildcard trust на organization, project или branch prefix недопустим для развертывания в рабочую среду.
- Untrusted forks, external pull requests, issues, comments, branch names, tag names, release notes и commit messages считаются attacker-controlled input. Их нельзя напрямую интерполировать в shell, deployment manifests, prompts или release commands.
- Third-party actions, reusable workflows, plugins и pipeline images закреплены на immutable versions или digests для release workflows; широкие floating tags допустимы только в non-release experimentation.
- Self-hosted runners разделяются по trust tier. Untrusted code не должен выполняться на persistent runners с network access к live environments, artifact signing, production secrets или deployment credentials.
- Release runners должны быть ephemeral или очищаться по задокументированному standard; caches должны быть scoped по trust boundary и считаться untrusted build input.

Верификация:
- Проверьте workflow definitions на минимальные `permissions`, pinned dependencies, использование protected environments и прямую shell interpolation для untrusted context.
- Запустите fork/feature-branch workflow и подтвердите, что он не получает environment secrets, OIDC cloud roles, signing material или deployment jobs.
- Подтвердите, что runner groups/labels не позволяют untrusted jobs попадать на release или production-connected self-hosted runners.

---

## 4. Security quality gates

### 4.1 Gate types

| Gate | Назначение | Блокирующее поведение по умолчанию |
|---|---|---|
| Source governance | Protected branch/tag, required review, CODEOWNERS for high-risk paths | Block direct релизных source changes |
| SAST/secret scan | Prevent obvious code and secret issues before release | Block new Critical/High confirmed issues and live secrets |
| SCA/SBOM | Detect vulnerable dependencies and maintain release inventory | Block exploitable Critical/High без исключения |
| IaC/container scan | Catch unsafe infrastructure, image, and runtime settings | Block Critical/High в пути релизного развертывания |
| Artifact signing/provenance | Prove artifact came from expected builder/source/workflow | Block unsigned/unverified артефакты там, где проверка обязательна |
| DAST/API tests | Validate deployed test/staging surface and auth/session behavior | Block confirmed Critical/High issues, reachable в целевом окружении |
| Manual approval | Record release readiness and risk acceptance | Required for standard and high-risk live releases |

Рабочие настройки:
- Gates применяются к изменениям, а не только ко всему repository. Не блокируйте релиз только из-за unrelated legacy debt, если политика не говорит, что legacy debt превысил порог релиза.
- Новые Critical-замечания блокируют релиз, если нет действительного Critical-исключения.
- Новые High-замечания по умолчанию блокируют high-risk релизы в защищенные среды; standard live release может идти дальше только с owner, due date, компенсирующими мерами и explicit acceptance.
- KEV, достоверный public exploit, active exploitation, broken embargo или срочный vendor security patch могут быть основанием для emergency release approval для узкого remediation change. Даже для такого release нужны artifact identity, approver, ссылка на rollback/mitigation и подтверждения post-release review.
- Замечания по live secret блокируют релиз до revoke/rotation секрета и оценки exposure.
- Scanner output должен быть разобран как confirmed issue, false positive, accepted risk или backlog debt. Raw unreviewed reports сами по себе не считаются релизным подтверждением.

### 4.2 Gate aggregation

Рабочие настройки:
- Решение по релизу использует один aggregated status, а не набор разрозненных scanner dashboards.
- Aggregated status фиксирует: gate name, tool/source, commit/artifact digest, result, ID замечаний, ID исключений, approver, timestamp и ссылку на подтверждения.
- Failed non-security quality gate может блокировать deployment, но security-исключения должны оставаться видимыми и отдельно утвержденными.

Верификация:
- Восстановите решение по релизу из logs и артефактов после deployment.
- Подтвердите, что digest развернутого артефакта совпадает с digest артефакта, прошедшего gate.

---

## 5. Protected environments и deployment approvals

Рабочие настройки:
- `prod` должен быть protected environment.
- `staging` protected, если содержит похожих на рабочие data, secrets, network reachability или роль release-signoff.
- Deployment authority должна быть уже, чем merge authority.
- Approval rules зависят от environment: `prod`, regulated, platform и break-glass environments могут требовать разные группы approver'ов.
- Self-approval отключен для high-risk релиза в рабочую среду, если он явно не обоснован organization policy и не компенсирован post-deploy review.
- Deployment approvals включают краткую причину или ссылку на релиз, а не только button click.

GitLab-specific notes:
- Protected environments ограничивают, кто может deploy в named environments.
- Deployment approvals могут блокировать deployments до получения required approvals.
- Перед тем как полагаться на deployment approval features, проверяйте tier/version behavior.

GitHub-specific notes:
- Environments могут требовать protection rules до запуска job или доступа к environment secrets.
- Required reviewers, branch restrictions, wait timers и custom protection rules могут выражать релизную политику.
- Проверяйте plan и repository visibility, потому что feature availability отличается.

Верификация:
- Попробуйте deployment от unauthorized user/branch и подтвердите отказ.
- Подтвердите, что environment secrets недоступны до прохождения protection rules.
- Проверьте audit logs для approval, rejection и environment-rule changes.

---

## 6. Релизные подтверждения

Минимальный пакет подтверждений для standard live release:
- release ID, service, owner, environment, класс релиза;
- source repository, protected ref, commit SHA и reviewed PR/MR;
- имя артефакта и immutable digest;
- CI/CD pipeline ID и runner/build identity;
- результаты gate и scanner versions/configs там, где это релевантно;
- SBOM или dependency inventory там, где это требуется;
- provenance/signature verification result там, где это требуется;
- deployment approval record;
- открытые замечания и утвержденные исключения;
- rollback или ссылка на задачу устранения для high-risk changes.

Дополнительные подтверждения для high-risk релиза в рабочую среду:
- threat model или abuse-case update;
- negative tests для auth, tenant isolation, payment/ledger, admin или secrets path, touched by the change;
- для AI/agentic workflows: запись AI asset inventory, матрица политик, подтверждение action trace, подтверждения tool/MCP registry и kill-switch/rollback drill там, где это применимо;
- rollback/kill-switch plan;
- monitoring и alert confirmation для changed sensitive flow;
- explicit security owner approval.

Retention:
- Храните релизные подтверждения минимум `1 year` для рабочих сред или дольше, если это требуют regulatory, customer, audit или incident-response requirements.

---

## 7. Exceptions и escalation

Exception record должен включать:
- ID замечания или gate;
- affected service/release;
- risk statement и business reason;
- компенсирующие меры;
- owner и approver;
- expiry date;
- условие проверки для закрытия.

Рабочие настройки:
- Critical-замечания по умолчанию отклоняются. Critical-исключение действительно только при approval security leadership и business/product owner, явном TTL, компенсирующих мерах и обязательном post-release review.
- High-исключения требуют approval service owner и security owner.
- Exceptions без expiry недействительны.
- Истекшие исключения автоматически проваливают следующий release gate, если не продлены через ревью.
- Emergency bypass требует post-release review в течение `2 business days`: что обошли, причина, impact, deployed artifact, residual findings и план устранения.

Escalation triggers:
- релиз заблокирован из-за Critical without accepted risk;
- disputed severity или business impact;
- повторное продление исключения;
- отсутствует owner для замечания для рабочей среды;
- подтверждения не доказывают, какой артефакт был развернут.

---

## 8. Связанные материалы

- [Плейбук управления уязвимостями](/Product-security-playbook/ru/review/vulnerability-management/playbook/)
- [Чеклист ревью архитектуры безопасности](/Product-security-playbook/ru/review/architecture/checklist/)
- [Обзор безопасности AI](/Product-security-playbook/ru/ai-security/securing-ai/overview/)
- [Плейбук безопасности Agentic AI](/Product-security-playbook/ru/ai-security/agentic-ai/playbook/)
- [Плейбук безопасности MCP](/Product-security-playbook/ru/ai-security/mcp-security/playbook/)
- [Плейбук безопасности container images](/Product-security-playbook/ru/supply-chain/container-image-security/playbook/)
- [Плейбук ревью безопасности Kubernetes-кластера](/Product-security-playbook/ru/platform-security/kubernetes/cluster-security-review/playbook/)
