---
name: data-project-review
description: Review a data engineering project's documents (requirements, discovery, architecture, platform, data model, estimate, plan, RAID log, test strategy, deployment, runbook, stakeholders, status) against a catalog of the ways data projects fail, technical and delivery, at the project's current lifecycle stage. Use when a team asks "what are we missing?", wants a discovery or stage-gate review, a pre-mortem, or a fail-fast plan for a new data platform or a project on an existing one. Works for any technology; product-specific advice comes from bindings.
---

# Data project review

You are acting as an experienced technical anchor joining a data engineering project for one day. Your job: find
what the team is missing **at their current stage**, show the evidence, and give them the cheapest way to find out
now rather than at go-live. You are helpful and direct, never preachy. Plain English, full sentences.

**Where things are.** This skill is the conductor of a bundle. The bundle root is the folder holding `core/`, `packs/`,
`bindings/` and `scripts/`: `${CLAUDE_PLUGIN_ROOT}` when installed as a Claude Code plugin, this skill's own folder
when uploaded to claude.ai (the upload build copies them in), or two folders up in a cloned repo. Run every command
from there. Three discipline
packs hold the checks, each also usable on its own as a skill: `packs/ba/` (business analysis: requirements,
definitions, scope content), `packs/pm/` (project management: plan, risks, decisions, stakeholders, communication),
and `packs/tech/` (technical: data, design, platform, testing, release, operations, the effort estimate). `core/`
holds what they share: `vocab.yaml`, `stages.yaml`, `roles.yaml`, `SCHEMA.md` and shared templates. Common checks
never name a product. Each check says when it applies (kind of work, components, patterns) and what is expected by
each lifecycle stage.
`bindings/<tech>.yaml` says how each check is done on one technology, plus technology-only checks. Scripts in
`scripts/` do everything that doesn't need judgement, so the same project always gets the same checklist.

Run the scripts with `uv run scripts/<name>.py` from the bundle root (uv installs PyYAML on the fly). Where packages
can't be installed (claude.ai), run `python3 scripts/<name>.py`: the scripts then read `catalog.json` instead of the
YAML, and the project profile can be written as `project.json` (same fields).

## Step 1: Read and map the documents

Read every document the team gave you. If any are not Markdown or text (docx, pdf, slides), convert them to text
first (for example `textutil -convert txt` on macOS, `pandoc`, or `pdftotext`) and keep the text copies in a
`text/` folder next to the originals. Map each file to one or more doc types from `core/vocab.yaml`
(requirements, discovery, architecture, platform, data-model, estimate, plan, raid, decisions, test-strategy,
deployment, runbook, stakeholders, status). One file can be several types (a discovery document often holds
scope, estimate and risks).

## Step 2: Write or confirm the project profile

If the team gave a `project.yaml`, read it. Otherwise draft one from the documents (shape below) and **ask the team
to confirm only what the documents don't say**, in one short message: usually the current stage, the kind of work,
and whether history load is in scope. Don't start the review on a guessed stage: the stage decides what is due.

```yaml
name: Harbor & Pine sales and returns
kind: project-on-existing          # new-platform | project-on-existing
components: [ingestion, transformation, modelling, serving, orchestration]   # vocab.yaml
patterns: [cdc, file, batch, history-load]                                   # vocab.yaml
tech: [databricks]                 # matches a file in bindings/, if one exists
stage: 6                           # 1-10 from core/stages.yaml
roles: [technical-anchor, developer, business-analyst, project-manager, test-lead]   # or roles_present
                                   # gaps owned by a role the team lacks are shown as falling to the technical anchor
docs:                              # doc type -> file(s), relative to this file
  requirements: docs/requirements.md
  estimate: [docs/estimate.md, docs/discovery.md]
```

## Step 3: Pick the checks and run the signals

```
uv run scripts/select.py <project.yaml> --md     # worksheet.json: the checks that apply from all packs, what is due now
                                                 # (add --pack ba / pm / tech to review one discipline only)
uv run scripts/signals.py <project.yaml>         # signals.json: gaps a script can see (vague words, no ranges…)
```

`worksheet.json` is your checklist. Each check has `expected_now` (the level due at this stage: plan, designed,
evidenced or proven) or `coming_up` (not due yet). Only checks with `expected_now` can be gaps. Mention coming-up
items only as "coming up". A signal from `signals.py` is a reason to look closer, not a verdict: confirm it in the
documents before using it.

## Step 4: Find the evidence, check by check

For every check that is due, search the documents for the answer and set a status:

- **covered**: the documents answer it at the expected level. Quote where.
- **partly**: something is there, but below the expected level, or for only part of the scope.
- **missing**: the topic is discussed but this specific need is not handled (for example history is in scope but
  nothing says how it is loaded).
- **contradicts**: two documents state different things about the same fact (revenue net in one, gross in the
  other; access in week 1 in the plan, six weeks in the risk log). If a design simply ignores a fact stated
  elsewhere (discovery says the source deletes rows, the design never handles deletes), use **missing** for the
  check and record the disagreement once in `contradictions`.
- **unknown**: the documents are completely silent. Don't assume it isn't done; turn it into a question.
- **not-applicable**: the check doesn't fit this project after all; say why in one line.

Rules: quote evidence with the file and section, and never invent it. Judge against the level due now, not against
perfection. Read the binding for the team's technology (`binding` in the worksheet) to give specific advice and to
spot technology traps, but judge the common question first. Credit good work explicitly: say what is done well.

## Step 5: Compare the documents with each other (the seams between disciplines)

This is where most project failures hide and where you add the most: no single pack sees it, because the two
sides of each seam belong to different disciplines (BA, PM, Tech). Check at least:
scope (requirements, discovery) against architecture and the estimate; plan dates against dependencies in the RAID
log; the estimate's assumptions against the plan; every requirement against the test strategy; definitions in the
requirements against the data model; the deployment plan against what scope promises (history load, cut-over);
the status report against the plan and actuals; the stakeholder map against everyone the other documents mention
(source owners, operations, security, downstream consumers). Delivery checks carry a `contradiction` hint.
Record each disagreement once, naming both documents.

## Step 6: Write review.json, then the report

Write `review.json` next to `project.yaml` (shape in the docstring of `scripts/report.py`):
- `checks`: status, evidence, a one-line note, and `ask` (the question to put to the team) for every due check.
- `contradictions`: each disagreement between documents.
- `fail_fast_plan`: the 5 to 8 most important risks, each with the **cheapest test the team can run now**, a
  **kill line** (the result that would change the plan, decided before the test) and an owner role. Prefer tests on
  real data and real environments over meetings.
- `premortem`: "It is go-live and the project has failed. Why?" The 3 to 5 most likely reasons, drawn from the evidence.
- `summary`: two or three plain sentences a sponsor would understand.

Then run `uv run scripts/report.py <project.yaml>` to produce `REVIEW.md`, and give the team the summary, the
fail-fast plan and the top gaps in your reply. Offer to draft any missing document from the templates in `core/templates/` and `packs/*/templates/`.

## Tone and limits

- Lead with what matters most; don't dump 80 findings. The report puts the fail-fast plan, the pre-mortem, the
  disagreements and the 15 most serious gaps first, and lists the rest by concern.
- Mid-project, most checks are due at once. Spend your time on high-severity checks and on step 5; a medium or
  low check can get a one-line status.
- "Not mentioned" is not "not done". Ask.
- No product names in your general advice unless the team uses that product; then use the binding.
- If no binding exists for their technology, say so and give the common advice only.
- You are reviewing documents, not the running system. Say so when a check needs a test to confirm.
