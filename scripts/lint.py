# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Check the catalog and bindings follow catalog/SCHEMA.md. Exit 1 on any error.

    uv run scripts/lint.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog as cat  # noqa: E402

# Product and vendor names that must never appear in common checks (they belong in bindings/).
PRODUCTS = ["databricks", "spark", "pyspark", "delta lake", "delta table", "unity catalog", "lakeflow", "auto loader",
            "autoloader", "dlt", "snowflake", "snowpipe", "bigquery", "redshift", "synapse", "fabric", "onelake",
            "power bi", "tableau", "looker", "adf", "data factory", "airflow", "dbt", "kafka", "kinesis", "event hub",
            "glue", "emr", "dataproc", "aws", "azure", "gcp", "google cloud", "s3", "adls", "iceberg", "hudi",
            "great expectations", "deequ", "terraform", "github", "gitlab", "jenkins", "jira", "confluence"]
REQUIRED = ["id", "title", "kind", "concern", "question", "why", "applies", "owner", "evidence", "due", "fail_fast", "severity"]
ID = re.compile(r"^[A-Z]{2,6}-\d{2}$")
SIGNALS = {"vague-words", "single-number-estimate", "no-assumptions", "no-out-of-scope", "risks-without-owner",
           "no-decision-log", "no-acceptance-criteria", "missing-doc-type", "no-invisible-work", "status-always-green"}


def main():
    v, roles, stages = cat.vocab(), cat.roles(), cat.stages()
    concerns = {**v["concerns"]["technical"], **v["concerns"]["delivery"]}
    errs, warns = [], []
    checks = cat.checks()
    binds = cat.bindings()
    all_checks = checks + [c for b in binds.values() for c in b.get("checks") or []]
    ids = [c.get("id") for c in all_checks]
    for c in all_checks:
        where = f"{c.get('_file')}:{c.get('id')}"
        for k in REQUIRED:
            if not c.get(k):
                errs.append(f"{where}: missing '{k}'")
        if c.get("id") and not ID.match(c["id"]):
            errs.append(f"{where}: id must look like ABC-01")
        if ids.count(c.get("id")) > 1:
            errs.append(f"{where}: duplicate id")
        if not c.get("binding") and c.get("pack") not in v["packs"]:
            errs.append(f"{where}: pack folder '{c.get('pack')}' is not listed in core/vocab.yaml packs")
        if c.get("kind") not in ("technical", "delivery"):
            errs.append(f"{where}: kind must be technical or delivery")
        if c.get("concern") not in concerns:
            errs.append(f"{where}: unknown concern '{c.get('concern')}'")
        for r in [c.get("owner")] + list(c.get("also") or []):
            if r not in roles:
                errs.append(f"{where}: unknown role '{r}'")
        a = c.get("applies") or {}
        for field, allowed in (("kind", v["kinds"]), ("components", v["components"]), ("patterns", v["patterns"])):
            for x in a.get(field) or []:
                if x != "any" and x not in allowed:
                    errs.append(f"{where}: unknown {field} '{x}'")
        for d in (c.get("evidence") or {}).get("docs") or []:
            if d not in v["doc_types"]:
                errs.append(f"{where}: unknown doc type '{d}'")
        due = c.get("due") or {}
        last = 0
        for lv in cat.LEVELS:
            if lv in due:
                if due[lv] not in stages:
                    errs.append(f"{where}: due.{lv} must be a stage 1-10")
                elif due[lv] < last:
                    errs.append(f"{where}: due.{lv} comes before an earlier level")
                else:
                    last = due[lv]
        for k in due:
            if k not in cat.LEVELS:
                errs.append(f"{where}: unknown level '{k}'")
        if c.get("severity") not in ("high", "medium", "low"):
            errs.append(f"{where}: severity must be high, medium or low")
        for r in c.get("related") or []:
            if r not in ids:
                errs.append(f"{where}: related id '{r}' does not exist")
        if c.get("signal_id") and c["signal_id"] not in SIGNALS:
            errs.append(f"{where}: unknown signal_id '{c['signal_id']}'")
        if c.get("kind") == "delivery" and not c.get("signals"):
            errs.append(f"{where}: delivery checks need 'signals'")
        if not c.get("binding"):
            text = " ".join(str(c.get(k, "")) for k in ("title", "question", "why", "fail_fast", "signals", "evidence")).lower()
            for p in PRODUCTS:
                if re.search(r"(?<![a-z])" + re.escape(p) + r"(?![a-z])", text):
                    errs.append(f"{where}: product name '{p}' in a common check (move it to a binding)")
    for tech, b in binds.items():
        for cid in (b.get("how") or {}):
            if cid not in ids:
                errs.append(f"bindings/{tech}.yaml: how.{cid} points to a check that does not exist")
    n_t = sum(1 for c in checks if c.get("kind") == "technical")
    n_d = sum(1 for c in checks if c.get("kind") == "delivery")
    n_b = sum(len(b.get("checks") or []) for b in binds.values())
    per = {p: sum(1 for c in checks if c.get("pack") == p) for p in v["packs"]}
    print("packs: " + ", ".join(f"{p} {n}" for p, n in per.items()))
    print(f"{len(checks)} common checks ({n_t} technical, {n_d} delivery), {n_b} technology-only, "
          f"{len(binds)} binding(s): {', '.join(binds) or 'none'}")
    for w in warns:
        print("warn ", w)
    for e in errs:
        print("ERROR", e)
    print("lint:", "FAIL" if errs else "PASS", f"({len(errs)} errors)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
