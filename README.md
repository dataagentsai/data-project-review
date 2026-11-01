# data-project-review

**A skill for Claude that reviews a data engineering project's documents and tells the team what they are
missing, at the stage they are in, with the cheapest way to find out now instead of at go-live.**

Give Claude this folder plus your project documents (requirements, discovery, architecture, data model, estimate,
plan, risk log, test strategy, deployment plan, runbook, stakeholder map, status reports). It works for a new data
platform or a project on an existing one, at any stage from "requirement received" to "project sign-off", and for
any technology.

It looks for the reasons data projects actually fail:
- **Technical:** duplicates and reruns, first load and history load, late and corrected data, deletes, history
  over time, schema change, data quality, reconciliation, performance, cost, personal data, environments,
  release and git, orchestration and recovery, operations, testing.
- **Delivery:** estimates, requirements, scope, project management, stakeholders, communication, handover.

Open source: code under Apache 2.0 (`LICENSE`), catalog and templates under CC BY 4.0 (`LICENSE-SPEC.txt`).
Part of [Clean Data Engineering](https://cleandataengineering.ai/). The thinking behind it:
[the technical anchor](https://cleandataengineering.ai/learn/technical-anchor/) and
[discovery](https://cleandataengineering.ai/learn/technical-anchor/discovery/).

## How it stays generic and still specific

| Layer | What it holds | Where |
|---|---|---|
| Common checks | Questions every data project faces, with no product names | `catalog/checks/` |
| When they apply | Kind of work, components (ingestion, serving…), patterns (CDC, streaming…), lifecycle stage, role | each check's `applies`, `due`, `owner` |
| Technology bindings | How each check is done on one product, its traps, and product-only checks | `bindings/<tech>.yaml` |

Switching technology means adding one binding file. The common checks don't change.

## Use it

**Claude Code:** copy or clone this folder into `~/.claude/skills/data-project-review/` (or a project's
`.claude/skills/`), then ask: *"Review our project documents in ./docs with the data-project-review skill."*

**claude.ai:** upload the folder as a skill (Settings, Capabilities, Skills), then attach your documents.

**By hand:**
```
uv run scripts/lint.py                                   # check the catalog
uv run scripts/select.py path/to/project.yaml --md       # which checks apply, what is due now
uv run scripts/signals.py path/to/project.yaml           # gaps a script can see in the documents
# Claude writes review.json (see SKILL.md), then:
uv run scripts/report.py path/to/project.yaml            # REVIEW.md
```

## What's here

```
SKILL.md                 the playbook Claude follows
catalog/                 SCHEMA.md, vocab.yaml, stages.yaml, roles.yaml, checks/technical, checks/delivery
bindings/                one file per technology (databricks.yaml first)
templates/               fill-in templates for missing documents (discovery, estimate, scope, RAID, tests…)
scripts/                 select, signals, report, lint, score
examples/sample-project/ an invented project with planted gaps, used to test the skill
tests/                   the answer key and how to score a review against it
docs/DESIGN.md           why it is built this way
```

## How we know it works

`examples/sample-project/` is an invented retailer's project with 27 planted gaps (some hidden by omission,
some by vague words, some only visible when two documents disagree) and a few things done well that a reviewer
must not flag. Claude reviews it blind; `scripts/score.py` reports how many gaps it caught and how many false
alarms it raised. See `tests/RESULTS.md`.

Status: v0.1, a working draft.
