# Analyzer reference

[Back to the quick start](README.md)

## Current review-mode limits

- A model-only applicability or conditional-clause exclusion stays unknown until supported by explicit user confirmation. Answering scope questions is optional: you can answer a subset and prepare a new review, while unresolved scope remains unknown. Original documents and raw model output stay unchanged. Preparing answers does not automatically start the review.
- Unknown, not assessed, missing context, and incomplete results are not a pass. They are also not proof of a defect. If retrieval cannot cover all selected document blocks, the affected assessment is conservatively unknown and the run is partial.
- The review checks documentation, not a running product. Model conclusions and quotations require human review; there is no security percentage or certification.
- Findings in document-review mode are currently read-only. Accept/reject decisions and patch editing belong to the advanced comparison workflow.
- Custom requirement catalogs work in review mode. Custom stage prompts, skills and saved pipelines are not yet supported there; the UI makes this restriction explicit instead of silently ignoring them. Use **Analysis mode → Advanced: compare and enrich changes** for these configurations.
- Review mode builds document blocks deterministically at P2 and produces its report after assessment (P6), without model-based change inference or generation/reassessment stages P7/P8. Exports require a ready report and include source references and hashes; treat document quotations as potentially sensitive.

## Advanced comparison

Choose **Analysis mode → Advanced: compare and enrich changes** when you have both existing baseline documentation and a separate Markdown change document. This retains the prior comparison, enrichment, patch review and export workflow, including old history. Multiple change-role Markdown files are combined with filename headings (100 KiB total); ordinary review uploads remain separate.

Changing selected patches changes the reviewed candidate. Preview/export marks that candidate as requiring a new analysis; it does not silently call a model or overwrite documents.

## Import a Hub skill as a draft

Under **Settings → Skills and advanced analysis settings**, choose **Import SKILL.md as draft** and select
one entry file from `skills/<name>/SKILL.md`. The preview shows the source text,
SHA-256 fingerprint, referenced resources and possible command/tool declarations.
Save creates a new **draft prompt**, never a published prompt or enabled skill.
No existing configuration is overwritten. Only simple `name`/`description` YAML
scalars are recognized; source text is preserved. Limits: UTF-8, 30,000 characters,
100 KiB; template braces conflicting with prompt syntax must be adapted first.

This supports reviewing entry files from Product-security-skills, not installing
its complete Bifrost package. References, assets, scripts, manifest files and tool
permissions are not imported. Dependency/command detection is advisory, not a
complete compatibility or security audit. For the advanced comparison workflow, adapt the instructions and output
schema before publishing a prompt and creating a declarative skill. Custom skills
are not available in document-review mode. Check the source license before
redistributing imported material. Code scanning, code changes, cleanup and fix verification are not supplied
by this importer. Nothing is sent to a model during preview or save.

Built-in prompts work without custom skills. The importer does not install or
execute Hub skill folders or overwrite existing configuration.

## MCP protocol profiles

Choose the protocol explicitly for each MCP connection. Existing `streamable_http`
connections retain **2025-06-18**, its initialization handshake and optional session
ID. The separate `streamable_http_2026_07_28` profile uses **2026-07-28** stateless
requests, per-request metadata and mirrored HTTP headers. Saving a different
profile creates a connection revision; test and approve that revision through the
normal data-access workflow. The capability report identifies the selected version.

The modern profile performs `server/discover`, paginated `tools/list`, and only
explicitly allowlisted `tools/call`. Invalid `x-mcp-header` tool definitions are
excluded and reported; header-bound arguments must match the approved schema.
Results require an explicit `resultType: complete` discriminator; sampling, elicitation, roots, tasks, subscriptions,
server-initiated requests and incomplete interaction results are not supported.
There is no protocol fallback, automatic tool retry, cross-request cache or
implicit use of another profile. A legacy-only server requires the legacy profile;
a modern-only server requires the modern profile. These profiles are not general
MCP agents, and tool descriptions never grant read-only authority.

Protocol references: [legacy lifecycle](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle),
[modern versioning](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning),
[modern HTTP binding](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
and [discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover).

Credentials are **session-only by default** and must be entered again after restart. Do not put keys in Git, Compose environment values, documents, or shell history. Advanced file-secret support requires a separate read-only mount under `/run/secrets` and file mode; Docker does not encrypt the host secret file.

## LM Studio native profile

For models whose OpenAI-compatible endpoint returns JSON only in `reasoning_content`,
create a separate **LM Studio native** connection using
`http://host.docker.internal:1234/api/v1`. Existing OpenAI-compatible profiles stay
unchanged. Choose reasoning **none** to send native `reasoning: "off"` per request;
this does not change LM Studio's global settings. The native route disables chat
storage and integrations and accepts only final message output, never reasoning
or tool output as a result.

This adapter requires explicit **prompt JSON + server validation** mode: the JSON
schema is supplied in the instruction and the application validates the response
locally. It is not server-enforced structured generation. Native requests support
only a system instruction plus one user input; automatic history-based structural
repair is unavailable and rejected output stops the affected stage. A successful capability
test demonstrates compatibility, not analysis quality. Existing data-scope approval,
budget, evidence and schema checks still apply. See the official [native chat API](https://lmstudio.ai/docs/developer/rest/chat)
and [model capability API](https://lmstudio.ai/docs/developer/rest/list).

For the initial built-in P3 stage in native mode, the model's wire contract omits
catalog `version`: this identifier is application-owned metadata. The application
first validates the complete version-free wire response, then attaches the version
from the uniquely pinned requirement/predicate/side mapping and runs the normal
canonical schema, evidence and coverage checks. Unknown, duplicate or ambiguous
identities and model-supplied versions are rejected. Raw responses remain unchanged;
the normalized output records the wire contract and pinned-metadata fingerprint.
Custom prompts, skills and architectural-review calls retain their existing contracts.

Native built-in P5 uses the explicit `builtin.P5.native.optional-design-summary.v1`
wire contract. Its `applicable_design` presentation summary may be omitted; it is
then stored as null without inferred text. A supplied summary must still be a
nonempty string of at most 600 characters. Decisions, evidence, explanations,
question/control-removal fields and pinned identifiers retain their mandatory
validation. Custom prompts/skills, OpenAI-compatible contracts and P8 are unchanged.
The wire version and missing-field handling are recorded on output artifacts and
participate in cache identity. This does not establish model assessment accuracy.

For the native built-in P3 fact-pins wire contract only, one narrowly bounded
syntax normalization may insert a single missing `{` at an array-element start
immediately before a JSON string key and colon. It requires a unique complete
strict parse, at most 64 KiB and 32 candidates. It does not remove tokens, edit
strings/values, accept duplicate keys, combine with Markdown-fence normalization,
or repair truncation/multiple errors. Original raw output is retained and the
normalization plus character offset is recorded. All wire/schema, pinned-ID,
evidence and semantic checks still run. This is syntax-only normalization, not
a guarantee of model intent, assessment quality or constrained generation.

## Document-review sequence

1. The browser submits selected document, catalog and connection IDs to preflight, which validates the configuration and exposes the data-access plan.
2. Starting the review pins its inputs and configuration. P1 snapshots the selected documents; P2 builds the checked block set without a model call.
3. P3 extracts applicability facts. P4 applies deterministic catalog conditions and holds model-only exclusions for user confirmation.
4. P5 assesses applicable obligations against checked-document evidence. Schema, pinned-ID, citation and coverage checks can reject or mark incomplete results.
5. P6 consolidates assessments, findings and unresolved questions. The report endpoint and ZIP export expose the independent report, with no P7/P8 rewrite stages.
6. Optional scope answers prepare a new review. The user reviews its inputs and starts it explicitly; earlier reports and original documents are preserved.


## Reviewing agentic application specifications

Select the applicable existing agentic catalogue records rather than treating every agent requirement as universal. A specification may describe ownership, authority boundaries, memory policy, resource limits or incident response without providing evidence of implementation. Report the documented intent and the available supporting evidence separately; leave implementation status unknown when the supplied materials cannot establish it. Do not infer an operational security result from a model's assessment of a document. The reviewer decides whether further implementation evidence is required.
