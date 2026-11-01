# Data requirements: [project name]

Version: [n] · Date: [date] · Signed by business owner: [name, date]

## What good looks like

Data requirements say, in business terms, which data the project needs and how it must behave, before anyone designs tables. Every source is named with a system and a person who owns it. For each need, the grain the users want is compared with the grain the source really holds, checked against a real extract rather than assumed. History depth and freshness are numbers, each tied to the decision that needs them, so their cost can be weighed against their value. When two systems disagree, a written decision says which wins. When data arrives late or is corrected, the business has said what may change and when a period is closed. Retention, privacy purpose and audit needs are stated from the business side so the design can meet them.

## Sources

| # | Source system | Business data it provides | Source owner (person) | Business data owner | Requirement ids | Access requested? | Profiled? |
|---|---|---|---|---|---|---|---|
| S1 | | | | | | Yes / No, date | Yes / No |

## Needs per requirement

| Req id | Decision it serves | Grain needed | Grain the source holds | Gap and resolution | History needed (years) and why | Freshness (time of day or delay) and why |
|---|---|---|---|---|---|---|
| R-1 | | | | | | |

## Source of truth when systems disagree

| Entity | Sources holding it | Which wins, for which fields | Record in only one source | Decided by |
|---|---|---|---|---|
| Customer | | | | |

## Late and corrected data

| Question | Answer |
|---|---|
| Which date puts a record into a period, per measure? | |
| How far back may corrections change published figures? | |
| When is a period closed and never restated? | |
| How are users told a past figure changed? | |

## As it was, or as it is now

| Attribute that can change | Report past figures under the value at the time, the current value, or both? | Agreed example |
|---|---|---|
| [customer region] | | |

## Volumes (business view)

| Data | Today (per day or month) | Expected in two to three years | What drives growth |
|---|---|---|---|
| | | | |

## Policy needs

| Data kind | Personal data? | Purpose and basis | Keep for | Must be reproducible as reported? | Privacy / compliance sign-off |
|---|---|---|---|---|---|
| | Yes / No | | | Yes / No, for how long | name, date |
