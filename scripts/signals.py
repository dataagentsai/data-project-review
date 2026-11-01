# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Scan a project's documents for gaps a script can find reliably, without AI.

    uv run scripts/signals.py path/to/project.yaml          # writes signals.json next to project.yaml

Each detector returns findings with the document and line, so Claude can quote them. A detector firing is
a signal to look closer, not a verdict: Claude confirms each one against the documents before reporting it.
Detectors read Markdown and plain text. Convert other formats (docx, pdf) to text first.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog as cat  # noqa: E402

VAGUE = ["real-time", "real time", "near real-time", "near real time", "fast", "quickly", "as soon as possible", "asap",
         "all data", "all historical", "all history", "user-friendly", "user friendly", "seamless", "robust", "scalable",
         "as needed", "as required", "minimal", "appropriate", "etc", "and so on", "high quality", "timely", "intuitive",
         "efficient", "flexible", "easy"]
NUMBER = re.compile(r"\d")
IDS = re.compile(r"\b[A-Z][A-Z0-9]*-\d+\b")
TOTAL = re.compile(r"\b(?:total|overall|duration|estimate[ds]?|effort|delivery|timeline|in total)\b", re.I)
UNIT = re.compile(r"\b\d+(?:\.\d+)?\s*(?:weeks?|days?|months?|sprints?|person[- ]days?|hours?)\b", re.I)
RANGE = re.compile(r"\b\d+(?:\.\d+)?\s*(?:-|–|—|to)\s*\d+(?:\.\d+)?\b")
INVISIBLE = {"testing": r"\btest", "environments": r"environment", "access": r"\baccess\b",
             "data fixes / data quality": r"data (?:fix|quality|issue)|bad data", "cut-over / go-live": r"cut-?over|go-?live",
             "handover / knowledge transfer": r"hand-?over|knowledge transfer|\bkt\b", "deployment / release": r"deploy|release",
             "documentation": r"document"}


def docs_of(prof, *types):
    """[(doc_type, path, lines)] for the given doc types that exist."""
    out = []
    for t in types:
        files = (prof.get("docs") or {}).get(t) or []
        for f in [files] if isinstance(files, str) else files:
            p = (prof["_dir"] / f).resolve()
            if p.exists():
                out.append((t, p, p.read_text(encoding="utf-8", errors="replace").splitlines()))
    return out


def rel(prof, p):
    try:
        return str(Path(p).relative_to(prof["_dir"].resolve()))
    except ValueError:
        return str(p)


def hit(prof, p, i, line):
    return {"doc": rel(prof, p), "line": i + 1, "text": line.strip()[:220]}


def vague_words(prof):
    found = []
    for _, p, lines in docs_of(prof, "requirements", "discovery"):
        for i, line in enumerate(lines):
            low = line.lower()
            words = [w for w in VAGUE if re.search(r"(?<![a-z-])" + re.escape(w) + r"(?![a-z-])", low)]
            if words and not NUMBER.search(IDS.sub("", line)):   # ignore ids like FR-10 / NFR-01 when looking for a number
                found.append({**hit(prof, p, i, line), "words": words})
    return found


def single_number_estimate(prof):
    """Flag headline totals ("Total: 12 weeks") given as one number. Ranges elsewhere (sizing tables, staffing
    week spans) don't count: what matters is whether the number people will quote is a range."""
    out = []
    for _, p, lines in docs_of(prof, "estimate"):
        heads = [(i, l) for i, l in enumerate(lines) if TOTAL.search(l) and UNIT.search(l)]
        if heads:
            if not any(RANGE.search(l) for _, l in heads):
                out += [{**hit(prof, p, i, l), "note": "headline figure given as a single number"} for i, l in heads[:5]]
        elif not any(RANGE.search(l) for l in lines):
            out.append({"doc": rel(prof, p), "line": None, "text": "No range (like '8-11 weeks') anywhere in the estimate."})
    return out


def no_assumptions(prof):
    ds = docs_of(prof, "estimate")
    return [{"doc": rel(prof, p), "line": None, "text": "The estimate never states its assumptions."}
            for _, p, lines in ds if not any(re.search(r"assum", l, re.I) for l in lines)]


def no_out_of_scope(prof):
    ds = docs_of(prof, "requirements", "discovery", "plan", "architecture")
    pat = re.compile(r"out[- ]of[- ]scope|not in scope|excluded|exclusions|outside (?:the )?scope|won'?t (?:do|have)", re.I)
    if any(pat.search(l) for _, _, lines in ds for l in lines):
        return []
    return [{"doc": None, "line": None, "text": "No out-of-scope list in requirements, discovery, plan or architecture."}]


def table_rows(lines):
    """Yield (header cells, row cells, line index) for Markdown tables."""
    header = None
    for i, l in enumerate(lines):
        if l.strip().startswith("|"):
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if header is None:
                header = [c.lower() for c in cells]
            elif not set("".join(cells)) <= set("-: "):
                yield header, cells, i
        else:
            header = None


def risks_without_owner(prof):
    found = []
    for _, p, lines in docs_of(prof, "raid"):
        saw_owner_col = False
        for header, cells, i in table_rows(lines):
            if "owner" not in header:
                continue
            saw_owner_col = True
            v = cells[header.index("owner")] if header.index("owner") < len(cells) else ""
            if v.strip().lower() in ("", "-", "–", "tbd", "tbc", "n/a", "?", "team", "all"):
                found.append({**hit(prof, p, i, lines[i]), "owner": v})
        if not saw_owner_col:
            found.append({"doc": rel(prof, p), "line": None, "text": "The RAID log has no owner column."})
    return found


def no_decision_log(prof):
    if docs_of(prof, "decisions"):
        return []
    for _, p, lines in docs_of(prof, *cat.vocab()["doc_types"]):
        if any(re.match(r"\s*#+\s*.*decision (?:log|record|register)", l, re.I) for l in lines):
            return []
    return [{"doc": None, "line": None, "text": "No decision log or decision records found."}]


def no_acceptance_criteria(prof):
    ds = docs_of(prof, "requirements")
    pat = re.compile(r"acceptance|\bgiven\b.*\bwhen\b|done when|definition of done", re.I)
    return [{"doc": rel(prof, p), "line": None, "text": "Requirements have no acceptance criteria."}
            for _, p, lines in ds if not any(pat.search(l) for l in lines)]


def missing_doc_type(prof):
    have = prof.get("docs") or {}
    out = []
    for t, desc in cat.vocab()["doc_types"].items():
        files = have.get(t)
        files = [files] if isinstance(files, str) else (files or [])
        if not files or not any((prof["_dir"] / f).exists() for f in files):
            out.append({"doc": None, "line": None, "doc_type": t, "text": f"No {t} document ({desc})."})
    return out


def no_invisible_work(prof):
    ds = docs_of(prof, "estimate")
    if not ds:
        return []
    text = "\n".join(l for _, _, lines in ds for l in lines).lower()
    missing = [k for k, rx in INVISIBLE.items() if not re.search(rx, text)]
    return [{"doc": rel(prof, ds[0][1]), "line": None, "missing": missing,
             "text": "The estimate has no lines for: " + ", ".join(missing) + "."}] if missing else []


def status_always_green(prof):
    out = []
    for _, p, lines in docs_of(prof, "status"):
        text = "\n".join(lines).lower()
        green = len(re.findall(r"\bgreen\b", text))
        amber_red = len(re.findall(r"\b(?:amber|red|at risk|off track)\b", text))
        trouble = [hit(prof, p, i, l) for i, l in enumerate(lines)
                   if re.search(r"slip|behind|delay|late\b|blocked|overrun|not started", l, re.I)]
        if green and not amber_red:
            out.append({"doc": rel(prof, p), "line": None,
                        "text": f"Status is green everywhere ({green} times) with no amber or red"
                                + (f", while {len(trouble)} lines mention slips, delays or blocks." if trouble else "."),
                        "trouble_lines": trouble[:8]})
    return out


DETECTORS = {
    "vague-words": vague_words, "single-number-estimate": single_number_estimate, "no-assumptions": no_assumptions,
    "no-out-of-scope": no_out_of_scope, "risks-without-owner": risks_without_owner, "no-decision-log": no_decision_log,
    "no-acceptance-criteria": no_acceptance_criteria, "missing-doc-type": missing_doc_type,
    "no-invisible-work": no_invisible_work, "status-always-green": status_always_green,
}


def run(prof):
    by_signal = {}
    for c in cat.checks():
        if c.get("signal_id"):
            by_signal.setdefault(c["signal_id"], []).append(c["id"])
    out = []
    for sid, fn in DETECTORS.items():
        found = fn(prof)
        if not found:
            continue
        ids = by_signal.get(sid, [])
        if sid == "missing-doc-type":   # link each missing document only to the checks about that document
            first = {c["id"]: ((c.get("evidence") or {}).get("docs") or [None])[0] for c in cat.checks()}
            for f in found:
                f["checks"] = [i for i in ids if first.get(i) == f["doc_type"]]
            ids = sorted({i for f in found for i in f["checks"]})
        out.append({"signal": sid, "checks": ids, "count": len(found), "findings": found})
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    prof = cat.project(sys.argv[1])
    res = run(prof)
    out = prof["_dir"] / "signals.json"
    out.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    for r in res:
        print(f"- {r['signal']}: {r['count']} finding(s) -> checks {', '.join(r['checks']) or '(none mapped)'}")
    print(f"{len(res)} of {len(DETECTORS)} detectors fired -> {out}")


if __name__ == "__main__":
    main()
