# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Pick the checks that apply to one project, and what each should look like at its current stage.

    uv run scripts/select.py path/to/project.yaml            # writes worksheet.json next to project.yaml
    uv run scripts/select.py path/to/project.yaml --md       # also prints a readable list

No AI here on purpose: the same profile always gets the same checklist. Claude fills in the evidence.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog as cat  # noqa: E402


def worksheet(prof):
    stage = int(prof["stage"])
    binds = cat.bindings()
    techs = [t for t in prof.get("tech") or [] if t in binds]
    pool = cat.checks() + [c for t in techs for c in binds[t].get("checks") or []]
    rows = []
    for c in pool:
        if not cat.applies(c, prof):
            continue
        now, nxt = cat.expectation(c, stage)
        how = {t: binds[t]["how"][c["id"]] for t in techs if c["id"] in (binds[t].get("how") or {})}
        rows.append({
            "id": c["id"], "title": c["title"], "kind": c["kind"], "concern": c["concern"],
            "question": c["question"], "why": c.get("why"), "owner": c["owner"], "also": c.get("also", []),
            "severity": c.get("severity", "medium"), "evidence": c.get("evidence", {}),
            "signals": c.get("signals", []), "contradiction": c.get("contradiction"),
            "signal_id": c.get("signal_id"), "fail_fast": c.get("fail_fast"),
            "expected_now": now, "coming_up": {"level": nxt[0], "stage": nxt[1]} if nxt else None,
            "binding": how or None, "tech_only": c.get("binding"),
            "status": None, "evidence_found": [], "note": None,   # Claude fills these in
        })
    order = {"high": 0, "medium": 1, "low": 2}
    rows.sort(key=lambda r: (r["expected_now"] is None, order.get(r["severity"], 1), r["id"]))
    return {"project": prof.get("name"), "stage": stage, "stage_name": cat.stages()[stage]["name"],
            "kind": prof.get("kind"), "tech": techs, "checks": rows}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    prof = cat.project(sys.argv[1])
    ws = worksheet(prof)
    out = prof["_dir"] / "worksheet.json"
    out.write_text(json.dumps(ws, indent=2, ensure_ascii=False))
    due = sum(1 for r in ws["checks"] if r["expected_now"])
    print(f"{len(ws['checks'])} checks apply ({due} due at stage {ws['stage']} {ws['stage_name']}, "
          f"{len(ws['checks']) - due} coming up) -> {out}")
    if "--md" in sys.argv:
        for r in ws["checks"]:
            when = f"expected now: {r['expected_now']}" if r["expected_now"] else \
                f"coming up: {r['coming_up']['level']} by stage {r['coming_up']['stage']}" if r["coming_up"] else "no stage set"
            print(f"- {r['id']} [{r['severity']}] {r['title']} ({r['owner']}; {when})")


if __name__ == "__main__":
    main()
