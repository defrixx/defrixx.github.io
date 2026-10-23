---
template: splash
tableOfContents: false
prev: false
next: false
title: "Skills and tools"
description: "Our five independent skills guide an assistant through security tasks; three Python tools perform bounded local operations. Choose an input and desired result, then open the gui..."
sidebar:
  order: 100
---
Our five independent skills guide an assistant through security tasks; three Python tools perform bounded local operations. Choose an input and desired result, then open the guide at the selected revision.

<div class="hub-catalogue">
<section class="catalogue-group"><h2>Skills for your assistant</h2>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/security-skills/secure-development/overview/">secure-development</a></h3>
<p>Write or change code</p></div>
<p class="catalogue-result">Applicable requirements, implementation and checks</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>Change, architecture, trust boundaries</dd>
<dt>Local execution</dt><dd>Assistant in an authorized local project</dd>
<dt>Limits</dt><dd>Select controls for the actual architecture; modifications need a task</dd>
<dt>Version / source</dt><dd>commit:55010b3f9484 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/skills/secure-development">Guide at this revision</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/security-skills/security-review/overview/">security-review</a></h3>
<p>Assess a PR or repository</p></div>
<p class="catalogue-result">Findings, hypotheses and prioritized actions</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>Scope and exact base/head or project revision</dd>
<dt>Local execution</dt><dd>Assistant; optional Python 3.9+ and Git helper</dd>
<dt>Limits</dt><dd>Assessment itself does not modify code</dd>
<dt>Version / source</dt><dd>commit:55010b3f9484 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/skills/security-review">Guide at this revision</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/security-skills/sensitive-data-cleanup/overview/">sensitive-data-cleanup</a></h3>
<p>Prepare material for sharing</p></div>
<p class="catalogue-result">Separate cleaned copy and redacted inventory</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>Agreed directory, mode and policy</dd>
<dt>Local execution</dt><dd>Assistant; Python 3.9+, POSIX helper</dd>
<dt>Limits</dt><dd>UTF-8 text/JSON/JSONL/CSV; JPEG/PNG metadata only; preserve originals</dd>
<dt>Version / source</dt><dd>commit:55010b3f9484 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/skills/sensitive-data-cleanup">Guide at this revision</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/security-skills/security-report-triage/overview/">security-report-triage</a></h3>
<p>Triage scanner signals</p></div>
<p class="catalogue-result">Accounted signals and action queue</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>Report provenance, target revision and scope</dd>
<dt>Local execution</dt><dd>Assistant; bounded SARIF helper Python 3.9+, POSIX</dd>
<dt>Limits</dt><dd>Normalization inventories signals; findings need context</dd>
<dt>Version / source</dt><dd>commit:55010b3f9484 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/skills/security-report-triage">Guide at this revision</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/security-skills/security-fix-verification/overview/">security-fix-verification</a></h3>
<p>Recheck a selected repair</p></div>
<p class="catalogue-result">Per-finding verdict and allowed/bypass cases</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>Finding ID, original evidence and patched revision</dd>
<dt>Local execution</dt><dd>Assistant in the selected local scope</dd>
<dt>Limits</dt><dd>Keep historical assessment separate from current repair verdict</dd>
<dt>Version / source</dt><dd>commit:55010b3f9484 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/skills/security-fix-verification">Guide at this revision</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
</section>
<section class="catalogue-group"><h2>Local tools</h2>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/prompt-integrity/overview/">prompt-integrity</a></h3>
<p>Verify static instructions at dispatch</p></div>
<p class="catalogue-result">Mismatch block or dispatch of checked snapshot</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>Protected baseline and application request</dd>
<dt>Local execution</dt><dd>Python 3.11+, POSIX; CLI/library</dd>
<dt>Limits</dt><dd>Strict Ollama/LM Studio adapter subsets; cover every dispatch route</dd>
<dt>Version / source</dt><dd>0.1.0 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/tools/prompt-integrity">Guide at this revision</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/prompt-guard/overview/">prompt-guard</a></h3>
<p>Inspect input and output at content boundaries</p></div>
<p class="catalogue-result">allow/block/review/error; explicit sanitized result</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>UTF-8 text/JSON, trusted source and policy</dd>
<dt>Local execution</dt><dd>Python 3.11+, POSIX; CLI/library</dd>
<dt>Limits</dt><dd>Literal/regex policies have false positives; action authorization is separate</dd>
<dt>Version / source</dt><dd>0.3.0 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/tools/prompt-guard">Guide at this revision</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/model-security-eval/overview/">model-security-eval</a></h3>
<p>Evaluate local model security regressions</p></div>
<p class="catalogue-result">CI verdict, events and private local evidence</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>Local model, synthetic profile and budgets</dd>
<dt>Local execution</dt><dd>Python 3.11+ and a local LM Studio/Ollama endpoint</dd>
<dt>Limits</dt><dd>Fixed scenarios and virtual effects; budgets may yield inconclusive</dd>
<dt>Version / source</dt><dd>0.4.0 · <code>55010b3f9484</code><br /><a href="https://github.com/defrixx/Product-security-skills/tree/55010b3f94844e310bc3ac85fae2a0256b689595/tools/model-security-eval">Guide at this revision</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/Product-security-skills/blob/55010b3f94844e310bc3ac85fae2a0256b689595/LICENSE">MIT</a></dd></dl></details></article>
</section>
</div>

## Versions and execution

This catalogue pins public Product-security-skills paths to one revision. It is a link registry with no automatic downloading or execution. Each entry links to that revision's guide and a related playbook. Installation and data processing happen in the local environment chosen by the user.

A skill version is the package commit SHA, not a Python package number. When copying a skill, retain the full directory and the source repository's root MIT notice. Sibling skills are optional. Tool versions come from their package metadata; a version number does not imply a PyPI release.
