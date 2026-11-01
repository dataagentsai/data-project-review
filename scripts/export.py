# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Write the whole catalog (vocabulary, stages, roles, checks, bindings) as one JSON file.

    uv run scripts/export.py            # writes catalog.json at the repo root

Other tools (the cleandataengineering.ai catalog page, dashboards, other agents) read catalog.json, so they need
no YAML parser and always see the same catalog as the skill.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog as cat  # noqa: E402


def strip(c):
    return {k: v for k, v in c.items() if not k.startswith("_")} | {"file": c.get("_file")}


def main():
    binds = cat.bindings()
    out = {
        "vocab": cat.vocab(), "stages": {str(k): v for k, v in cat.stages().items()}, "roles": cat.roles(),
        "checks": [strip(c) for c in cat.checks()],
        "bindings": {t: {"name": b.get("name", t), "version_note": b.get("version_note"), "how": b.get("how") or {},
                         "checks": [strip(c) for c in b.get("checks") or []]} for t, b in binds.items()},
    }
    p = cat.ROOT / "catalog.json"
    p.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    n = len(out["checks"]) + sum(len(b["checks"]) for b in out["bindings"].values())
    print(f"{n} checks -> {p}")


if __name__ == "__main__":
    main()
