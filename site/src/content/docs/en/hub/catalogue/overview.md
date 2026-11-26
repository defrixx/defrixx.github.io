---
template: splash
tableOfContents: false
prev: false
next: false
title: "Skills and tools"
description: "Our four independent skills guide an assistant through security tasks; four Python tools perform bounded local operations. Choose an input and desired result, then open the rele..."
sidebar:
  order: 100
---
Our four independent skills guide an assistant through security tasks; four Python tools perform bounded local operations. Choose an input and desired result, then open the relevant guide.

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
<dt>Version / source</dt><dd>main<br /><a href="https://github.com/defrixx/defrixx.github.io/tree/main/skills/secure-development">Source package</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/defrixx.github.io/blob/main/skills/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/security-skills/security-review/overview/">security-review</a></h3>
<p>Assess a PR or repository</p></div>
<p class="catalogue-result">Findings, hypotheses and prioritized actions</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>Scope and exact base/head or project revision</dd>
<dt>Local execution</dt><dd>Assistant; optional Python 3.9+ and Git helper</dd>
<dt>Limits</dt><dd>Assessment itself does not modify code</dd>
<dt>Version / source</dt><dd>main<br /><a href="https://github.com/defrixx/defrixx.github.io/tree/main/skills/security-review">Source package</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/defrixx.github.io/blob/main/skills/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/security-skills/security-report-triage/overview/">security-report-triage</a></h3>
<p>Triage scanner signals</p></div>
<p class="catalogue-result">Accounted signals and action queue</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>Report provenance, target revision and scope</dd>
<dt>Local execution</dt><dd>Assistant; bounded SARIF helper Python 3.9+, POSIX</dd>
<dt>Limits</dt><dd>Normalization inventories signals; findings need context</dd>
<dt>Version / source</dt><dd>main<br /><a href="https://github.com/defrixx/defrixx.github.io/tree/main/skills/security-report-triage">Source package</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/defrixx.github.io/blob/main/skills/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/security-skills/security-fix-verification/overview/">security-fix-verification</a></h3>
<p>Recheck a selected repair</p></div>
<p class="catalogue-result">Per-finding verdict and allowed/bypass cases</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>Finding ID, original evidence and patched revision</dd>
<dt>Local execution</dt><dd>Assistant in the selected local scope</dd>
<dt>Limits</dt><dd>Keep historical assessment separate from current repair verdict</dd>
<dt>Version / source</dt><dd>main<br /><a href="https://github.com/defrixx/defrixx.github.io/tree/main/skills/security-fix-verification">Source package</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/defrixx.github.io/blob/main/skills/LICENSE">MIT</a></dd></dl></details></article>
</section>
<section class="catalogue-group"><h2>Local tools</h2>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/security-skills/sensitive-data-cleanup/overview/">sensitive-data-cleanup</a></h3>
<p>Prepare material for sharing</p></div>
<p class="catalogue-result">Separate cleaned copy and redacted inventory</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>Agreed directory, mode and policy</dd>
<dt>Local execution</dt><dd>Assistant; Python 3.9+, POSIX helper</dd>
<dt>Limits</dt><dd>UTF-8 text/JSON/JSONL/CSV; JPEG/PNG metadata only; preserve originals</dd>
<dt>Version / source</dt><dd>main<br /><a href="https://github.com/defrixx/defrixx.github.io/tree/main/tools/sensitive-data-cleanup">Source package</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/defrixx.github.io/blob/main/tools/sensitive-data-cleanup/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/prompt-integrity/overview/">prompt-integrity</a></h3>
<p>Verify static instructions at dispatch</p></div>
<p class="catalogue-result">Mismatch block or dispatch of checked snapshot</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>Protected baseline and application request</dd>
<dt>Local execution</dt><dd>Python 3.11+, POSIX; CLI/library</dd>
<dt>Limits</dt><dd>Strict Ollama/LM Studio adapter subsets; cover every dispatch route</dd>
<dt>Version / source</dt><dd>0.1.0<br /><a href="https://github.com/defrixx/defrixx.github.io/tree/main/tools/prompt-integrity">Source package</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/defrixx.github.io/blob/main/tools/prompt-integrity/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/prompt-guard/overview/">prompt-guard</a></h3>
<p>Inspect input and output at content boundaries</p></div>
<p class="catalogue-result">allow/block/review/error; explicit sanitized result</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>UTF-8 text/JSON, trusted source and policy</dd>
<dt>Local execution</dt><dd>Python 3.11+, POSIX; CLI/library</dd>
<dt>Limits</dt><dd>Literal/regex policies have false positives; action authorization is separate</dd>
<dt>Version / source</dt><dd>0.3.0<br /><a href="https://github.com/defrixx/defrixx.github.io/tree/main/tools/prompt-guard">Source package</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/defrixx.github.io/blob/main/tools/prompt-guard/LICENSE">MIT</a></dd></dl></details></article>
<article class="catalogue-item">
<div class="catalogue-summary">
<h3><a href="/en/ai-automation/model-security-eval/overview/">model-security-eval</a></h3>
<p>Evaluate local model security regressions</p></div>
<p class="catalogue-result">CI verdict, events and private local evidence</p>
<details class="catalogue-details"><summary>Inputs, execution and version</summary><dl>
<dt>Inputs</dt><dd>Local model, synthetic profile and budgets</dd>
<dt>Local execution</dt><dd>Python 3.11+ and a local LM Studio/Ollama endpoint</dd>
<dt>Limits</dt><dd>Fixed scenarios and virtual effects; budgets may yield inconclusive</dd>
<dt>Version / source</dt><dd>0.4.0<br /><a href="https://github.com/defrixx/defrixx.github.io/tree/main/tools/model-security-eval">Source package</a></dd>
<dt>License</dt><dd><a href="https://github.com/defrixx/defrixx.github.io/blob/main/tools/model-security-eval/LICENSE">MIT</a></dd></dl></details></article>
</section>
</div>

## Bifrost integration

[Connect the skills and tools through Bifrost](/en/ai-automation/bifrost/overview/): application ingress, final provider integrity, buffered SSE, authorized tools and skill staging.

## Versions and execution

This catalogue links to the skill and tool packages in the monorepository and their related playbooks. It does not download or execute them. For reproducible installation, select and record a repository commit. Installation and data processing happen in the local environment chosen by the user.

A skill version is the package commit SHA, not a Python package number. When copying a skill, retain the full directory and the source repository's root MIT notice. Sibling skills are optional. Tool versions come from their package metadata; a version number does not imply a PyPI release.
