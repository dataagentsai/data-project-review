# Project review: Sales and Returns Insight (MVP 1)

Stage 6, Build · project-on-existing · technology: databricks · 127 checks due now, 0 coming up

The team has done solid engineering groundwork (clean release pipeline, service principals, written data quality rules, table-driven tests, real volumes from discovery), but the status says green while POS data has never been read from the live source, the history load that FR-10 requires has no design or estimate, and the data model calculates revenue differently from the definition the sponsor signed. Several design gaps (voided sales, Cartwell resends and late files, returns up to 60 days back) will quietly produce wrong numbers unless fixed before the gold build in sprint 4. Re-forecast the plan now: the estimate needs about 35 developer-weeks and the plan has about 28.

| Covered | Partly | Missing | Documents disagree | Not mentioned |
|---|---|---|---|---|
| 22 | 47 | 39 | 5 | 12 |

| Pack | Checks due | Gaps |
|---|---|---|
| BA: Business analysis | 11 | 10 |
| PM: Project management | 27 | 21 |
| TECH: Technical | 89 | 72 |

## Fail fast: do these first

| Risk | Cheapest test now | Kill line (what would change the plan) | Owner | By |
|---|---|---|---|---|
| The dashboard's headline revenue will not match the figure finance reports to the board. | Take last week's POS static extract and Cartwell files, compute revenue both ways (data model vs signed definition) and put both next to last week's manual pack in front of Mark Haddad. | If the gold definition differs from the pack by more than the tolerance Mark sets, change the gold model and DAX before sprint 4 starts. | Business analyst | this week |
| POS CDC has never run against a live source, and access may not arrive before gold is due. | Escalate R-01 to the sponsor now (its week-4 trigger passed); the day the account lands, run pos_extract against STLK-TST01 for all seven tables and compare with the DBA extract. | No live POS connection by end of week 7 means go-live moves, and the sponsor is told this week rather than in week 10. | Project manager | this week |
| Voids, price corrections and late returns leave gold wrong for past days. | On the static extract (or STLK-TST01), void a 3-day-old transaction, correct a 5-day-old line and add a return for a 30-day-old sale, run the job and compare silver detail with gold totals. | Any gold date that does not equal its silver detail means gold must rebuild affected dates (not just run_date - 1) before it is built in sprint 4. | Technical anchor | week 6 |
| Cartwell resends and late files double or drop online sales without anyone noticing. | In dev, drop orders_YYYYMMDD_v2.csv, then a same-name resend with a changed amount, then start the job with one file missing; check silver and gold totals. | If totals double, the correction is ignored, or the day publishes without a warning, switch silver to MERGE/replace-by-day and gate the job on file arrival before sprint 4. | Developers | week 6 |
| The 3-year history load (FR-10, ~200M lines) has no design, estimate, source window or reconciliation and could alone delay go-live. | Request the Cartwell history extract now; extract one month of POS sales_line over JDBC in an agreed window, time it, and record the LSN before and after. | If one month scaled to 36 takes longer than the windows the POS owner allows before week 11, or Cartwell cannot supply 3 years, re-scope FR-10 with the sponsor now. | Technical anchor | week 6 |
| The 12-week date cannot hold: ~35 developer-weeks of build in ~28 available, with no history, deployment or handover work counted. | Re-forecast from sprint 1–2 actuals with the leave, access delay and missing work added, and show a range to the sponsor at the next steering. | If the likely end is after week 12 (or after the January trading review), agree now what drops from MVP 1 (for example the marketing extract). | Project manager | next steering |
| Customer personal data goes to a third party without consent filtering, and credentials sit in the repo. | Ask the data protection lead to review the Brightwave extract layout and the opt-in rule; scan the repo for passwords and move POS/SFTP credentials to a secret scope. | If consent filtering or a lawful basis is not confirmed by week 9, the extract does not go live with MVP 1. | Security and governance | week 7 |
| Nobody can run or recover the system after go-live. | Name the support team, show them the job, and have them do one rerun and one past-day reload in test with a draft runbook. | No support team named by week 8 means go-live is held or the project team commits to hypercare for an agreed period. | Technical anchor | week 8 |

## Pre-mortem: the most likely ways this project fails

1. POS access arrived around week 8, CDC was first run against a live source in SIT, and its problems (deletes, the 3-day retention) surfaced in the last two weeks.
2. Finance compared the dashboard with the board pack in UAT and revenue was off by VAT and returns; trust was lost before go-live.
3. The history load was discovered as unplanned work in week 10; year-on-year pages (FR-07, a Must) were empty at launch.
4. Online revenue was double-counted after a Cartwell _v2 resend, or missing on late-file days, and store managers saw it first.
5. The plan never had room: 35 developer-weeks in about 28, reported green until week 10.

## Where the documents disagree

- **requirements.md §5 vs data-model.md §3.2:** Revenue is signed as excluding VAT and net of returns; the data model builds it including VAT and before returns. Units are 'net of returns' vs 'sum of quantity sold'. (REQ-03, SERV-04, REC-02)
- **requirements.md NFR-01 vs architecture.md §7:** 'Near real-time so store managers can act on the day's trading' vs a daily 05:00 batch. (DES-06, REQ-01)
- **requirements.md FR-10 vs discovery.md §2.1 vs architecture.md / plan.md / estimate.md / deployment-plan.md:** History is 'all' in requirements, 3 years (~200M lines) in discovery, and absent from architecture, plan, estimate and go-live steps. (HIST-01, EST-07, EST-04)
- **plan.md §4 vs raid-log.md R-01:** Plan needs POS access in week 1; the RAID log knew at week 0 that it takes about 6 weeks. (PM-01)
- **status-report-week5.md §1, §3 vs plan.md §2:** M1 reported Complete and everything green, while M1's exit criterion (query the POS test instance) is unmet and M3 is behind. (PM-04, COM-01)
- **estimate.md §3 vs plan.md §3 vs raid-log.md R-07:** 35 developer-weeks assume 3 developers for all 12 weeks; the plan reserves weeks 11–12 for SIT/UAT and one developer is on leave weeks 8–9 (~28 available). (PM-07)
- **discovery.md §2.1 vs architecture.md §3:** Voided sales are physically deleted at source; silver MERGE handles only inserts and updates. (DEL-01)
- **discovery.md §2.2 vs architecture.md §2.2–3:** Cartwell resends files (same name or _v2); ingestion appends and silver online orders append, so resends double or are ignored. (DUP-01)
- **discovery.md §2.2 vs architecture.md §6:** Cartwell files arrive after 06:00 on 9 days a quarter; the job runs at a fixed 05:00. (ORCH-01, DQ-04)
- **discovery.md §3 vs architecture.md §4:** Returns are attributed to an original sale up to 60 days back, but fact_returns_daily writes only business_date = run_date - 1. (LATE-01)
- **platform-and-environments.md §3 vs platform-and-environments.md §6:** Dev is meant to read the POS test instance, but the firewall request covers only test and prod subnets. (ENV-03)
- **plan.md §7 / deployment-plan.md §5 step 8 vs status-report-week5.md §7:** Plan shares the dashboard with store managers after the first refresh; steering agreed to wait one week so finance can check numbers. (COM-03, REC-04)
- **data-model.md §2 vs data-model.md §4:** silver.customer holds marketing_opt_in, but the marketing extract selects all active customers. (SEC-01)
- **stakeholders.md §1 vs requirements.md §3 / discovery.md §4:** Marketing (an extract consumer), the POS owner/DBA and a support team appear in other documents but not in the stakeholder map. (STK-01)

## The 15 most serious gaps

| Check | Severity | Status | What we found | Owner | Ask |
|---|---|---|---|---|---|
| **PM-01** Dates set before the dependencies were known | high | Documents disagree | The plan needs POS access in week 1 while the RAID log knew at week 0 it takes about six weeks; the critical path starts with source access. (plan.md § 4. Dependencies; raid-log.md § R-01) | Project manager | With access likely in week 7 or later, what moves on the critical path? |
| **PM-04** Green until it is red | high | Documents disagree | Status is green everywhere while M1's exit criterion is not met, M3 (due week 5) is incomplete, and I-02/I-04 threaten the critical path. (status-report-week5.md § 1. Overall status; status-report-week5.md § 3. Progress; plan.md § 2. Milestones) | Project manager | What rule sets the RAG colour? On forecast versus baseline, schedule is amber at least. |
| **REQ-03** Business definitions not agreed and signed | high | Documents disagree | Definitions are written and signed (good), but the data model builds revenue including VAT and before returns, and units gross of returns, so the headline number will not match the board figure. (requirements.md § 5. Business definitions; data-model.md § 3.2 Facts; requirements.md § 5; data-model.md § 3.2) | Business analyst | Which revenue is right? If the signed one, the gold model and DAX must change now, before gold is built in sprint 4. |
| **COM-01** Bad news held back | high | Missing | The 6-week access lead time was known at week 0 and POS CDC has never run against a live source, yet the sponsor sees all green and 'M1 Complete'. (raid-log.md § Risks R-01; status-report-week5.md § 1. Overall status) | Technical anchor | What do we know today that Claire does not? Tell her this week: POS access is ~5 weeks late, CDC is untested live, customer merge is behind. |
| **DEL-01** Detecting hard deletes at the source | high | Missing | Discovery found physical deletes of voided sales, but the silver MERGE handles only inserts and updates; CDC delete rows (operation 1) are ignored, so voids stay in revenue. (discovery.md § 2.1 StoreLink POS; architecture.md § 3. Transformation (silver)) | Technical anchor | What does silver.sales_line do with CDC operation 1? Can we void a transaction in STLK-TST01 and watch it leave gold? |
| **DUP-01** Same batch or file arriving twice | high | Missing | A _v2 resend is a new file to Auto Loader and is appended twice (doubling online sales); a same-name resend is ignored by Auto Loader by default, so the corrected file is lost. (discovery.md § 2.2 Cartwell; architecture.md § 3. Transformation (silver)) | Technical anchor | What happens to online revenue when orders_YYYYMMDD_v2.csv arrives? Should silver MERGE on order_id, line_no and replace the day? |
| **ENV-03** Network path to every source proven early | high | Missing | No connection to POS has been made from any environment; Cartwell staging and Brightwave sandbox are not connected either. The firewall request omits the dev subnet that the platform doc says dev uses. (raid-log.md § Dependencies D-01/D-02; platform-and-environments.md § 6. Network; platform-and-environments.md § 3. Source connectivity) | Platform team (not on the team: technical anchor by default) | Does the firewall request include the dev subnet? When will each of POS test, POS prod, Cartwell staging and Brightwave SFTP get a test connection? |
| **EST-02** One number instead of a range | high | Missing | A single number with no range or spread. (estimate.md § 1. Summary) | Technical anchor | What is the low and high end, and what moves it (access date, customer merge, history load)? |
| **EST-04** Invisible work left out of the estimate | high | Missing | Only build features are counted: no lines for access, environments, history load, testing/SIT/UAT support, data fixes, deployment, cut-over, runbook or handover. (estimate.md § 2. Breakdown by feature) | Technical anchor | Where are history load, SIT/UAT fixes, cut-over and handover in the 35 developer-weeks? |
| **EST-06** Never corrected against actual progress | high | Missing | No comparison of actuals with the estimate or forecast finish; M3 is due now and incomplete but the date is unchanged. (status-report-week5.md § 3. Progress) | Technical anchor | What does the real rate over sprints 1–2 forecast for go-live? |
| **EST-07** History load and data fixing underestimated | high | Missing | History load of ~200M POS lines plus a Cartwell one-off extract is a Must (FR-10) and has no estimate line. (discovery.md § 2.1; estimate.md § 2) | Technical anchor | Who estimates the history load and its reconciliation, and from what trial? |
| **HAND-01** Runbook missing or written at the end | high | Missing | No runbook exists or is planned in the plan or estimate. (deployment-plan.md § 6. Monitoring after go-live) | Technical anchor | Who writes the runbook, starting when, and who will test it? |
| **HAND-03** Knowledge transfer never tested | high | Missing | No knowledge-transfer plan; no support team is named anywhere. | Technical anchor | Which team will run this, and when will they do one change and one recovery while the project team watches? |
| **HAND-04** Support model not agreed | high | Missing | Nobody is named to support the system after go-live; alerts go to the developers' list. (plan.md § 7. Go-live) | Project manager | Who answers a failure on the first weekend in production, in which hours, and for how long does the project team stay? |
| **HIST-01** History load scope and approach | high | Missing | History is a Must, but architecture, plan, estimate and deployment plan never say how it is loaded, in what order, or who checks it. FR-10 also says 'all' while discovery says 3 years. (requirements.md § FR-10; discovery.md § 2.1; discovery.md § 2.2) | Technical anchor | How will 3 years of POS and Cartwell history be loaded, when, and who signs off the historical numbers? Has the Cartwell extract been requested? |

## All other gaps (88), by concern

**Initial load, history, backfill**
- HIST-03 Handing over from history load to incremental loads (missing, high): Nothing defines the LSN taken before the history snapshot or how the overlap is absorbed; with 3-day CDC retention the gap risk is real. Ask: Which LSN is recorded before the history extract starts, and how is bronze._pos_watermark seeded from it?
- HIST-02 Source can bear the history extract (missing, medium): 200M lines over JDBC from an on-premises production POS has no chunking, extract window or agreement with the POS owner. Ask: When may the history extract run against STLK-PRD01, in what chunks, and has one chunk been timed?
- HIST-04 Reloading or backfilling a past period (partly covered, medium): Gold writes by period, which is the right shape, but no run-date parameter or reload procedure is described for bronze/silver. Ask: Can the job be run for a chosen past date, and which tables must be rebuilt with it?

**Late arriving and corrected data**
- LATE-01 Late and corrected rows rebuild the right periods (missing, high): Returns are attributed to an original sale date up to 60 days back, but gold writes only yesterday's partition (and replaceWhere would drop earlier returns for that date). Corrections to older sales also never reach gold. Ask: Which gold dates are rebuilt when a return arrives for a sale 30 days ago, or a 5-day-old line is price-corrected?
- LATE-02 Facts arriving before their reference data (partly covered, high): Unknown members exist for products, but nothing re-points facts when the product or the original sale arrives later; DQ-08's fallback silently moves returns to the wrong period. Ask: When the product or the original sale turns up a day later, are the affected facts corrected?
- LATE-04 Time zones and business dates (not mentioned: ask, medium): Time zones of POS and Cartwell timestamps and the business-day definition are not stated (BST/GMT changes matter for near-midnight online orders). Ask: Which time zone are Cartwell order timestamps in, and is an online order at 23:30 UK time on the day it was placed?

**Scheduling, dependencies, retries, restart**
- ORCH-01 Jobs wait for their data, not the clock (missing, high): The job starts on the clock; on roughly one day in ten Cartwell files are not there, so the day publishes without online sales and nobody is told. Ask: Should the Cartwell task wait for all three files (file-arrival trigger) with a cut-off, and what does finance see if they are late?
- ORCH-05 Recovery time and data loss limits (missing, high): Discovery names a hard recovery limit, but there is no agreed recovery time, no plan if CDC retention is exceeded (full re-snapshot), and no backup approach. Ask: If extraction is down for 3 days, how is POS recovered, and how long may the dashboard be stale?
- ORCH-03 Restart after failing in the middle (partly covered, high): Split into tasks with atomic Delta writes; restart behaviour and whether Power BI can read a half-finished run are not described. Ask: If gold_build fails at 06:50, what does the 07:00 refresh show?
- ORCH-06 Stream restarts from where it stopped (partly covered, high): Saved positions exist for both sources; the CDC 3-day retention versus outage and a reset procedure are not covered. Ask: What happens if the saved LSN is older than CDC retention?
- DBX-06 Job retries, concurrency and repair are safe (not mentioned: ask, high): Retries, timeouts and concurrency per task are not stated, and two silver tables are built by append, so a repair run is not obviously safe. Ask: What retry, timeout and max-concurrent-runs settings are in the bundle for hp_sales_daily, and is each task safe to rerun from the start?
- DBX-04 Table retention matches time travel and recovery needs (not mentioned: ask, medium): Nothing on Delta retention or VACUUM settings per table. Ask: What retention do bronze/silver/gold tables use, and does it allow RESTORE for a bad release and still meet erasure deadlines for customer data?
- ORCH-02 Retries for passing failures only (not mentioned: ask, medium): No retry policy described. Ask: Which failures are retried (JDBC timeout, SFTP) and how many times?
- ORCH-04 Two runs writing the same table at once (not mentioned: ask, medium): Concurrency not stated. Ask: Is max concurrent runs 1 for hp_sales_daily, and what is the rule for manual reruns?

**Plan, dependencies, risks, decisions, status**
- PM-02 Risks listed, not managed (missing, high): Risks are listed but 6 of 7 have no owner, no triggers, and R-01's own week-4 escalation trigger has passed with no escalation recorded. Ask: Who owns each risk, and was R-01 escalated in week 4?
- PM-03 Decisions not written down (partly covered, high): Decisions exist in the architecture and in meeting notes, but no decision log with options, decider and date (the signal missed the architecture table). Ask: Can one decision log collect architecture §7 and the week-5 meeting decisions?
- PM-05 Testing and deployment left to the end (partly covered, high): Unit tests in CI from day one (good); but first deployment to test is week 7–8 and SIT, performance and UAT are squeezed into the last two weeks. Ask: Can a thin slice be deployed to test and run against real sources by week 6?
- PM-07 The plan ignores the estimate's assumptions (documents disagree, medium): The estimate uses all 12 weeks of 3 developers for build; the plan needs build finished by week 10 (30 developer-weeks) and leave removes 2 more, leaving ~28 for 35 weeks of work, before history load or access delay. Ask: Where do the missing ~7 developer-weeks come from?
- PM-08 Open decisions with no owner, deadline or default (missing, medium): Open decisions exist (customer matching rule, online SKU categories, 2027 calendar, returns-by-reason page, revenue definition) with no owner, date or default. Ask: Can each open point get an owner, a needed-by date and a default?
- PM-06 Key-person risk (partly covered, medium): Each area has one developer; one technical anchor; a part-time tester. Leave is logged (good) but no second person per critical area. Ask: Who is the second person for POS CDC, customer merge and CI/CD?

**Proving numbers match from source to report**
- REC-02 Matched against a number the business already trusts (missing, high): The requirement names the ledger, but no test compares any figure with the ledger or the current weekly pack. Ask: Which weekly pack or ledger figure will each measure be matched to, and when is the first comparison?
- REC-04 First production loads reconciled (missing, high): The first production run is checked only for non-zero counts; no reconciliation of history or first loads before users rely on them. Ask: Who reconciles the first production week and the history load before store managers get access?
- REC-01 Counts and totals reconciled layer by layer (partly covered, high): Quarantine and reference-row counts are recorded, but no source-to-gold count and sum comparison per run. Ask: Can each run record POS and Cartwell counts and sums at source, bronze, silver and gold?
- REC-03 Tolerances and who signs off differences (missing, medium): No tolerance per measure or named approver. Ask: What difference from the ledger is acceptable, and who signs it off (Mark?)

**Version control, branching, promotion between environments**
- REL-05 No secrets in the repository (missing, high): Config files in the repo hold the POS password; no secret scope or secret scan is mentioned. Ask: Can the POS and SFTP credentials move to a secret scope (or a UC connection) before the service account is issued, and is the repo history clean?
- REL-07 Rolling back a release, including its data (not mentioned: ask, high): No rollback plan for code or data. Ask: If v1.0.x writes wrong gold data, how do we redeploy the previous bundle and RESTORE the tables?

**Requirements, definitions, acceptance criteria**
- REQ-01 Vague words in the requirements (missing, high): Three vague phrases in signed requirements; two already contradict other documents. Ask: Replace with numbers: 'previous day by 07:00', '3 years', 'within X of the ledger'.
- REQ-02 No acceptance criteria (missing, high): No acceptance criteria for any FR. Ask: For FR-04, FR-05, FR-07: given last week's data, what figure must the dashboard show?
- REQ-04 Requirements written without looking at the data (partly covered, high): Requirements map to known sources, but there is no field-level check; e.g. FR-06 home region from address and FR-09 contact details were not checked against real data. Ask: Which source field supplies home_region, and how complete is it?
- REQ-06 Non-functional needs missing (partly covered, high): Page speed and availability have numbers; volume, recovery, data loss, retention and access to personal data do not. Ask: Can recovery time, retention and who may see customer contact details be added to the NFRs?
- REQ-05 The users are not the requesters (partly covered, medium): Store managers test in UAT, but none were asked what they need; sprint reviews show finance only. Marketing users are not engaged at all. Ask: Can two store managers and someone from marketing see the wireframes before sprint 5?

**Columns added, renamed or retyped at the source**
- SCH-02 A column renamed, removed or retyped (missing, high): A rename has happened before; nothing makes the load stop loudly, and inferred schemas would load nulls into the old column. Ask: Will a renamed or retyped Cartwell column fail the load with an alert?
- DBX-05 Auto Loader schema evolution mode chosen per source (missing, medium): No schema evolution mode is chosen, although Cartwell changed layouts twice in 12 months including a rename. Ask: Which schemaEvolutionMode is used per Cartwell entity, who watches _rescued_data, and does the task retry after the intentional stop on a new column?
- SCH-01 A new column appears at the source (missing, medium): No policy per layer for new columns. Ask: When Cartwell adds a column, should bronze carry it and silver ignore it until reviewed?
- SCH-03 Source owners warn before they change (partly covered, medium): Changes are announced to the e-commerce team, not the data team, and there is no written agreement. Ask: Can Leo's team forward Cartwell change notices to the data team, and can POS changes be agreed the same way?

**In scope, out of scope, change control**
- SCOPE-01 Scope written only as "in" (missing, high): Only an in-scope list. Ask: What is explicitly out (e.g. returns-by-reason page, stock, other channels) and later?
- SCOPE-02 The data scope traps left silent (missing, high): Of the ten traps, only history (vaguely) and reports are stated; deletes, late data, changes over time, bad rows, personal data, access and recovery are silent. Ask: Can we write in/out/later for each trap with the sponsor?
- SCOPE-03 Scope creep with no change process (missing, high): Requests are arriving with no change process. Ask: Who decides new requests, and how are their size and date impact recorded?
- SCOPE-04 "Phase 2" used as a hiding place (partly covered, medium): MVP 2 is referenced but no later list exists. Ask: What is in MVP 2, and is it funded?
- SCOPE-05 MVP 1 is too big (partly covered, medium): MVP 1 combines two sources, customer merge, a personal-data extract and a 3-year history load in 12 weeks; the marketing extract could be split out. Ask: Would MVP 1 still meet O1–O3 without the marketing extract (FR-09)?
- SCOPE-06 Scope not signed by the business owner (partly covered, medium): Scope is signed and dated (good), but only the in-list exists to sign. Ask: Can the sponsor sign the out and later lists too?

**Access, masking, retention, regulations**
- SEC-01 Personal and sensitive data found and classified (missing, high): No classification of personal columns; the marketing extract sends names, emails and phones to a third party without filtering on marketing_opt_in. Ask: Has data protection approved the Brightwave extract, and must it include only customers with marketing_opt_in = true?
- SEC-02 Who can see what (partly covered, high): Group grants and Power BI RLS are designed; the mapping is not started and no persona tests or access rules for silver customer PII exist. Ask: Who may read silver.customer in prod, and will RLS be tested as a store manager?
- SEC-03 Retention and the right to be forgotten (not mentioned: ask, high): Retention and erasure are not mentioned. Ask: How long is customer data kept, and how is an erasure request applied across silver, gold, history and sent extracts?

**Architecture decisions, patterns, non-functional needs**
- DES-01 A thin slice proved the design end to end (partly covered, high): Pieces run in dev, but nothing has gone source → bronze → silver → gold → Power BI, and POS never from the live CDC source. Ask: Can one Cartwell entity and one POS table be pushed all the way to a Power BI page in test within two weeks?
- DES-02 Non-functional needs written as numbers (partly covered, high): Some needs have numbers (5 s, 08:00–21:00, 60-minute run); freshness, accuracy, recovery and retention do not. Ask: Can we write: data ready by 07:00 on X% of days; reconciled to the ledger within Y; recovery within Z hours; data kept N years?
- DES-06 Batch or streaming chosen for a reason (documents disagree, medium): The batch choice is sensible for the stated consumers, but the signed requirement asks for near real-time and was never corrected. Ask: Will the sponsor change NFR-01 to 'previous day's trading by 07:00'? Store managers acting on 'the day's trading' cannot be met by a daily batch.

**Rules, bad rows, quarantine**
- DQ-04 A source goes quiet or sends far too little (partly covered, high): Volume check only on reference tables; nothing detects a missing or tiny Cartwell file or a quiet POS feed, which discovery shows happens. Ask: What stops the 05:00 run publishing a day with no online sales when Cartwell is late?
- DQ-05 Real data profiled before design (partly covered, high): Discovery captured volumes and behaviour well, but no profile of keys, nulls and duplicates; the week-4 date format and week-5 customer surprises are what a profile finds. Ask: Can we profile the POS static extract and Cartwell customers now (key uniqueness, null emails, cards per email) and show Mark?
- DQ-03 One poison record does not stop the whole load (partly covered, medium): Parsing failures have already happened; there is no stated rescued-data or bad-records handling for malformed CSV rows. Ask: Is _rescued_data (or badRecordsPath) captured and watched for Cartwell files? What happens to a row with a broken quote or encoding?

**Same data arriving or being processed twice**
- DUP-02 Rerunning a job changes the result (partly covered, high): Gold and the sales MERGE are rerunnable; the appended silver online orders and bronze appends are not obviously safe to rerun. Ask: If silver_pipeline fails after writing online orders and is repaired, are rows appended twice?
- DUP-03 Duplicates already inside the source (partly covered, high): Keys are chosen and customer uniqueness fails the pipeline, but the rule for source duplicates (several cards per email) is still open. Ask: What is the agreed rule when one email has several loyalty cards, and has Mark signed it?

**Estimates and their assumptions**
- EST-01 The rough guess became the promise (partly covered, high): The baseline is a discovery estimate (good), but it has not been revisited since, although access, customer merge and history load facts have changed. Ask: When will the estimate be redone with week 1–5 actuals?
- EST-03 An estimate with no written assumptions (partly covered, high): The estimate lists no assumptions of its own; some live in the RAID log and requirements, but not the ones it rests on (access by week 1, full team all 12 weeks, JDBC pattern reuse). Ask: Which assumption moves the 12 weeks the most, and is it in the RAID log with an owner?

**Monitoring, alerting, support, runbooks**
- OPS-01 Alerts reach someone who can act (partly covered, high): Failure email exists, but to the developers' list, with no lateness alert against 07:00 and no response time. Ask: Who receives the alert at 05:30 and must act before the 07:00 refresh?
- OPS-05 Production watched closely after go-live (missing, medium): Go-live ends after the first run; no hypercare period. Ask: How many weeks of daily checks follow go-live, and who does them?
- OPS-03 Every run leaves a record (partly covered, medium): DQ results and file lineage per run are recorded; no audit of rows read/written per task. Ask: Can each task write counts read and written per run?

**Volume, speed, freshness**
- PERF-02 Freshness target measured end to end (partly covered, high): A time budget exists; the end-to-end path including late Cartwell arrival and the refresh has not been timed. Ask: What freshness do we promise on a day Cartwell arrives at 07:30?
- PERF-03 Tested at production volume (partly covered, high): A nightly-run test is planned and an early 9-minute run exists (good), but no peak-day test, no production compute check and no test of the 200M-line history load. Ask: Can we time a December peak day and one month of history on the bundle's job clusters?
- PERF-05 Storage layout and file sizes kept healthy (partly covered, medium): Daily partitions on small aggregate tables create many small files; no compaction or clustering approach stated. Ask: Are gold tables managed (predictive optimization on) or should they use liquid clustering instead of date partitions?
- PERF-04 Skewed keys and very large joins (not mentioned: ask, medium): Customer matching on email may hit null or shared emails as a hot key. Ask: How many customers have null or shared emails, and how is the match join handled for them?

**Contracts with consumers, grain, freshness promises**
- SERV-01 A contract with each consumer (partly covered, high): The extract layout is defined (good); no delivery time, contact or agreement with Brightwave/marketing. Ask: Who in marketing owns the extract, and what time must it arrive?
- SERV-04 Business definitions live in one place (partly covered, high): Measures are defined once in one Power BI dataset (good), but the definition differs from the signed one (see REQ-03).
- SERV-02 Consumers can tell whether data is complete (missing, medium): No 'data as of' or completeness flag, though partial days are likely when Cartwell is late. Ask: Will the dashboard show last refresh time and whether online data is complete for yesterday?
- SERV-05 Consumer queries fast enough under real load (partly covered, medium): Target and Import mode set; no concurrency test with 50+ users at store opening. Ask: Will we test page load with the expected morning users?
- SERV-03 Changes to what consumers use are announced (not mentioned: ask, medium): Nothing on announcing changes to the dataset or extract. Ask: How will a change to the extract columns be announced to Brightwave?

**Who is involved, who decides, who can block**
- STK-01 Only the sponsor is managed (partly covered, high): A broad map (good), but missing the POS system owner/DBA, marketing and Brightwave, the support team, and data protection, all named in other documents. Ask: Who owns StoreLink, who owns the marketing extract, and who will support the system?
- STK-04 Conflicts left unsaid (partly covered, medium): The NFR-01 versus daily-batch conflict and the new January date are not written as open decisions. Ask: What calendar date is week 12, and is it before the January trading review?
- STK-05 Sign-off without reading (not mentioned: ask, medium): No record of review time or findings; the sponsor signed definitions that the data model now differs from. Ask: Did Mark review the definitions before Claire signed?

**Test levels, test data, environments**
- TEST-01 Test levels that include data tests (partly covered, high): All levels with owners (good), and DQ tests; no reconciliation test level. Ask: Where do source-to-gold and gold-to-ledger reconciliation tests sit?
- TEST-02 Realistic, safe test data (partly covered, high): Sources are named; test POS is stale and the masking of the POS DBA extract is not stated. Ask: Is the static POS extract masked, and can STLK-TST01 be refreshed before SIT?
- TEST-04 Users test with numbers they recognise (partly covered, high): UAT checks screens, not figures users already know. Ask: Can finance supply last month's pack figures as UAT expected results?
- TEST-05 Failure, rerun and recovery tested on purpose (partly covered, high): Bad-row tests exist; no tests for reruns, duplicate files, late files, schema changes, empty files or a killed run. Ask: Can SIT add: _v2 resend, late Cartwell file, renamed column, empty file, mid-run cancel?
- TEST-03 Automated tests run on every change (partly covered, medium): Code tests gate every PR (good); data tests are not in the pipeline. Ask: Can a CI job run the DQ and reconciliation checks in test?

**How news, decisions and problems travel**
- COM-05 Assumptions never shared with the business (missing, medium): Assumptions that are already broken or unvalidated (A-02, A-03, access in week 1) do not appear in the status report the sponsor reads. Ask: Can the status report carry the key assumptions with holding / at risk / broken each week?
- COM-02 Technical words used with business people (partly covered, medium): Requirements read well for the business; the discovery the sponsor signed states technical constraints without their business consequence. Ask: Did the sponsor understand that a 3-day outage means a full POS reload, and that customer home-region trends will restate when customers move?
- COM-03 Agreed in a meeting, lost afterwards (partly covered, medium): Meeting decisions are noted in the status report (good), but have no owner or date and were not copied into the plan, deployment plan or a decision log, which still say otherwise. Ask: Who copies meeting decisions into the plan, deployment plan and decision log, and by when?
- COM-04 Nobody knows who to call (partly covered, medium): There is a project escalation path, but no contact list for sources (POS DBA, Cartwell, Brightwave) or for a night-time failure. Ask: Who is called when the 05:00 job fails, when Cartwell files are late, or when Brightwave rejects the file? Who is each person's deputy?

**Deletes and soft deletes at the source**
- DEL-02 What a delete means downstream (missing, medium): Nobody has decided whether a voided sale must disappear from revenue, be flagged, or stay, nor what happens to a customer deleted at source. Ask: Does finance want voids removed from revenue entirely? What happens to a deleted loyalty customer in silver, gold and the marketing extract?
- DEL-03 Deletes flow through derived tables (missing, medium): Gold rebuilds only yesterday, so a delete or correction to any earlier date never reaches the facts. Ask: When a sale from three days ago is voided or corrected, which gold partitions are rebuilt?

**Documentation, knowledge transfer, support model**
- HAND-05 Benefits never measured (missing, medium): Good measurable objectives with a baseline, but no plan or owner to measure them after go-live. Ask: Who measures O1–O4 after go-live, and when?
- HAND-06 No exit criteria for early-life support (missing, medium): No early-life support period or exit criteria. Ask: What must be true (clean runs, reconciled weeks, no sev 1/2) before the project team steps back?
- HAND-02 Decision log and data dictionary not ready to hand over (partly covered, medium): The data model can grow into the data dictionary and the architecture holds decisions; no plan to keep them current for handover. Ask: Who owns keeping the data model and decision list current to production?

**Keeping history of changes (slowly changing dimensions)**
- SCD-01 Which tables keep history, and for how long (partly covered, medium): Customer is latest-only; nobody has asked finance whether FR-06's 12-month trend by home region should restate when 2% of customers move each month. Ask: Does finance accept that past sales move to a customer's new region when they move?
- SCD-03 A business key that can change (partly covered, medium): A surrogate key exists (good), but matching falls back to email, which customers change; no mapping keeps identity across that. Ask: When a customer changes email, do they become a new customer_id?
- SCD-04 Facts joined to the right version of history (partly covered, medium): 'As it is now' by design, but not confirmed as what consumers expect. Ask: Is 'as it is now' what finance wants for region trends?

**Running cost and its controls**
- COST-01 Running cost estimated from a real run (not mentioned: ask, medium): No running-cost estimate. Ask: What will the nightly job, serverless pipeline and SQL warehouse cost per month, from the week-4 run?
- COST-03 Cost can be traced to a team and a job (not mentioned: ask, low): No tagging mentioned. Ask: Does the platform's tagging standard apply to the bundle's job clusters and serverless pipeline?

## By role

**Technical anchor** (42): COM-01 Bad news held back; DEL-01 Detecting hard deletes at the source; DUP-01 Same batch or file arriving twice; EST-02 One number instead of a range; EST-04 Invisible work left out of the estimate; EST-06 Never corrected against actual progress; EST-07 History load and data fixing underestimated; HAND-01 Runbook missing or written at the end; HAND-03 Knowledge transfer never tested; HIST-01 History load scope and approach; HIST-03 Handing over from history load to incremental loads; LATE-01 Late and corrected rows rebuild the right periods; ORCH-01 Jobs wait for their data, not the clock; REC-04 First production loads reconciled; SCH-02 A column renamed, removed or retyped; SCOPE-02 The data scope traps left silent; DES-01 A thin slice proved the design end to end; DQ-05 Real data profiled before design; DUP-02 Rerunning a job changes the result; EST-01 The rough guess became the promise; EST-03 An estimate with no written assumptions; LATE-02 Facts arriving before their reference data; ORCH-03 Restart after failing in the middle; PERF-02 Freshness target measured end to end; REC-01 Counts and totals reconciled layer by layer; SERV-01 A contract with each consumer; DEL-03 Deletes flow through derived tables; HAND-06 No exit criteria for early-life support; HIST-02 Source can bear the history extract; OPS-05 Production watched closely after go-live; SCH-01 A new column appears at the source; SERV-02 Consumers can tell whether data is complete; COM-02 Technical words used with business people; HAND-02 Decision log and data dictionary not ready to hand over; HIST-04 Reloading or backfilling a past period; SCD-03 A business key that can change; SCD-04 Facts joined to the right version of history; SCH-03 Source owners warn before they change; SERV-05 Consumer queries fast enough under real load; COST-01 Running cost estimated from a real run; DBX-04 Table retention matches time travel and recovery needs; SERV-03 Changes to what consumers use are announced

**Project manager** (19): PM-01 Dates set before the dependencies were known; PM-04 Green until it is red; HAND-04 Support model not agreed; PM-02 Risks listed, not managed; SCOPE-03 Scope creep with no change process; PM-03 Decisions not written down; PM-05 Testing and deployment left to the end; STK-01 Only the sponsor is managed; PM-07 The plan ignores the estimate's assumptions; COM-05 Assumptions never shared with the business; PM-08 Open decisions with no owner, deadline or default; COM-03 Agreed in a meeting, lost afterwards; COM-04 Nobody knows who to call; PM-06 Key-person risk; SCOPE-04 "Phase 2" used as a hiding place; SCOPE-05 MVP 1 is too big; SCOPE-06 Scope not signed by the business owner; STK-04 Conflicts left unsaid; STK-05 Sign-off without reading

**Business analyst** (12): REQ-03 Business definitions not agreed and signed; REQ-01 Vague words in the requirements; REQ-02 No acceptance criteria; SCOPE-01 Scope written only as "in"; DUP-03 Duplicates already inside the source; REQ-04 Requirements written without looking at the data; REQ-06 Non-functional needs missing; SERV-04 Business definitions live in one place; DEL-02 What a delete means downstream; REQ-05 The users are not the requesters; SCD-01 Which tables keep history, and for how long; LATE-04 Time zones and business dates

**Developers** (10): ORCH-06 Stream restarts from where it stopped; DBX-06 Job retries, concurrency and repair are safe; DBX-05 Auto Loader schema evolution mode chosen per source; DQ-03 One poison record does not stop the whole load; OPS-03 Every run leaves a record; PERF-05 Storage layout and file sizes kept healthy; TEST-03 Automated tests run on every change; ORCH-02 Retries for passing failures only; ORCH-04 Two runs writing the same table at once; PERF-04 Skewed keys and very large joins

**Test lead** (6): REC-02 Matched against a number the business already trusts; PERF-03 Tested at production volume; TEST-01 Test levels that include data tests; TEST-02 Realistic, safe test data; TEST-04 Users test with numbers they recognise; TEST-05 Failure, rerun and recovery tested on purpose

**Security and governance (not on the team: technical anchor by default)** (4): REL-05 No secrets in the repository; SEC-01 Personal and sensitive data found and classified; SEC-02 Who can see what; SEC-03 Retention and the right to be forgotten

**Architect (not on the team: technical anchor by default)** (3): ORCH-05 Recovery time and data loss limits; DES-02 Non-functional needs written as numbers; DES-06 Batch or streaming chosen for a reason

**Platform team (not on the team: technical anchor by default)** (2): ENV-03 Network path to every source proven early; COST-03 Cost can be traced to a team and a job

**Operations and support (not on the team: technical anchor by default)** (2): DQ-04 A source goes quiet or sends far too little; OPS-01 Alerts reach someone who can act

**Business owner and sponsor** (2): HAND-05 Benefits never measured; REC-03 Tolerances and who signs off differences

**Release and DevOps (not on the team: technical anchor by default)** (1): REL-07 Rolling back a release, including its data

## Done well

DES-04 Grain and keys of every table; DQ-01 Data quality rules written with owners; DQ-02 What happens to a row that fails a rule; ENV-02 Access through groups and service identities; PM-10 Access and environments treated as admin; REL-01 Everything that runs is in version control; REL-03 Automated promotion of the same build; SCD-02 History rows stay correct on reruns and out-of-order changes; STK-02 Nobody clearly owns the decisions; STK-03 No real numbers shown to the business; COST-04 No compute running when nothing needs it; DBX-07 Pipeline expectations with the right action; DBX-08 Promotion through bundles, run as service principals; ENV-05 Project fits the existing platform's standards; EST-05 Guessed, not counted; PERF-01 Volumes and growth stated; PM-09 Discovery with no timebox; REL-02 Branching and code review; REL-04 Configuration per environment, not in code; REQ-07 Goals with no measure of success; COM-06 No regular rhythm for updates; STK-06 Success not defined for each stakeholder

---
Made with data-project-review. Statuses come from the documents provided; "Not mentioned" means the documents are silent, not that the work isn't done.