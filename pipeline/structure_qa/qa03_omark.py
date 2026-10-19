#!/usr/bin/env python3
"""QA step 3: OMArk consistency (consistent / inconsistent / contaminant / unknown).

In:  --proteins longest_isoform.proteins.faa (from qa01); OMAmer DB in config (omamer_db)
Out: <out>/omark/..., <out>/metrics/qa03_omark.tsv
A *.sum already under <out>/omark/ is reused, not rerun.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa_common as qc  # noqa: E402

STEP = "qa03_omark"
PCT = r"([\d.]+)%"
CONS_RE = re.compile(rf"^A:{PCT}.*?I:{PCT}.*?C:{PCT}.*?U:{PCT}", re.M)
COMP_RE = re.compile(rf"^S:{PCT},D:{PCT}.*?M:{PCT}", re.M)


def parse_sum(path) -> dict[str, float] | None:
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    m = CONS_RE.search(text)
    if not m:
        return None
    vals = dict(zip(("consistent", "inconsistent", "contaminant", "unknown"),
                    (float(x) for x in m.groups())))
    c = COMP_RE.search(text)
    if c:
        vals.update(zip(("single", "duplicated", "missing"), (float(x) for x in c.groups())))
    return vals


def find_sum(d: Path):
    hits = sorted(d.rglob("*.sum")) if d.is_dir() else []
    return hits[0] if hits else None


def run(out, proteins_fa, config=None):
    cfg = qc.load_config(config)
    out = Path(out)
    odir = out / "omark"
    summ, note = find_sum(odir), ""
    if summ is None:
        db = qc.setting(cfg, "omamer_db", "")
        if not (qc.have("omamer") and qc.have("omark")):
            note = "omamer/omark not on PATH and no .sum found"
        elif not db or not Path(db).is_file():
            note = "set omamer_db in config to an OMAmer .h5 file"
        else:
            odir.mkdir(parents=True, exist_ok=True)
            hits = odir / "proteins.omamer"
            cmd2 = ["omark", "-f", str(hits), "-d", db, "-o", str(odir / "omark_output")]
            taxid = qc.setting(cfg, "omark_taxid", "")
            if taxid:
                cmd2 += ["-t", taxid]
            if qc.run_cmd(["omamer", "search", "--db", db, "--query", str(proteins_fa),
                           "--out", str(hits)]) and qc.run_cmd(cmd2):
                summ = find_sum(odir)
            note = "" if summ else "omark not run (RUN!=1 or failed)"
    vals = parse_sum(summ) if summ else None
    if summ and vals is None:
        note = f"could not parse {summ}"
    keys = ("consistent", "inconsistent", "contaminant", "unknown", "single", "duplicated", "missing")
    rows = [(f"omark_{k}_pct", vals.get(k) if vals else None, qc.rel(summ, out) if vals else note)
            for k in keys]
    qc.write_metrics(out, STEP, rows)


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--proteins", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--config")
    a = ap.parse_args(argv)
    run(a.out, a.proteins, a.config)


if __name__ == "__main__":
    main()
