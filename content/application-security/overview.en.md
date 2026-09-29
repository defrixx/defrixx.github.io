# Application Security

Choose a playbook for the part of the application under review: code, APIs, business logic, sign-in, or the browser client. Use OWASP Top 10 to check review coverage.

| Task | Document | Review scope |
| --- | --- | --- |
| Review code | [Code review](./secure-coding/code-review/playbook.en.md) | Review changes and substantiate findings |
| Review an API | [API security](./api/api-security-patterns/playbook.en.md) | Controls at API boundaries |
| Review business logic | [Business logic security](./business-logic/business-logic-abuse/playbook.en.md) | Abuse of product workflows |
| Review sign-in and delegated access | [OIDC and OAuth](./identity/oidc-oauth/playbook.en.md) | OIDC and OAuth integrations |
| Review browser security | [Browser security](./web/browser-security/playbook.en.md) | Browser security mechanisms for web applications |
| Check coverage of web risks | [OWASP Top 10](./web/owasp-top-10/playbook.en.md) | OWASP Top 10 categories and corresponding checks |

## When to use other sections

For a system-wide assessment, start with [architecture review and threat modeling](../review/overview.en.md).
