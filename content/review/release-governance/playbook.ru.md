# Плейбук управления релизами и security quality gates

## 1. Область и цель

Этот плейбук задает слой контроля релизов вокруг CI/CD: security quality gates, protected environments, deployment approvals, релизные подтверждения, обработку исключений и эскалацию.

Используйте документ для:
- production-релизов и high-risk staging-релизов;
- GitLab, GitHub Actions, Argo CD, Jenkins или похожих delivery systems;
- сервисы, container images, infrastructure changes, Kubernetes manifests и security-sensitive configuration.

Вне области:
- детальная реализация SLSA provenance: используйте [SLSA provenance overview](../../supply-chain/slsa-provenance/overview.ru.md);
- Kubernetes cluster admission и RBAC review: используйте [Kubernetes cluster security review playbook](../../platform-security/kubernetes/cluster-security-review/playbook.ru.md);
- architecture threat modeling: используйте [Threat Modeling Playbook](../threat-modeling/playbook.ru.md).

Цель:
- отделить право merge code от права deploy risk;
- сделать решения по релизам основанными на подтверждениях и повторяемыми;
- не допускать silent production deployment при high-risk замечаниях, непроверенных артефактах, неутвержденных исключениях и unauthorized deployment paths.

---

## 2. Версионные допущения и источники

| Область | Допущение | Источник | Проверено |
|---|---|---|---|
| Secure SDLC | NIST SSDF SP 800-218 v1.1 имеет финальный статус и задает high-level secure software development practices | NIST SP 800-218 | 2026-05-06 |
| Provenance | SLSA v1.2 утверждена; Build L2/L3 требуют более сильного provenance и build-platform trust, чем L1 | SLSA v1.2 | 2026-05-06 |
| GitLab environments | Protected environments и deployment approvals доступны в GitLab Premium/Ultimate tiers; точное поведение зависит от GitLab version и tier | GitLab protected environments и deployment approvals docs | 2026-05-06 |
| GitHub environments | GitHub environments поддерживают protection rules, required reviewers, wait timers, environment secrets и deployment branch restrictions; availability зависит от plan и repository visibility | GitHub deployments and environments docs | 2026-05-06 |

---

## 3. Модель угроз

Активы:
- production deployment authority, релизные артефакты, provenance/attestations, environment secrets, CI/CD runners, approval records, решения по исключениям, audit logs и customer-impacting production state.

Атакующие и точки входа:
- compromised developer или maintainer account;
- malicious или compromised CI job, runner, reusable workflow, plugin или build dependency;
- insider, обходящий security checks через manual deployment или environment permission drift;
- атакующий, подменяющий артефакты между build и deploy;
- delivery pressure, превращающий исключения в undocumented release debt.

High-impact сценарии:
- Один человек может писать код, менять pipeline, approve deployment и deploy to production без independent review.
- Production deploy использует mutable tag или артефакт, который не был создан trusted release workflow.
- Critical-замечание сканера подавлено без owner, expiry, compensating control или подтверждений.
- Untrusted fork или branch получает доступ к signing, deployment или environment secrets.
- Emergency release обходит normal gates и не оставляет следов post-release review.

---

## 4. Модель контроля релизов

### 4.1 Классы релизов

| Класс релиза | Примеры | Минимальный набор gate |
|---|---|---|
| Low-risk internal | Internal tool, no sensitive data, bounded blast radius | CI checks pass, owner approval, подтверждения сохранены |
| Standard production | Customer-facing service, normal API или UI release | Security gates, protected environment, deployment approval, artifact immutability |
| High-risk production | Auth, payment, tenant isolation, admin, secrets, platform, CI/CD, Kubernetes control plane | Independent security approval, stricter gates, rollback plan, пакет релизных подтверждений |
| Emergency | Incident fix, urgent production restoration | Expedited approval, narrow scope, mandatory post-release review within `2 business days` |

Production recommendation:
- Для каждого repository или deployable service задается default-класс релиза.
- Change может повысить класс конкретного релиза, если затрагивает auth, tenant isolation, payment, secrets, CI/CD, IaC, Kubernetes policy или privileged admin paths.

### 4.2 Separation of duties

Production-настройки:
- Protected production environments должны быть доступны для deploy только dedicated CD identities или явно authorized release roles.
- Human direct production deployment допускается только как break-glass.
- Один человек не должен быть sole author, sole approver и sole deploy approver для high-risk production-релиза.
- Изменения pipeline definitions, reusable workflows, deployment manifests, IaC modules, signing configuration и environment protection rules требуют review by owners из CODEOWNERS или эквивалентной политики.

Верификация:
- Получите список users/groups/service accounts, которым разрешен deploy to production.
- Подтвердите, что environment secrets доступны только jobs, ссылающимся на protected environments после прохождения required rules.
- Проверьте audit events для изменений protected environment rules и deployment approvals.

---

## 5. Security quality gates

### 5.1 Gate types

| Gate | Назначение | Блокирующее поведение по умолчанию |
|---|---|---|
| Source governance | Protected branch/tag, required review, CODEOWNERS for high-risk paths | Block direct production-source changes |
| SAST/secret scan | Prevent obvious code and secret issues before release | Block new Critical/High confirmed issues and live secrets |
| SCA/SBOM | Detect vulnerable dependencies and maintain release inventory | Block exploitable Critical/High без исключения |
| IaC/container scan | Catch unsafe infrastructure, image, and runtime settings | Block Critical/High in production deploy path |
| Artifact signing/provenance | Prove artifact came from expected builder/source/workflow | Block unsigned/unverified артефакты там, где проверка обязательна |
| DAST/API tests | Validate deployed test/staging surface and auth/session behavior | Block confirmed Critical/High issues, reachable в целевом окружении |
| Manual approval | Record release readiness and risk acceptance | Required for standard and high-risk production |

Production-настройки:
- Gates применяются к изменениям, а не только ко всему repository. Не блокируйте релиз только из-за unrelated legacy debt, если политика не говорит, что legacy debt превысил порог релиза.
- Новые Critical-замечания блокируют релиз, если нет valid Critical exception.
- Новые High-замечания по умолчанию блокируют high-risk production-релизы; standard production может идти дальше только с owner, due date, компенсирующими мерами и explicit acceptance.
- Замечания по live secret блокируют релиз до revoke/rotation секрета и оценки exposure.
- Scanner output должен быть разобран как confirmed issue, false positive, accepted risk или backlog debt. Raw unreviewed reports сами по себе не считаются релизным подтверждением.

### 5.2 Gate aggregation

Production-настройки:
- Решение по релизу использует один aggregated status, а не набор разрозненных scanner dashboards.
- Aggregated status фиксирует: gate name, tool/source, commit/artifact digest, result, ID замечаний, exception IDs, approver, timestamp и ссылку на подтверждения.
- Failed non-security quality gate может блокировать deployment, но security exceptions должны оставаться видимыми и отдельно утвержденными.

Верификация:
- Восстановите решение по релизу из logs и артефактов после deployment.
- Подтвердите, что digest развернутого артефакта совпадает с digest артефакта, прошедшего gate.

---

## 6. Protected environments и deployment approvals

Production-настройки:
- `production` должен быть protected environment.
- `staging` protected, если содержит production-like data, secrets, network reachability или роль release-signoff.
- Deployment authority должна быть уже, чем merge authority.
- Approval rules environment-specific: production, regulated, platform и break-glass environments могут требовать разные группы approver'ов.
- Self-approval disabled для high-risk production, если он явно не justified organization policy и не компенсирован post-deploy review.
- Deployment approvals включают краткую причину или ссылку на релиз, а не только button click.

GitLab-specific notes:
- Protected environments ограничивают, кто может deploy to named environments.
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

## 7. Релизные подтверждения

Минимальный пакет подтверждений для standard production:
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

Дополнительные подтверждения для high-risk production:
- threat model или abuse-case update;
- negative tests для auth, tenant isolation, payment/ledger, admin или secrets path, touched by the change;
- rollback/kill-switch plan;
- monitoring и alert confirmation для changed sensitive flow;
- explicit security owner approval.

Retention:
- Храните релизные подтверждения минимум `1 year` для production или дольше, если это требуют regulatory, customer, audit или incident-response requirements.

---

## 8. Exceptions и escalation

Exception record должен включать:
- ID замечания или gate;
- affected service/release;
- risk statement и business reason;
- компенсирующие меры;
- owner и approver;
- expiry date;
- условие проверки для закрытия.

Production-настройки:
- Critical-замечания по умолчанию отклоняются. Critical exception действителен только при approval security leadership и business/product owner, явном TTL, компенсирующих мерах и обязательном post-release review.
- High exceptions требуют approval service owner и security owner.
- Exceptions без expiry недействительны.
- Expired exceptions автоматически проваливают следующий release gate, если не продлены через ревью.
- Emergency bypass требует post-release review within `2 business days`: что было обойдено, причина, impact и план устранения.

Escalation triggers:
- релиз заблокирован из-за Critical without accepted risk;
- disputed severity или business impact;
- repeated exception renewal;
- отсутствует owner для production-замечания;
- подтверждения не доказывают, какой артефакт был развернут.