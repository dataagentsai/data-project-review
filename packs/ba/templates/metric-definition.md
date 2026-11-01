# Metric definition: [metric name]

Version: [n] · Date: [date] · Owner: [name, role] · Signed: [name, date]

## What good looks like

A metric definition is complete when two people who have never spoken could calculate it separately from this card and get the same number. It states the formula in words and symbols, everything included and excluded, the grain, the date that puts a record into a period, the calendar, and the currency or unit. It says how the metric adds up across days, regions and products, because ratios, distinct counts and balances do not simply add. It has a worked example with real numbers that matches a figure the business already trusts. It is owned and signed by one named business person, and any department that uses the same word with a different meaning is listed below with the decision taken.

## Definition

| Field | Answer |
|---|---|
| Plain definition (one sentence a new starter would understand) | |
| Formula | [for example: sum of invoice line amount, excluding tax, minus credit notes] |
| Included | [order types, channels, entities, statuses] |
| Excluded | [test and internal accounts, cancellations, intercompany, staff purchases] |
| Grain (what one value is for) | [for example: one value per store per day] |
| Date that decides the period | Order / shipment / invoice / posting date |
| Calendar | Calendar months / fiscal periods [give the fiscal year start] / weeks starting [day] |
| Time zone for the business day | |
| Currency or unit, and conversion rule | [currency; which exchange rate: daily, month-end, budget rate] |
| Adds up how? | Additive / adds across [dimensions] but not across time / not additive: recalculate from [parts] |
| Late and corrected data | [may past periods change? until when? which periods are closed?] |
| Sources and fields | [system.table.field for each part of the formula] |
| Requirement ids | [R-..] |

## Worked example

| Period and slice | Inputs | Result | Matches trusted figure? |
|---|---|---|---|
| [for example: March, North region] | [values] | [value] | [report name and value] |

## Other definitions in use

| Department | Their definition | Difference | Decision: one definition, or a separately named measure | Decided by |
|---|---|---|---|---|
| | | | | |

## Change history

| Version | Date | Change | Effect on past figures | Approved by |
|---|---|---|---|---|
| 1 | | First version | | |
