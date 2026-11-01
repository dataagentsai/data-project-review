# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Turn the worksheet (from select.py) and Claude's review.json into one readable report.

    uv run scripts/report.py path/to/project.yaml       # reads worksheet.json + review.json, writes REVIEW.md

review.json shape (Claude writes it, see SKILL.md step 6):
{
  "summary": "two or three plain sentences",
  "checks": {"DUP-01": {"status": "missing", "evidence": [{"doc": "architecture.md", "section": "Ingestion",
              "quote": "..."}], "note": "why this status", "ask": "question for the team, if any"}},
  "contradictions": [{"docs": ["plan.md", "raid-log.md"], "issue": "...", "checks": ["PM-01"]}],
  "fail_fast_plan": [{"risk": "...", "test": "...", "kill_line": "...", "owner": "technical-anchor", "by": "this week"}],
  "premortem": ["most likely reasons this project fails, from the evidence"]
}
Statuses: covered, partly, missing, contradicts, unknown (documents are silent: ask), not-applicable.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog as cat  # noqa: E402

RANK = {"contradicts": 0, "missing": 1, "partly": 2, "unknown": 3, "covered": 4, "not-applicable": 5}
SEV = {"high": 0, "medium": 1, "low": 2}
TOP = 15   # how many gaps the top table shows; the rest are listed by concern
LABEL = {"contradicts": "Documents disagree", "missing": "Missing", "partly": "Partly covered",
         "unknown": "Not mentioned: ask", "covered": "Covered", "not-applicable": "Not applicable"}


def md_escape(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def build(prof):
    d = prof["_dir"]
    ws = json.loads((d / "worksheet.json").read_text())
    rv = json.loads((d / "review.json").read_text())
    roles = cat.roles()
    got = rv.get("checks", {})
    rows = []
    for c in ws["checks"]:
        r = got.get(c["id"], {})
        rows.append({**c, "status": r.get("status", "unknown" if c["expected_now"] else None),
                     "ev": r.get("evidence", []), "note": r.get("note"), "ask": r.get("ask")})
    due = [r for r in rows if r["expected_now"]]
    later = [r for r in rows if not r["expected_now"]]
    gaps = sorted([r for r in due if r["status"] in ("contradicts", "missing", "partly", "unknown")],
                  key=lambda r: (SEV.get(r["severity"], 1), RANK.get(r["status"], 9), r["id"]))
    counts = {k: sum(1 for r in due if r["status"] == k) for k in RANK}

    L = [f"# Project review: {prof.get('name', '')}", "",
         f"Stage {ws['stage']}, {ws['stage_name']} · {ws['kind']} · technology: {', '.join(ws['tech']) or 'none bound'} · "
         f"{len(due)} checks due now, {len(later)} coming up", "", rv.get("summary", ""), "",
         "| Covered | Partly | Missing | Documents disagree | Not mentioned |", "|---|---|---|---|---|",
         f"| {counts['covered']} | {counts['partly']} | {counts['missing']} | {counts['contradicts']} | {counts['unknown']} |", ""]
    if rv.get("fail_fast_plan"):
        L += ["## Fail fast: do these first", "", "| Risk | Cheapest test now | Kill line (what would change the plan) | Owner | By |",
              "|---|---|---|---|---|"]
        L += [f"| {md_escape(x.get('risk'))} | {md_escape(x.get('test'))} | {md_escape(x.get('kill_line'))} | "
              f"{roles.get(x.get('owner'), {}).get('name', x.get('owner', ''))} | {md_escape(x.get('by'))} |" for x in rv["fail_fast_plan"]]
        L.append("")
    if rv.get("premortem"):
        L += ["## Pre-mortem: the most likely ways this project fails", ""] + [f"{i}. {p}" for i, p in enumerate(rv["premortem"], 1)] + [""]
    if rv.get("contradictions"):
        L += ["## Where the documents disagree", ""]
        L += [f"- **{' vs '.join(x.get('docs', []))}:** {x.get('issue')} ({', '.join(x.get('checks', []))})" for x in rv["contradictions"]]
        L.append("")
    have = set(prof.get("roles") or [])

    def who(role):
        name = roles.get(role, {}).get("name", role)
        return name if not have or role in have else f"{name} (not on the team: technical anchor by default)"

    top = [r for r in gaps if r["status"] in ("contradicts", "missing")][:TOP]
    L += [f"## The {len(top)} most serious gaps", "", "| Check | Severity | Status | What we found | Owner | Ask |", "|---|---|---|---|---|---|"]
    for r in top:
        ev = "; ".join(f"{e.get('doc')}{' § ' + e['section'] if e.get('section') else ''}" for e in r["ev"])
        L.append(f"| **{r['id']}** {md_escape(r['title'])} | {r['severity']} | {LABEL[r['status']]} | "
                 f"{md_escape(r['note'])}{' (' + md_escape(ev) + ')' if ev else ''} | {who(r['owner'])} | "
                 f"{md_escape(r['ask'] or r['question'])} |")
    L.append("")
    rest = [r for r in gaps if r not in top]
    if rest:
        concerns = {**cat.vocab()["concerns"]["technical"], **cat.vocab()["concerns"]["delivery"]}
        L += [f"## All other gaps ({len(rest)}), by concern", ""]
        groups = {}
        for r in rest:
            groups.setdefault(r["concern"], []).append(r)
        for con, rs in groups.items():
            L.append(f"**{concerns.get(con, con)}**")
            L += [f"- {r['id']} {r['title']} ({LABEL[r['status']].lower()}, {r['severity']}): {r['note'] or r['question']}"
                  + (f" Ask: {r['ask']}" if r.get("ask") else "") for r in rs]
            L.append("")
    by_role = {}
    for r in gaps:
        by_role.setdefault(r["owner"], []).append(r)
    L += ["## By role", ""]
    for role, rs in sorted(by_role.items(), key=lambda x: -len(x[1])):
        L.append(f"**{who(role)}** ({len(rs)}): " + "; ".join(f"{r['id']} {r['title']}" for r in rs))
        L.append("")
    covered = [r for r in due if r["status"] == "covered"]
    if covered:
        L += ["## Done well", "", "; ".join(f"{r['id']} {r['title']}" for r in covered), ""]
    if later:
        L += ["## Coming up at later stages", ""]
        L += [f"- {r['id']} {r['title']}: {r['coming_up']['level']} by stage {r['coming_up']['stage']}" for r in later if r["coming_up"]]
        L.append("")
    L += ["---", "Made with data-project-review. Statuses come from the documents provided; "
          "\"Not mentioned\" means the documents are silent, not that the work isn't done."]
    return "\n".join(L)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    prof = cat.project(sys.argv[1])
    out = prof["_dir"] / "REVIEW.md"
    out.write_text(build(prof))
    print("report ->", out)


if __name__ == "__main__":
    main()
