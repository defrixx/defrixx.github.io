---
title: "Безопасность платформы"
description: "Для общей проверки Kubernetes начните с ревью кластера, затем перейдите к отдельным механизмам защиты. Управление секретами в Vault описано в отдельном плейбуке."
sidebar:
  order: 5
---
Для общей проверки Kubernetes начните с ревью кластера, затем перейдите к отдельным механизмам защиты. Управление секретами в Vault описано в отдельном плейбуке.

| Задача | Документ | Охват проверки |
| --- | --- | --- |
| Проверить кластер Kubernetes | [Ревью кластера](/Product-security-playbook/ru/platform-security/kubernetes/cluster-security-review/playbook/) | Общая проверка кластера |
| Проверить настройки Pod | [Безопасность Pod](/Product-security-playbook/ru/platform-security/kubernetes/pod-security/playbook/) | Параметры безопасности рабочих нагрузок |
| Проверить секреты Kubernetes | [Секреты Kubernetes](/Product-security-playbook/ru/platform-security/kubernetes/secrets/playbook/) | Работа с секретами в кластере |
| Проверить seccomp | [Проверка seccomp](/Product-security-playbook/ru/platform-security/kubernetes/seccomp/checklist/) | Профили системных вызовов |
| Разобрать выход из контейнера | [Выход из контейнера и capabilities](/Product-security-playbook/ru/platform-security/kubernetes/container-escape-capability-abuse/overview/) | Сценарии выхода из контейнера и злоупотребления привилегиями Linux (capabilities) |
| Проверить защиту от атак | [Проверка защиты от атак](/Product-security-playbook/ru/platform-security/kubernetes/adversarial-validation/playbook/) | Практическая проверка мер защиты Kubernetes |
| Проверить Vault | [Секреты в Vault](/Product-security-playbook/ru/platform-security/secrets/vault/playbook/) | Управление секретами через Vault |

## Как выбрать глубину проверки

- Для незнакомого кластера начните с общего ревью Kubernetes. Затем используйте документы по Pod, секретам и seccomp для подробной проверки соответствующих настроек.
- Для изменения одного механизма можно сразу открыть профильный документ. Обзор выхода из контейнера поможет связать настройки с рассматриваемыми сценариями атак.
- Для практической проверки уже настроенной защиты перейдите к проверке сценариями атак и следуйте условиям проведения, указанным в плейбуке.
- Если задача касается Vault, начните с его плейбука. Документ по секретам Kubernetes дополнит его, когда проверка затрагивает и хранение секретов в кластере.

## Когда нужны другие разделы

Для проверки происхождения сборок и безопасности контейнерных образов перейдите в раздел [цепочки поставки](/Product-security-playbook/ru/supply-chain/overview/).
