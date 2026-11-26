# SDD Security Analyzer

A local app for reviewing software design documents against a pinned security catalog. Upload multiple specification files, select requirements, check them together, and download a separate report. No existing baseline or change document is required. Originals are not overwritten.

The built-in catalog is an offline snapshot. Four updated OIDC and GitHub Actions requirements use newer pinned source revisions; their independent peer review is pending. Existing project catalogs and past runs retain their original versions. The monorepository's `catalog/playbook-links.json` tracks the historical source baseline and subsequent differences.

**This reviews documentation, not the security of a running system. Model output needs human review.**

## Start

Install and start Docker Desktop with Linux containers. No host Python, Node.js, or test setup is needed. Open a terminal in the monorepository’s `analyzer/` folder before running the commands below.

macOS (Docker Desktop):

```sh
mkdir -p config exports backups
docker compose up -d --build app
docker compose exec app python -m spec_enricher.cli bootstrap-url
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force config,exports,backups | Out-Null
docker compose up -d --build app
docker compose exec app python -m spec_enricher.cli bootstrap-url
```

Open the printed one-time sign-in link. The UI is at <http://127.0.0.1:8080>. The link expires after five minutes; do not share it. Generate another with the same command if needed. Sessions expire after 12 hours or a restart.

The first build downloads a pinned Alpine Linux image and hash-locked dependencies. The app does not install packages or download models at startup. Allow 2 CPUs / 2 GiB for the app, plus the resources your model needs.

The main compose.yaml sets the localhost port, persistent storage, and container security settings. The optional compose.test.yaml is used for the checks described in [Analyzer operations](OPERATIONS.md).

The UI starts in **English**. Choose English or Русский in the language selector; the browser remembers your choice. Language changes preserve the selected product and page and ask before discarding unsaved fields. The page's file picker follows this choice; the operating system's file dialog follows the browser/system language. Documents, catalog sources, prompts, and saved model outputs are not translated.

## First review

1. Create a product. Under **Documentation → Specification files**, select several Markdown files together, such as proposal, design, specs, and tasks. The default role keeps each file as a separate document. Limits: 20 files per upload, 1 MiB each, 10 MiB total product corpus.
2. Under **Requirements**, add requirements: review and enable the built-in catalog, select a smaller domain scope, import a schema 4.0 catalog, or author custom requirements. Templates in [templates](templates/) are not automatically active policy.
3. Configure one model under **Settings → Model connections**, run its capability test, and approve the exact destination and data scopes for this product.
4. Open **Analysis → New review**. The default **Check documents against requirements** mode lets you select all files, requirements and one model connection. Review readiness and the data-access plan, then start.
5. Open **Analysis → History and results** and read the independent report: requirement assessments, findings, unresolved questions and source evidence. Download its Markdown + JSON ZIP. No patches or rewritten specification need to be accepted.

Optional source imports and snapshots are under **Settings → External sources**, also linked from **Documentation**. They are separate from uploaded files selected for checking.

For review-mode limits, advanced comparison, and importing a Hub skill, see the [Analyzer reference](REFERENCE.md).

## Connect a model

For LM Studio on the Docker Desktop host:

- Load a model and start its server in LM Studio yourself.
- Use `http://host.docker.internal:1234/v1`. Container `localhost` is not the host.
- Use the app's DNS discovery and approve the exact private addresses for this endpoint.
- Select the actual loaded model ID. Use supported `json_schema` output, or explicitly choose degraded `prompt_json`.
- Run the capability test, then approve the project's destination and data scopes.

A successful capability test proves protocol compatibility, not analysis quality or sufficient context for a full run. The app does not load/switch models or fall back to another endpoint. Model-specific options must be set explicitly. Do not expose LM Studio to a LAN or change firewall/CORS settings just to make a test pass.

Other OpenAI-compatible endpoints require explicit external-access policy and project grants. You can enforce an additional startup restriction with `APP_DENY_EXTERNAL_EGRESS=true`; approved private endpoints remain available. Optional MCP sources support typed, explicitly allowlisted read-only calls, not arbitrary tools or shell execution.

For MCP and LM Studio native profiles, see the [Analyzer reference](REFERENCE.md).

## Security and limitations

- Single-user, localhost-only. Keep publication on `127.0.0.1`; this is not a public web server.
- The container runs non-root with a read-only filesystem, dropped capabilities, and no Docker socket. Persistent data is separate.
- Project data and history are scoped. One-time login, session, Host/Origin/CSRF, bounded parsing, path, schema, and citation checks are implemented.
- Untrusted documents, catalog text, and model/tool outputs cannot authorize network access, change permissions, or execute commands.
- Model output can be wrong despite valid structure and citations. Observed runs have confused missing documentation with an explicit contradiction. No detection-rate or security-certification claim is made.
- Third-party MCP servers control their own implementation. Read-only metadata does not prove the absence of server-side effects.
- Known-secret guards are not universal data-loss prevention. Review documents before sending them to an external service.
- Actual Windows Docker Desktop, auth/custom-port LM Studio, and a complete manual accessibility audit are not fully qualified by the available evidence.
- Host malware/admin access, Docker compromise, and physical secure erasure are outside the app's protection. Keep backups and exported data secure.

## Troubleshooting

- **Sign-in link rejected:** generate a new link; it is single-use and time-limited.
- **Model unreachable:** check the server, loaded model, host address, and exact approved private addresses.
- **Capability passes, analysis fails:** check context size, stage errors, budgets, and output mode. Partial/unknown is not a passing result.
- **Credential missing:** re-enter the session credential rather than adding it to a document or configuration file.
- **Run cannot resume after an update:** preserve history and start a new run with the saved inputs.

For updates, backups, restore, and optional checks, see [Analyzer operations](OPERATIONS.md).

## Architecture

![Architecture: the local browser uses the API and review pipeline, which reads the pinned catalog, stores project history, and prepares exports for human review. Model and MCP access goes through the permission broker and requires an approved destination and data scope.](architecture.svg)

The local browser talks to the API and review pipeline. The pipeline reads the pinned catalog, keeps project data and history, and prepares exports for human review. Model and MCP requests pass through the permission broker and require an approved destination and data scope.

The diagram is a local SVG image, so it does not require Mermaid support in the Markdown preview. If your preview blocks local images, [open the architecture diagram](architecture.svg) directly.

## Contents and licenses

This checkout contains the runnable app and a focused deterministic test suite, without historical experiments or development tooling. `spec_enricher/` is the backend and local UI; `catalog/` and `sources/` contain the pinned offline corpus; `templates/` supports authoring. The three retained `qa/` files are provenance referenced by the catalog, not a test suite. Sources remain in Russian to preserve their exact hashes and quotations.

Original application code uses the [MIT License](LICENSE). The catalog/source prose retains CC BY 4.0, its [upstream license](sources/LICENSE.upstream), attribution, and per-record provenance. See [NOTICE](NOTICE) for the boundaries and third-party terms. User documents and model outputs are not relicensed by the application.
