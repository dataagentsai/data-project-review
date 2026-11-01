# Technical checks

84 technical checks, one file per technical concern in `catalog/vocab.yaml`. Each file is a YAML list
in the shape described in `catalog/SCHEMA.md`. No product names appear here; technology-specific
advice lives in `bindings/<tech>.yaml`.

| File | Concern | Ids | Checks |
|------|---------|-----|-------:|
| `duplicates.yaml` | Same data arriving or processed twice | DUP-01 to DUP-04 | 4 |
| `first-and-history-load.yaml` | Initial load, history, backfill | HIST-01 to HIST-04 | 4 |
| `late-and-corrected.yaml` | Late and corrected data, time zones | LATE-01 to LATE-04 | 4 |
| `deletes.yaml` | Deletes and soft deletes at the source | DEL-01 to DEL-03 | 3 |
| `history-over-time.yaml` | Slowly changing dimensions | SCD-01 to SCD-04 | 4 |
| `schema-change.yaml` | Columns added, renamed or retyped | SCH-01 to SCH-03 | 3 |
| `data-quality.yaml` | Rules, bad rows, quarantine, profiling | DQ-01 to DQ-05 | 5 |
| `reconciliation.yaml` | Numbers match from source to report | REC-01 to REC-04 | 4 |
| `performance.yaml` | Volume, speed, freshness, layout | PERF-01 to PERF-05 | 5 |
| `cost.yaml` | Running cost and its controls | COST-01 to COST-04 | 4 |
| `security-and-personal-data.yaml` | Access, masking, retention, regulation | SEC-01 to SEC-05 | 5 |
| `environments-and-access.yaml` | Environments, permissions, network, standards | ENV-01 to ENV-05 | 5 |
| `release-and-git.yaml` | Version control, review, promotion, config, secrets, infrastructure as code, rollback | REL-01 to REL-07 | 7 |
| `orchestration-and-recovery.yaml` | Dependencies, retries, restart, recovery | ORCH-01 to ORCH-06 | 6 |
| `operations.yaml` | Alerts, runbook, run records, support, hypercare | OPS-01 to OPS-05 | 5 |
| `testing.yaml` | Test levels, test data, automation, acceptance | TEST-01 to TEST-05 | 5 |
| `design.yaml` | Thin slice, non-functional needs, decisions, grain | DES-01 to DES-06 | 6 |
| `serving-and-consumers.yaml` | Consumer contracts, freshness, definitions | SERV-01 to SERV-05 | 5 |

Platform-only checks (`applies.kind: [new-platform]`): COST-02, SEC-04, ENV-01, ENV-04, REL-06, DES-05.
A project on an existing platform gets ENV-05 instead, which asks whether it follows the platform's standards.
Streaming- or change-capture-only checks: DUP-04, LATE-03, ORCH-06.
