# Design

Written 1 November 2026, from the design conversation with the owner.

## The problem

A data engineering team, building a new platform or a project on an existing one, has a set of project
documents. They might be in discovery or in the middle of build. Projects rarely fail because a developer
couldn't write the code. They fail because something nobody owned slipped through: a file that arrives twice,
a history load nobody estimated, a definition of revenue nobody signed, a plan that assumed access in week one
when approval takes six weeks. We want a bundle a team can hand to Claude with their documents, which tells them
what they are missing, at their stage, and how to fail fast.

## The idea

Package an experienced reviewer. They learn the project, pick the right checklist for it, look for evidence in
the documents, compare the documents with each other, and say what is missing in order of danger, with the
cheapest test to run now.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Generic vs specific | Three layers: common checks (no product names), applicability tags, technology bindings | Today Databricks, tomorrow something else: a new technology is one binding file. Same pattern as the AI Assurance and AI Harness Catalogs (archetype, obligation, mechanism) |
| Unknown project details | Checks are failure patterns detected three ways: signals in documents, contradictions between documents, silence turned into a question and a pre-mortem | We can't know the project, but the ways projects fail are the same everywhere |
| Any stage | Each check states by which lifecycle stage each level (plan, designed, evidenced, proven) is due | A team in discovery is judged on plans; a team in test on evidence. Not-yet-due items are "coming up", not findings |
| Roles | Every check has an owner role; the report groups gaps by role | Technical anchor, architect, BA, PM, test, release, operations, security each see their part |
| Deterministic first | Scripts pick the checks, scan for mechanical signals, lint the catalog and build the report; Claude does the reading and judging | The same project always gets the same checklist; the model is used only where judgement is needed |
| Proof | A sample project with planted gaps and a hidden answer key; a scorer | A repeatable score before any real team relies on it |
| Where it runs | One folder that is both a Claude Code skill and an uploadable claude.ai skill | No install beyond uv or PyYAML |

## How it relates to Clean Data Engineering

The Clean Data Engineering plan proposes a Data Assurance Catalog (what must be true of a data platform) and a
Data Platform Catalog (what must exist). The common checks here are a first, project-facing version of the Data
Assurance Catalog, with stable ids so they can be carried over.

## Next

1. Run the skill blind on the sample project and record the score in `tests/RESULTS.md`.
2. Run it on a real project's documents.
3. Grow the catalog from what the real runs miss; add bindings for other technologies.
