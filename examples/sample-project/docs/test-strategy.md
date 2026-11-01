# Test Strategy — Sales and Returns Insight MVP 1

| | |
|---|---|
| Author | Ravi Menon (Tester, part-time) |
| Reviewed by | Tom Okafor (Technical Anchor), Priya Raman (BA) |
| Version | 1.0 |
| Last updated | Week 4 |

### 1. Objectives

- Confirm each pipeline stage transforms data as specified in `data-model.md`.
- Confirm data quality rules catch and quarantine bad rows as designed.
- Confirm the dashboard and extract meet the functional requirements and row-level security rules.
- Confirm the nightly run completes within the batch window.

### 2. Test levels

| Level | What | Who | Where | When |
|---|---|---|---|---|
| Unit | Transformation functions (PySpark), parsing, merge logic, DQ rule logic | Developers | Dev / CI | Every pull request |
| Component | Each job task end to end on a small fixture dataset | Developers | Dev | Every sprint |
| System integration (SIT) | Full nightly job across all tasks against source test systems | Tester | Test | Week 11 |
| Performance | Nightly job duration | Tester + Technical Anchor | Test | Week 11 |
| User acceptance (UAT) | Dashboard pages, filters, RLS, extract format | Finance users, BA | Test | Week 12 |

### 3. Unit testing approach

- Written with `pytest` and `chispa` for DataFrame comparison; run in the Azure DevOps CI pipeline on every pull request.
- Tests are table-driven: each test function takes a list of (input rows, expected output rows, description) cases.
- Transformation logic lives in Python modules (not notebooks) so it can be imported and tested locally.
- Target: every silver and gold transformation function has unit tests; merge logic has cases for insert, update and out-of-order changes.

Example cases for `silver.sales_line` merge:

| Case | Input | Expected |
|---|---|---|
| New line | op=2 for new key | Row inserted |
| Price correction | op=4 for existing key | Amount updated |
| Two updates same night | op=4 at LSN 10 and LSN 12 | LSN 12 values kept |
| Null discount | discount null | discount = 0 |

### 4. Data quality testing

Each rule in `data-model.md` §5 has at least one passing and one failing unit test case. In SIT, the tester injects known bad rows into the source test systems (e.g. unknown store ID, future date) and checks that they appear in `silver._quarantine` with the correct rule ID and that thresholds stop the pipeline when exceeded.

### 5. Test data

| Environment | Data |
|---|---|
| Dev / CI | Hand-built fixture files in the repo (`tests/fixtures/`) |
| Test – POS | POS test instance `STLK-TST01` (last refreshed from production 4 months ago) |
| Test – Cartwell | Cartwell staging tenant files; until available, masked production sample files |

### 6. Performance testing

- Run the full nightly job in test against a representative sample: 1% of POS history (~2M sales lines) plus one week of Cartwell files.
- Measure the duration of each task and the total.
- Pass criterion: total job completes in under 60 minutes, leaving time for the 07:00 Power BI refresh.
- Early run in week 4 (dev, same sample): 9 minutes total.

### 7. UAT

- Scheduled for week 12 in the test environment.
- Participants: two finance analysts, one regional manager, two store managers.
- Scenarios prepared by the BA from FR-01 to FR-11: navigate each page, apply filters, check row-level security (store manager sees only their store), download the marketing extract from the sandbox and check columns.
- Defects logged in Azure DevOps Boards with severity 1–4.
- **Exit:** no open severity 1 or 2 defects; UAT signed off by the Sponsor.

### 8. Entry and exit criteria

| Level | Entry | Exit |
|---|---|---|
| SIT | All features deployed to test; unit tests passing | All SIT cases run; no open sev 1; sev 2 have agreed fixes |
| Performance | SIT build stable | Job under 60 minutes on the sample |
| UAT | SIT exit met; UAT scenarios reviewed by BA | Sponsor sign-off |

### 9. Defect management

| Severity | Meaning | Fix expectation |
|---|---|---|
| 1 | Pipeline fails or wrong numbers on a main page | Before next test cycle |
| 2 | Feature unusable, workaround hard | Before go-live |
| 3 | Feature usable with workaround | Agreed with BA |
| 4 | Cosmetic | Backlog |

### 10. Tools

Azure DevOps Boards (defects), Azure DevOps Pipelines (CI), pytest, chispa, Databricks job run history.
