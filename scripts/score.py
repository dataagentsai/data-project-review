# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Score a review of the sample project against its answer key.

    uv run scripts/score.py examples/sample-project/project.yaml tests/sample-project-key.yaml tests/key-map.yaml

key-map.yaml maps each planted gap to the check ids that should catch it, and each false-positive trap to the
check ids that must NOT be reported as a gap:
  gaps: {G01: [DUP-01, IDEM-01]}
  traps: {T01: [DQ-01]}
A planted gap counts as caught when any of its checks is reported missing, partly, contradicts or unknown.
A trap counts as a false positive when any of its checks is reported missing or contradicts.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog as cat  # noqa: E402

FLAGGED = {"missing", "partly", "contradicts", "unknown"}


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    prof = cat.project(sys.argv[1])
    key, kmap = cat.load_yaml(sys.argv[2]), cat.load_yaml(sys.argv[3])
    rv = json.loads((prof["_dir"] / "review.json").read_text())["checks"]
    caught, missed = [], []
    for g in key["planted_gaps"]:
        ids = kmap["gaps"].get(g["gap"], [])
        hit = [i for i in ids if rv.get(i, {}).get("status") in FLAGGED]
        (caught if hit else missed).append((g, ids, hit))
    fps = []
    for i, t in enumerate(key.get("false_positive_traps") or [], 1):
        tid = t.get("id", f"T{i:02d}")
        bad = [c for c in kmap.get("traps", {}).get(tid, []) if rv.get(c, {}).get("status") in ("missing", "contradicts")]
        if bad:
            fps.append((tid, t.get("what"), bad))
    n = len(key["planted_gaps"])
    print(f"Caught {len(caught)}/{n} planted gaps ({100 * len(caught) / n:.0f}%)")
    by_how = {}
    for g, _, _ in caught + missed:
        by_how.setdefault(g.get("how_hidden"), [0, 0])[1] += 1
    for g, _, _ in caught:
        by_how[g.get("how_hidden")][0] += 1
    print("  by how hidden: " + ", ".join(f"{k} {a}/{b}" for k, (a, b) in by_how.items()))
    for g, ids, _ in missed:
        print(f"  MISSED {g['gap']} [{g['how_hidden']}, {g['severity']}] {g['description']} (checks {', '.join(ids) or 'none mapped'})")
    print(f"False positives on things done well: {len(fps)}/{len(key.get('false_positive_traps') or [])}")
    for tid, what, bad in fps:
        print(f"  FALSE POSITIVE {tid}: {what} (flagged {', '.join(bad)})")


if __name__ == "__main__":
    main()
