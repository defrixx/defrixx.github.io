# Browser and Frontend Security Playbook

## 1. Scope and Objective

This playbook defines a release review baseline for browser-facing applications: CSP, CORS, cookies, browser storage, third-party scripts, embedded content, and frontend supply-chain controls.

Use this document for:
- SPA, server-rendered web applications, BFF-backed browser flows, admin panels, and embedded widgets;
- release review of security headers, browser session handling, and third-party frontend dependencies;
- abuse-case testing where XSS, cross-origin exposure, session leakage, or third-party script compromise can affect users.

Out of scope:
- OAuth/OIDC flow design: use the [OIDC + OAuth 2.0 security guide](../../identity/oidc-oauth/playbook.en.md);
- API authorization and webhook controls: use the [API security playbook](../../api/api-security-patterns/playbook.en.md);
- general OWASP Top 10 coverage: use the [web application defense playbook](../owasp-top-10/playbook.en.md).

Objective:
- reduce account/session theft, browser-side data exposure, cross-origin data leakage, clickjacking, and third-party script compromise;
- make browser controls testable before release instead of treating headers as scanner-only hardening.

---

## 2. Threat Model

Assets:
- browser session cookies, CSRF tokens, OAuth/OIDC transient parameters, user profile data, admin UI actions, checkout/payment state, and tenant-scoped data rendered in the DOM.

Attackers and entry points:
- external attacker injecting script through stored/reflected/DOM XSS;
- malicious or compromised third-party script/CDN/tag manager;
- hostile origin attempting credentialed cross-origin reads;
- attacker embedding sensitive pages in frames;
- compromised browser extension or local malware, where browser controls only reduce but do not eliminate exposure.

High-impact scenarios:
- XSS steals non-HttpOnly tokens from `localStorage`, calls privileged APIs through the victim session, or modifies checkout/admin actions.
- CORS reflects arbitrary origins and allows credentialed reads from a victim browser session.
- A compromised analytics or tag-manager script reads sensitive DOM content, session-adjacent data, or payment fields.
- Clickjacking frames an admin or approval screen and tricks a user into a destructive action.
- A third-party CDN script changes after release and executes unexpected code because no integrity or ownership control exists.

---

## 3. Release-Ready Baseline

### 3.1 Content Security Policy

Release-ready defaults:
- Browser-facing applications define CSP in the `Content-Security-Policy` response header, not only in a `<meta>` tag.
- Start new applications with `default-src 'none'` and explicitly allow required classes: `script-src`, `style-src`, `img-src`, `font-src`, `connect-src`, `frame-ancestors`, `base-uri`, and `form-action`.
- Use `frame-ancestors 'none'` by default for admin, account, checkout, and internal tools. Use explicit origins only when embedding is a product requirement.
- Set `base-uri 'none'` unless the application intentionally uses `<base>`.
- Set `form-action 'self'` plus explicit payment/IdP endpoints where required.
- Avoid `unsafe-inline` and `unsafe-eval` for new code. If legacy code needs them, document owner, affected routes, expiry, and compensating controls.
- Use nonce- or hash-based script execution for applications that still require inline bootstrap scripts.
- Roll out material CSP changes through `Content-Security-Policy-Report-Only` first, then enforce after false positives are reviewed.

Verification:
- Confirm the effective header on every browser entry point, including error pages, login/callback pages, admin pages, and static shell routes.
- Run a representative user journey with CSP reporting enabled and review violations before enforcement.
- Negative test: injected inline script and unapproved external script must not execute in the enforced profile.

### 3.2 CORS and Cross-Origin Data Exposure

Release-ready defaults:
- Do not enable CORS globally. Configure it per route or API surface that needs browser cross-origin access.
- Credentialed CORS must use exact origin allowlists. Do not combine reflected arbitrary `Origin` with `Access-Control-Allow-Credentials: true`.
- Do not use `Access-Control-Allow-Origin: *` for responses containing user, tenant, internal, payment, or admin data.
- Treat `Origin` as a browser signal only. Non-browser clients can spoof it; server-side authentication and authorization remain mandatory.
- Restrict allowed methods and headers to the smallest operational set.
- Cache preflight responses only after the policy is stable; use conservative `Access-Control-Max-Age` for sensitive APIs.

Verification:
- Test allowed and denied origins with and without credentials.
- Test `null` origin, sibling subdomains, attacker-controlled subdomains, and HTTP origins against HTTPS APIs.
- Confirm sensitive responses do not include wildcard CORS headers.

### 3.3 Cookies, Browser Storage, and Session Data

Release-ready defaults:
- Session cookies use `HttpOnly`, `Secure`, and explicit `SameSite`.
- Use `SameSite=Lax` for normal browser sessions unless the flow requires cross-site POST/iframe behavior.
- Use `SameSite=Strict` for high-risk admin or step-up cookies where UX allows it.
- Use `SameSite=None; Secure` only for documented cross-site embed or federated flows.
- Scope `Domain` and `Path` narrowly. Do not share session cookies across unrelated subdomains.
- Do not store access tokens, refresh tokens, session IDs, or long-lived secrets in `localStorage`.
- Prefer BFF/session-cookie patterns for browser apps that need durable authentication. If an SPA must hold tokens, document the risk decision and keep token lifetime short per the OIDC/OAuth playbook.

Verification:
- Inspect `Set-Cookie` on login, refresh, step-up, logout, and error paths.
- Confirm session ID rotation after login and privilege changes.
- Negative test: JavaScript cannot read session cookies; stolen local browser state does not contain reusable refresh tokens.

### 3.4 Third-Party Scripts and Frontend Supply Chain

Release-ready defaults:
- Maintain an inventory of third-party scripts, owners, purpose, data touched, and approval date.
- Do not load tag-manager or analytics scripts on admin, checkout, identity, or sensitive data-entry pages unless there is explicit business approval and data minimization.
- Prefer self-hosting or pinned versions for critical frontend dependencies.
- Use SRI for static third-party scripts/styles where the provider and update model allow it.
- Require `crossorigin="anonymous"` for cross-origin SRI resources where needed by browser behavior.
- Review npm/package lockfile changes that affect frontend build, bundler plugins, minifiers, auth/session packages, and payment UI.
- Remove unused scripts and stale feature flags; frontend supply-chain risk accumulates through forgotten integrations.

Verification:
- Compare runtime-loaded scripts with the approved inventory.
- Validate SRI hashes for static CDN resources.
- Confirm sensitive DOM fields are not exposed to scripts that do not need them.

### 3.5 Embedded Content and Browser APIs

Release-ready defaults:
- Use `frame-ancestors` for anti-clickjacking. Keep `X-Frame-Options` only as compatibility defense where needed.
- Sandbox untrusted iframes and grant capabilities explicitly.
- For `postMessage`, always set a specific target origin and verify `event.origin` exactly on receive.
- Treat `postMessage` data as untrusted input; never evaluate it as code or write it to the DOM through unsafe sinks.
- Use explicit policy for clipboard, camera, microphone, geolocation, payment, and file APIs.
- Use `Permissions-Policy` to disable powerful browser features by default on admin, account, checkout, support, and internal-tool pages. Start from deny-by-default and open only the features required by the route:

```http
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), serial=(), bluetooth=(), clipboard-read=(), display-capture=(), fullscreen=(self)
```

- Feature exceptions require an owner, affected routes, allowed origins, business purpose, expiry or review date, and a negative test showing that unauthorized origins cannot use the feature. For example, checkout may allow `payment=(self)` only on payment routes; a video-verification flow may allow `camera=(self)` only for the verification origin and only while that feature exists.
- Do not grant browser capabilities through iframe `allow` attributes unless the parent page's `Permissions-Policy` also permits that feature for the embedded origin.

Verification:
- Attempt to frame sensitive pages from an untrusted origin.
- Test `postMessage` with attacker origins and malformed payloads.
- Review iframe `sandbox` and `allow` attributes for least privilege.
- Inspect the effective `Permissions-Policy` response header on sensitive routes with browser DevTools or an automated header check.
- Negative test: unapproved origins and unrelated routes cannot access camera, microphone, geolocation, payment, display capture, USB/serial/Bluetooth, or clipboard-read capabilities.
---

## 4. Related Materials

- [OIDC + OAuth 2.0 playbook](../../identity/oidc-oauth/playbook.en.md)
- [API security playbook](../../api/api-security-patterns/playbook.en.md)
- [OWASP Top 10 web application defense playbook](../owasp-top-10/playbook.en.md)
- [Secure coding and code review playbook](../../secure-coding/code-review/playbook.en.md)
- [Agentic AI security playbook](../../../ai-security/agentic-ai/playbook.en.md)
