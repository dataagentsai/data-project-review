# Release and cut-over plan: [project name] · [release / MVP]

Version: [n] · Go-live date: [date] · Owners: [technical anchor], [release manager] · Accepted by operations: [name, date]

## What good looks like

The release route was working from the first weeks of build, so go-live is not the first real deployment. The cut-over and the rollback have both been rehearsed in a production-like environment, with timings. The history load is planned and timed, and its numbers are checked with the business. Monitoring and alerts are switched on before go-live, operations have run a failure drill using the runbook, and there are written criteria for ending early-life support that include at least one full business cycle (for example a month-end).

## 1. What is released

| Component | Version | Change from current production |
|---|---|---|
| | | |

## 2. Before go-live (checklist)

- [ ] Release route used for at least [n] earlier deployments
- [ ] Cut-over rehearsed on [date], took [time]
- [ ] Rollback rehearsed on [date], took [time]
- [ ] History load run in pre-production, took [time], reconciled with [name]
- [ ] Monitoring and alerts on, tested by forcing a failure
- [ ] Runbook reviewed by operations; failure drill done on [date]
- [ ] Access for users requested and approved
- [ ] Support model signed (see runbook)
- [ ] Source owners told of go-live date and extract load

## 3. Cut-over steps

| # | Step | Who | Start | Expected duration | Check that it worked | Go / no-go point? |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

## 4. Rollback

Trigger for rollback: [ ] · Who decides: [one name] · Steps: [ ] · Latest time rollback is still possible: [ ]

## 5. History load

Years: [n] · Order and batches: [ ] · Expected time: [ ] · Reconciled against: [ ] · Signed off by: [ ]

## 6. Early-life support (hypercare)

| Exit criterion | Target | Met on |
|---|---|---|
| Clean scheduled runs in a row | [n] | |
| Production loads reconciled | [n] | |
| Business cycle completed in production (for example month-end) | [which] | |
| Open critical defects | 0 | |
| Operations confirm they can run it alone | Yes | |

## 7. Communication on the day

Who is told at each go / no-go point: [list] · Channel: [ ] · Message if rolled back: [ ]
