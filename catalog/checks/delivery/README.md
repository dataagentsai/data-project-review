# Delivery checks

Why data projects fail for reasons other than technology, written so they apply without knowing the
project's details. Each check is a failure pattern, found in one of three ways:

1. **Signals**: things visible in the documents (`signals`, and `signal_id` where a detector in
   `scripts/signals.py` can find it mechanically).
2. **Contradictions**: two document types that disagree (`contradiction`).
3. **Silence**: nothing in the documents either way, so the `question` is asked directly. Every question
   also works as a pre-mortem prompt (see `templates/premortem.md`).

| File | Concern | Ids | Checks |
|---|---|---|---|
| `estimation.yaml` | Estimates and their assumptions | EST-01 to EST-07 | 7 |
| `requirements.yaml` | Requirements, definitions, acceptance criteria | REQ-01 to REQ-07 | 7 |
| `scope.yaml` | In scope, out of scope, change control | SCOPE-01 to SCOPE-06 | 6 |
| `project-management.yaml` | Plan, dependencies, risks, decisions, status | PM-01 to PM-10 | 10 |
| `stakeholders.yaml` | Who is involved, who decides, who can block | STK-01 to STK-06 | 6 |
| `communication.yaml` | How news, decisions and problems travel | COM-01 to COM-06 | 6 |
| `handover.yaml` | Runbook, decision log, knowledge transfer, support, benefits | HAND-01 to HAND-06 | 6 |
| **Total** | | | **48** |

Templates that answer these checks live in `templates/`: discovery document, estimate, scope, RAID log,
decision record, test strategy, release and cut-over, stakeholder map, status report and pre-mortem.
