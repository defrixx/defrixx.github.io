# Application Security

Choose a playbook for the part of the application under review: code, APIs, business logic, sign-in, or the browser client. Use OWASP Top 10 to check review coverage.

| Task | Document | Review scope |
| --- | --- | --- |
| Review code | [Code review](./secure-coding/code-review/playbook.en.md) | Input handling, interpreter boundaries, authorization, sessions, files, secrets, and dependencies in changed code. Includes checking whether sensitive operations are reachable and collecting evidence for review findings. |
| Review an API | [API security](./api/api-security-patterns/playbook.en.md) | REST, SOAP/XML, GraphQL, webhooks, and gRPC: authentication, object access, schema validation, request limits, and logging. Examines trust boundaries between clients, gateways, and internal services. |
| Review business logic | [Business logic security](./business-logic/business-logic-abuse/playbook.en.md) | Account takeover, signup and promotion abuse, tenant isolation, and authorization for business operations. Examines state transitions, request replay, idempotency, and abuse detection. |
| Review sign-in and delegated access | [OIDC and OAuth](./identity/oidc-oauth/playbook.en.md) | Sign-in and delegated access flows, redirects, PKCE, and validation of tokens, scopes, and audiences. Covers token lifecycle and trust boundaries between clients, authorization servers, and APIs. |
| Review browser security | [Browser security](./web/browser-security/playbook.en.md) | CSP, CORS, cookies, page embedding, and third-party scripts. Examines browser trust boundaries, frontend dependencies, and verification of effective headers and policies. |
| Check coverage of web risks | [OWASP Top 10](./web/owasp-top-10/playbook.en.md) | Access control, injection, cryptography, configuration, components, integrity, logging, and SSRF. Connects OWASP Top 10 categories to checks and failure signals for assessing review coverage. |

## How to combine documents

- For a PR review, start with code review, then select documents for the mechanisms affected: APIs, business logic, OIDC/OAuth, or browser security.
- For an API assessment, combine the API playbook with business logic review when the task involves action sequences or product rules.
- For a web application, add browser security to the relevant reviews. Use OWASP Top 10 to check which risk categories the assessment covers.

## When to use other sections

For a system-wide assessment, start with [architecture review and threat modeling](../review/overview.en.md).
