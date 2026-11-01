# Test results

## How the test works

`examples/sample-project/` is an invented retailer's project (Harbor & Pine, stage 6 Build, on an existing
Databricks platform) with 12 documents and 27 planted gaps: 14 technical, 13 delivery. 19 are hidden by omission,
2 by vague wording, 4 only show when two documents disagree, and 2 are never mentioned anywhere. There are also 5
things done well that a reviewer must not flag. The answer key (`tests/sample-project-key.yaml`) was written by a
separate helper that never saw the catalog. `tests/key-map.yaml` maps each gap to the checks that should catch it,
written by hand before the blind run.

A fresh Claude session reviewed the project using only `SKILL.md`, the catalog, bindings, templates, scripts and
the team's files. It could not see `tests/`, `docs/` or the README.

## Run 1 (1 November 2026, catalog v0.1, 132 common + 12 Databricks checks)

| Measure | Result |
|---|---|
| Planted gaps caught (missing, partly, contradicts or "not mentioned: ask") | **27 / 27** |
| Caught at the strict level (missing or contradicts only) | 19 / 27 |
| By how hidden | omission 19/19, contradiction 4/4, vague 2/2, silence 2/2 |
| Things done well wrongly flagged | **0 / 5** |
| Checks due / reviewed | 130 / 130 (22 covered, 48 partly, 41 missing, 5 contradicts, 12 unknown, 2 not applicable) |
| Disagreements between documents found | 14 |
| High-severity gaps found that were not planted | 14 (for example: never re-estimated against actuals, first production loads not reconciled); they read as real holes in the invented documents |

The 8 gaps caught only at the softer level were marked "partly" (customer history, performance on a 1% sample,
decision log, two stakeholder gaps, UAT timing) or "not mentioned" (rollback, running cost). That is a reasonable
call for gaps hidden by silence.

Outputs are kept in `tests/run-1/`.

### Changes made after run 1

- Three pairs of near-duplicate checks merged: OPS-02 into HAND-01 (runbook), OPS-04 into HAND-04 (support
  model), DES-03 into PM-03 (decision log). 129 common checks remain.
- The report now leads with the fail-fast plan, pre-mortem, disagreements and the 15 most serious gaps (about a
  7-minute read), then lists the rest by concern. Gaps owned by a role the team doesn't have are marked as falling
  to the technical anchor.
- The decision-log detector no longer treats a "decisions" section as missing; it reports it softly as "a
  section, not a log".
- The vague-words detector ignores requirement ids like NFR-01 when looking for a number; the estimate detector
  looks at the headline total, not at sizing tables.
- SKILL.md says when to use "contradicts" versus "missing", and accepts `roles_present`.

## Restructure into packs (2 November 2026, v0.2)

Checks moved into three packs (BA 11, PM 27, Tech 91) with no content changes; skills split into the conductor plus
one per pack. Re-scored run 1's review against the restructured catalog: still 27/27 planted gaps and 0/5 false
alarms, so the move broke nothing.

## Next

Fill the BA and PM packs with data-flavoured checks, write the seam checks, tag the answer key by pack, then run 2
and the first real project.
