# Test strategy: [project name]

Version: [n] · Date: [date] · Owners: [technical anchor], [test lead] · Agreed by business users: [names, date]

## What good looks like

Written in discovery, not "to be defined". Every requirement traces to at least one test, and every test traces to a requirement. Numbers are reconciled from source to report, data quality rules run on every load, performance is proven at real volume, and a rerun never doubles anything. Business users test with real numbers they recognise, against figures they already trust. Test environments and test data are requested early, because they are dependencies like any other. Testing starts with the thin slice in the first weeks of build, not after it.

## 1. Reconciliation (do the numbers match from source to report?)

| What is compared | Source figure | Target figure | Tolerance | When it runs | Who signs the result |
|---|---|---|---|---|---|
| [row counts per day] | | | [0] | [every load] | |
| [total amount per month] | | | | | |

## 2. Data quality rules

| Rule | Table / field | What happens to a failing row (reject / quarantine / flag) | Who is told | Who fixes |
|---|---|---|---|---|
| | | | | |

## 3. Performance and freshness

- Real volume used for the test: [rows, size, number of days]
- Freshness target from requirements: [for example: ready by 7 a.m.] · Measured result: [ ]
- History load timed at: [ ] · Load on the source during extract checked with: [source owner]

## 4. Reruns and recovery

- Same input loaded twice: counts and totals must not change. Result: [ ]
- Failure in the middle of a load, then restart. Result: [ ]
- Late or corrected data reprocessed. Result: [ ]

## 5. User acceptance

| Requirement id | Business tester (name) | Figure they already trust | Result | Date |
|---|---|---|---|---|
| R-1 | | | Pass / Fail | |

Testers' availability agreed with: [business owner, dates]

## 6. Test environments and test data

| Environment | Ready by | Data in it (real / masked / made-up) | Owner |
|---|---|---|---|
| Test | | | |
| Pre-production (production-like) | | | |

Personal data in test: [masked how, approved by whom]

## 7. When testing happens

Thin slice tested by: [week] · Definition of done includes tests passing and deployment: Yes / No · Regression run on every change: [how]
