"""Shared loader for the catalog, bindings and a project's profile. Imported by the other scripts."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CAT = ROOT / "catalog"
LEVELS = ["plan", "designed", "evidenced", "proven"]


def load_yaml(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def vocab():
    return load_yaml(CAT / "vocab.yaml")


def stages():
    return {int(k): v for k, v in load_yaml(CAT / "stages.yaml")["stages"].items()}


def roles():
    return load_yaml(CAT / "roles.yaml")["roles"]


def checks():
    """Every common check, in file order. Returns a list of dicts with `_file` added."""
    out = []
    for p in sorted((CAT / "checks").rglob("*.yaml")):
        for c in load_yaml(p) or []:
            c["_file"] = str(p.relative_to(ROOT))
            out.append(c)
    return out


def bindings():
    """{tech: binding dict}. Technology-only checks get `binding` and `_file` set."""
    out = {}
    for p in sorted((ROOT / "bindings").glob("*.yaml")):
        b = load_yaml(p) or {}
        tech = b.get("tech", p.stem)
        for c in b.get("checks") or []:
            c.setdefault("binding", tech)
            c["_file"] = str(p.relative_to(ROOT))
        out[tech] = b
    return out


def project(path):
    p = Path(path)
    prof = load_yaml(p)
    prof["_dir"] = p.parent
    prof.setdefault("roles", prof.get("roles_present") or [])   # accept either name
    return prof


def applies(check, prof):
    """Does this check apply to this project? `any` matches everything."""
    a = check.get("applies") or {}

    def hit(field, values):
        want = a.get(field) or ["any"]
        return "any" in want or bool(set(want) & set(values or []))

    return (hit("kind", [prof.get("kind")]) and hit("components", prof.get("components"))
            and hit("patterns", prof.get("patterns")))


def expectation(check, stage):
    """(expected level now or None, (next level, stage it becomes due) or None)."""
    due = check.get("due") or {}
    now, nxt = None, None
    for lv in LEVELS:
        s = due.get(lv)
        if s is None:
            continue
        if s <= stage:
            now = lv
        elif nxt is None:
            nxt = (lv, s)
    return now, nxt
