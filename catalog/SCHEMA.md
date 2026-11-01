# Catalog schema (v0.1)

Every file in `catalog/checks/**.yaml` is a YAML list of checks. Every check follows this shape.
`scripts/lint.py` enforces it.

```yaml
- id: DUP-01                      # permanent. PREFIX-NN. Never reuse or renumber.
  title: Same batch arriving twice  # short name, plain words
  kind: technical                 # technical | delivery
  concern: duplicates             # one of the concerns in concerns.yaml
  question: >-                    # the question a reviewer asks, answerable from documents
    How is a file or batch that arrives twice prevented from doubling the numbers?
  why: >-                         # one or two sentences: what goes wrong (a short failure story)
    The source resent yesterday's file after an outage and revenue doubled on the dashboard.
  applies:                        # when the check is relevant. 'any' = always.
    kind: [any]                   # new-platform | project-on-existing | any
    components: [ingestion, transformation]   # from components.yaml, or [any]
    patterns: [batch, cdc, file]  # from components.yaml patterns, or [any]
  owner: technical-anchor         # role id from roles.yaml (who must make sure it is answered)
  also: [test-lead]               # other roles who should look (optional)
  evidence:
    docs: [architecture, test-strategy]   # doc types from doc_types.yaml where the answer should be
    looks_like: a business key or file fingerprint, and a rerun test   # what a good answer contains
  signals:                        # how the GAP shows up in documents (delivery checks need these;
    - no mention of keys, reruns or duplicates in the architecture     #  technical checks optional)
  due:                            # lifecycle stage number (stages.yaml) by which each level is expected
    plan: 3                       #   plan      = we know how we'll handle it
    designed: 5                   #   designed  = it's in the design / backlog with acceptance criteria
    evidenced: 7                  #   evidenced = a test or run shows it works
    proven: 9                     #   proven    = it held in production
  fail_fast: >-                   # the cheapest test that could prove the team wrong, now
    Load the same file twice in test; row counts and sums must not change.
  severity: high                  # high | medium | low (impact if missed)
  related: [IDEM-01]              # other check ids (must exist)
  signal_id: null                 # optional: id of a deterministic detector in scripts/signals.py
  contradiction: >-               # delivery checks: which two doc types to compare, and what a disagreement means
    Compare the plan's dates with the RAID log's dependencies; a date earlier than its dependency means trouble.
```

Rules:
- **No product names** in `catalog/checks/**` (no Databricks, Snowflake, Spark, Delta, ADF, Fabric, dbt,
  Airflow, Kafka, AWS, Azure, GCP …). Product names live only in `bindings/<tech>.yaml`. The linter fails otherwise.
- Plain English. Full sentences. No arrow chains.
- Delivery checks must have `signals` and should have `contradiction`. For `signal_id: missing-doc-type`, put the
  document type the check is about first in `evidence.docs`.
- `due` may omit levels that don't apply (a delivery check may only have `plan` and `evidenced`).
- A check is about one question. Split, don't bundle.

## Bindings (`bindings/<tech>.yaml`)

```yaml
tech: databricks
name: Databricks
version_note: "checked against docs on 2026-11-01"
how:                      # per common check id: how it is done and verified on this technology
  DUP-01:
    do: MERGE on a business key; Auto Loader tracks files it has already ingested.
    verify: Re-run the job on the same input; DESCRIBE HISTORY shows no new rows written.
    traps: A MERGE that matches nothing still rewrites files and costs money.
checks:                   # technology-only checks, same shape as catalog checks plus `binding: <tech>`
  - id: DBX-01
    ...
```
