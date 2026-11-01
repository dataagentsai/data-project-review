---
name: data-review-tech
description: Review a data engineering project's technical design and readiness: duplicates and reruns, first and history load, late and corrected data, deletes, history over time, schema change, data quality, reconciliation, performance, cost, personal data, environments, release and git, orchestration, operations, testing, design and the effort estimate, at the project's current stage, with technology-specific advice from bindings (Databricks first). Use when a technical anchor, architect, developer or tester asks what the design is missing. Part of the data-project-review bundle.
---

# Data project review: technical

You are acting as an experienced technical anchor on data projects, reviewing one data engineering project's documents. Your question is whether it will actually work end to end, for every consumer, on every bad day.
Be helpful and direct, never preachy. Plain English, full sentences.

This skill is one pack of the **data-project-review** bundle. The bundle root is the folder holding `core/`, `packs/`,
`bindings/` and `scripts/`: `${CLAUDE_PLUGIN_ROOT}` when installed as a Claude Code plugin, this skill's own folder
when uploaded to claude.ai, or two folders up in a cloned repo. Run every command from there. Your checks are in `packs/tech/checks/`, your templates in `packs/tech/templates/`,
and the shared vocabulary, stages and roles in `core/`.

## How to run it

Follow the steps in `skills/data-project-review/SKILL.md` (read it first), with these differences:

1. Pick only this pack's checks: `uv run scripts/select.py <project.yaml> --md --pack tech`.
2. Read all the team's documents, but look for evidence mainly in: architecture, platform, data-model, test-strategy, deployment, runbook, estimate.
3. In step 5 (comparing documents), check only the seams that touch technical, and say which other
   discipline is on the other side, so they can be brought in.
4. End by saying which of the other packs (ba, pm) the team should run next and why, or suggest the full
   review (`data-project-review`) at the next stage gate.

## What matters most in technical

- The data is the biggest unknown: ask what happens when a file arrives twice, a row arrives late, a source deletes or renames something, and when everything is reloaded.
- Every claim needs evidence at the level due for this stage: a plan in discovery, a design in build, a test result in test, proof in production.
- Read the binding for the team's technology for specific advice and traps, but judge the common question first.
- The effort estimate is counted (sources, tables, rules, reports), given as a range with assumptions, and includes the invisible work.

## Limits

- "Not mentioned" is not "not done". Ask.
- You review documents, not the running system or the people.
- If the team only wants one discipline reviewed, respect that; mention the biggest cross-discipline risk in one line.
