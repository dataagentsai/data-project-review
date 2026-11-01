"""Build one claude.ai upload (zip) per skill. Plain Python, no packages needed.

    python3 scripts/package.py          # writes dist/<skill>.zip for every folder in skills/

claude.ai wants a zip whose top level is the skill folder (my-skill/SKILL.md). A skill there can't see files outside
its own folder, so each zip gets its own copy of what the skills share: core/, packs/, bindings/, scripts/ and
catalog.json (the scripts read catalog.json because PyYAML can't be installed there). Run scripts/export.py first so
catalog.json is current. In Claude Code, install the plugin instead; nothing is copied there.
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ["core", "packs", "bindings", "scripts", "catalog.json", "LICENSE", "LICENSE-SPEC.txt"]
SKIP = {"__pycache__", ".DS_Store"}


def files(p):
    if p.is_file():
        yield p
    else:
        for f in sorted(p.rglob("*")):
            if f.is_file() and not (set(f.parts) & SKIP) and f.suffix != ".pyc":
                yield f


def main():
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    for skill in sorted((ROOT / "skills").iterdir()):
        if not (skill / "SKILL.md").exists():
            continue
        z = out / f"{skill.name}.zip"
        n = 0
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(skill / "SKILL.md", f"{skill.name}/SKILL.md")
            n += 1
            for name in SHARED:
                for f in files(ROOT / name):
                    zf.write(f, f"{skill.name}/{f.relative_to(ROOT)}")
                    n += 1
        print(f"{z.relative_to(ROOT)}: {n} files, {z.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
