# Безопасность платформы

Для общей проверки Kubernetes начните с ревью кластера, затем перейдите к отдельным механизмам защиты. Управление секретами в Vault описано в отдельном плейбуке.

| Задача | Документ | Охват проверки |
| --- | --- | --- |
| Проверить кластер Kubernetes | [Ревью кластера](./kubernetes/cluster-security-review/playbook.ru.md) | Общая проверка кластера |
| Проверить настройки Pod | [Безопасность Pod](./kubernetes/pod-security/playbook.ru.md) | Параметры безопасности рабочих нагрузок |
| Проверить секреты Kubernetes | [Секреты Kubernetes](./kubernetes/secrets/playbook.ru.md) | Работа с секретами в кластере |
| Проверить seccomp | [Проверка seccomp](./kubernetes/seccomp/checklist.ru.md) | Профили системных вызовов |
| Разобрать выход из контейнера | [Выход из контейнера и capabilities](./kubernetes/container-escape-capability-abuse/overview.ru.md) | Сценарии выхода из контейнера и злоупотребления привилегиями Linux (capabilities) |
| Проверить защиту от атак | [Проверка защиты от атак](./kubernetes/adversarial-validation/playbook.ru.md) | Практическая проверка мер защиты Kubernetes |
| Проверить Vault | [Секреты в Vault](./secrets/vault/playbook.ru.md) | Управление секретами через Vault |

## Когда нужны другие разделы

Для проверки происхождения сборок и безопасности контейнерных образов перейдите в раздел [цепочки поставки](../supply-chain/overview.ru.md).
