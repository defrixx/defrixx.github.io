# Product Security Hub

A practical Product Security knowledge base and local toolset for reviewing designs, developing security controls, and verifying fixes. The playbooks connect security engineering guidance with reusable skills, tools, and the SDD Security Analyzer.

## Start here

- [Explore the knowledge base](https://defrixx.github.io/) or browse the [English](content/hub/knowledge/overview.en.md) and [Russian](content/hub/knowledge/overview.ru.md) library.
- [See a complete synthetic review](content/hub/reviews/delivery-api/overview.en.md) of a delivery integration, from architecture to proposed repairs and checks.
- [Run SDD Security Analyzer](analyzer/README.md) locally to review Markdown specifications against selected requirements.

## Example: reviewing an integration

An order service connects several tenants to a delivery provider. The [case](content/hub/reviews/delivery-api/overview.en.md) maps the trust boundaries, OAuth lifecycle and webhook flows, then turns them into requirements and negative checks. One example finding describes a callback that accepts a tenant from the request; the proposed design binds the OAuth transaction to the session and tenant and checks current authority. The accompanying test plan covers tenant substitution, cross-session use and revoked permissions.

The service and findings are fictional. Repairs are proposed and checks are planned, not executed. Use the [review template and test matrix](content/hub/api-integration/overview.en.md) to record actual revisions, observations and decisions for your own system.

## Components

- [Playbooks and checklists](content/hub/knowledge/overview.en.md) cover security review, application and platform security, supply chain, and AI security. The [site](https://defrixx.github.io/) provides English and Russian navigation.
- The [documentation index](DOCUMENTATION.md) lists topics and scenarios by directory.
- [SDD Security Analyzer](analyzer/README.md) checks specification documents against a pinned requirements catalog and prepares an independent report for human review.
- [Security Review](skills/security-review/SKILL.md), [Secure Development](skills/secure-development/SKILL.md), [Report Triage](skills/security-report-triage/SKILL.md), and [Fix Verification](skills/security-fix-verification/SKILL.md) are independently usable skills.
- [Shared requirements catalogue](catalog/README.md) indexes Analyzer and Secure Development requirements with their provenance. Semantic reconciliation between the sources is ongoing.
- [Prompt Integrity](tools/prompt-integrity/README.md), [Prompt Guard](tools/prompt-guard/README.md), [Model Security Eval](tools/model-security-eval/README.md), and [Sensitive Data Cleanup](tools/sensitive-data-cleanup/README.md) are standalone utilities. The [Bifrost integration](integrations/bifrost/README.md) provides application-owned gateway boundaries.
- [Policy examples](reference/security-policy-examples/overview.en.md) and [downloads](downloads/) provide executable examples and review templates.

The site is generated from source Markdown; see [site configuration](config/hub-scenarios.json) and [content synchronization](scripts/sync_starlight_content.py). Materials should be applied to the system's architecture, component versions, and threat model.

The [dependency security workflow](.github/workflows/dependency-security.yml) scans repository manifests and the built Analyzer runtime image on pull requests, pushes to `main`, and weekly. HIGH and CRITICAL findings fail the corresponding scan job; this separate workflow does not itself block site deployment. Review results for applicability and update affected dependencies or images.

## Licensing

Original playbooks, articles, diagrams, and prose templates in `content/`, `reference/`, and `downloads/`, as well as repository documentation outside independently licensed components, use CC BY 4.0. Original site code, scripts, configuration, and example code use MIT. Skills, tools, the Analyzer, and third-party materials retain their own notices. See [license boundaries](LICENSE), [MIT terms](LICENSE-MIT), and [Analyzer notices](analyzer/NOTICE).
