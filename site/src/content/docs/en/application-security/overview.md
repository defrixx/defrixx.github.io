---
title: "Application Security"
description: "Choose a playbook for the part of the application under review: code, APIs, business logic, sign-in, or the browser client. Use OWASP Top 10 to check review coverage."
sidebar:
  order: 5
---
Choose a playbook for the part of the application under review: code, APIs, business logic, sign-in, or the browser client. Use OWASP Top 10 to check review coverage.

| Task | Document | Review scope |
| --- | --- | --- |
| Review code | [Code review](/Product-security-playbook/en/application-security/secure-coding/code-review/playbook/) | Input handling, interpreter boundaries, authorization, sessions, files, secrets, and dependencies in changed code. Includes checking whether sensitive operations are reachable and collecting evidence for review findings. |
| Review an API | [API security](/Product-security-playbook/en/application-security/api/api-security-patterns/playbook/) | REST, SOAP/XML, GraphQL, webhooks, and gRPC: authentication, object access, schema validation, request limits, and logging. Examines trust boundaries between clients, gateways, and internal services. |
| Review business logic | [Business logic security](/Product-security-playbook/en/application-security/business-logic/business-logic-abuse/playbook/) | Account takeover, signup and promotion abuse, tenant isolation, and authorization for business operations. Examines state transitions, request replay, idempotency, and abuse detection. |
| Review sign-in and delegated access | [OIDC and OAuth](/Product-security-playbook/en/application-security/identity/oidc-oauth/playbook/) | Sign-in and delegated access flows, redirects, PKCE, and validation of tokens, scopes, and audiences. Covers token lifecycle and trust boundaries between clients, authorization servers, and APIs. |
| Review browser security | [Browser security](/Product-security-playbook/en/application-security/web/browser-security/playbook/) | CSP, CORS, cookies, page embedding, and third-party scripts. Examines browser trust boundaries, frontend dependencies, and verification of effective headers and policies. |
| Check coverage of web risks | [OWASP Top 10](/Product-security-playbook/en/application-security/web/owasp-top-10/playbook/) | Access control, injection, cryptography, configuration, components, integrity, logging, and SSRF. Connects OWASP Top 10 categories to checks and failure signals for assessing review coverage. |

## How to combine documents

- For a PR review, start with code review, then select documents for the mechanisms affected: APIs, business logic, OIDC/OAuth, or browser security.
- For an API assessment, combine the API playbook with business logic review when the task involves action sequences or product rules.
- For a web application, add browser security to the relevant reviews. Use OWASP Top 10 to check which risk categories the assessment covers.

## When to use other sections

For a system-wide assessment, start with [architecture review and threat modeling](/Product-security-playbook/en/review/overview/).
