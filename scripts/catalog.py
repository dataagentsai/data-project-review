"""Shared loader for the catalog, bindings and a project's profile. Imported by the other scripts."""
import json
from functools import lru_cache
from pathlib import Path

try:
    import yaml           # normal path: read the YAML sources
except ImportError:       # claude.ai and other places where packages can't be installed: read catalog.json
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
CAT = ROOT / "core"          # shared vocabulary, stages, roles, schema
PACKS = ROOT / "packs"       # one folder per discipline: ba, pm, tech
LEVELS = ["plan", "designed", "evidenced", "proven"]


def load_yaml(p):
    if yaml is None:
        raise SystemExit(f"PyYAML is not installed, so {p} can't be read. Use `uv run`, `pip install pyyaml`, "
                         "or JSON files (catalog.json, project.json).")
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=1)
def _json():
    """The exported catalog, used when PyYAML is missing. Refresh it with scripts/export.py."""
    p = ROOT / "catalog.json"
    if not p.exists():
        raise SystemExit("PyYAML is not installed and catalog.json is missing. Run `uv run scripts/export.py` first.")
    return json.loads(p.read_text(encoding="utf-8"))


def vocab():
    return load_yaml(CAT / "vocab.yaml") if yaml else _json()["vocab"]


def stages():
    src = load_yaml(CAT / "stages.yaml")["stages"] if yaml else _json()["stages"]
    return {int(k): v for k, v in src.items()}


def roles():
    return load_yaml(CAT / "roles.yaml")["roles"] if yaml else _json()["roles"]


def checks(packs=None):
    """Every common check, in file order, from every pack (or only the packs named). Adds `pack` and `_file`."""
    if yaml is None:
        return [dict(c, _file=c.get("file")) for c in _json()["checks"] if not packs or c.get("pack") in packs]
    out = []
    for d in sorted(PACKS.iterdir()):
        if not d.is_dir() or (packs and d.name not in packs):
            continue
        for p in sorted((d / "checks").rglob("*.yaml")):
            for c in load_yaml(p) or []:
                c["pack"] = d.name
                c["_file"] = str(p.relative_to(ROOT))
                out.append(c)
    return out


def bindings():
    """{tech: binding dict}. Technology-only checks get `binding` and `_file` set."""
    if yaml is None:
        return {t: {"tech": t, "name": b["name"], "version_note": b.get("version_note"), "how": b["how"],
                    "checks": [dict(c, binding=t, _file=c.get("file")) for c in b["checks"]]} for t, b in _json()["bindings"].items()}
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
    prof = json.loads(p.read_text(encoding="utf-8")) if p.suffix == ".json" else load_yaml(p)
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
