#!/usr/bin/env python3
"""QA step 2: BUSCO protein mode (longest isoform) and genome mode (upper bound).

In:  --proteins longest_isoform.proteins.faa (from qa01); --genome FASTA (optional)
Out: <out>/busco/<mode>_<lineage>/..., <out>/metrics/qa02_busco.tsv
A short_summary*.txt already under <out>/busco/<mode>_<lineage>/ is reused, not rerun.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa_common as qc  # noqa: E402

STEP = "qa02_busco"
# Lineage names come from config (busco_*_lineages). The defaults are the
# odb12 datasets embryophyta_odb12 + eudicotyledons_odb12: odb12 is the
# current BUSCO dataset release, and eudicotyledons_odb12 is the odb12 name of
# the old eudicots_odb10 (there is no eudicots_odb12). odb10 names still work
# if you set them in the config; confirm with: busco --list-datasets
SUMMARY_RE = re.compile(
    r"C:\s*([\d.]+)%\s*\[S:\s*([\d.]+)%\s*,\s*D:\s*([\d.]+)%\s*\]\s*,\s*"
    r"F:\s*([\d.]+)%\s*,\s*M:\s*([\d.]+)%\s*,\s*n:\s*(\d+)")


def parse_short_summary(path) -> dict[str, float] | None:
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    m = SUMMARY_RE.search(text)
    if not m:
        return None
    keys = ("C", "S", "D", "F", "M", "n")
    vals = dict(zip(keys, (float(x) for x in m.groups())))
    vals["n"] = int(vals["n"])
    return vals


def find_summary(run_dir: Path):
    hits = sorted(run_dir.rglob("short_summary*.txt")) if run_dir.is_dir() else []
    return hits[0] if hits else None


def busco_one(inp, mode, lineage, busco_root: Path, cfg, out=None):
    run_dir = busco_root / f"{'prot' if mode == 'proteins' else 'genome'}_{lineage}"
    summ = find_summary(run_dir)
    if summ is None:
        if not qc.have("busco"):
            qc.warn(f"busco not on PATH and no short_summary in {qc.rel(run_dir, out or busco_root)}; "
                    f"BUSCO {mode} {lineage} rows = NA")
            return None, "busco not on PATH and no short_summary found"
        cmd = ["busco", "-i", str(inp), "-l", lineage, "-m", mode, "-o", run_dir.name,
               "--out_path", str(busco_root), "-c", qc.setting(cfg, "threads", "8"), "-f"]
        dl = qc.setting(cfg, "busco_download_path", "")
        if dl:
            cmd += ["--offline", "--download_path", dl]
        busco_root.mkdir(parents=True, exist_ok=True)
        why = qc.run_cmd(cmd)
        if why:
            return None, why
        summ = find_summary(run_dir)
        if summ is None:
            return None, "busco ran but no short_summary found"
    vals = parse_short_summary(summ)
    if vals is None:
        return None, f"could not parse {summ}"
    return vals, qc.rel(summ, out or busco_root)


def run(out, proteins_fa, genome_fa=None, config=None):
    cfg = qc.load_config(config)
    out = Path(out)
    root = out / "busco"
    rows = []
    prot_c = {}
    for lin in qc.setting_list(cfg, "busco_protein_lineages"):
        vals, note = busco_one(proteins_fa, "proteins", lin, root, cfg, out)
        for k in ("C", "S", "D", "F", "M", "n"):
            k_note = note
            if vals and k == "D":
                k_note = f"{note}; high D: isoforms not deduplicated, split or chimeric genes"
            rows.append((f"busco_prot_{lin}_{k}", vals[k] if vals else None, k_note))
        if vals:
            prot_c[lin] = vals["C"]
    for lin in qc.setting_list(cfg, "busco_genome_lineages"):
        if not genome_fa:
            rows.append((f"busco_genome_{lin}_C", None, "no --genome given"))
            rows.append((f"busco_gap_{lin}", None, "no --genome given"))
            continue
        vals, note = busco_one(genome_fa, "genome", lin, root, cfg, out)
        rows.append((f"busco_genome_{lin}_C", vals["C"] if vals else None, note))
        gap = (vals["C"] - prot_c[lin]) if (vals and lin in prot_c) else None
        if gap is not None:
            gap_note = "genome C minus annotation C (points); guidance: within 3-5"
        elif lin not in prot_c:
            gap_note = f"protein-mode result missing for {lin}"
        else:
            gap_note = f"genome-mode result missing: {note}"
        rows.append((f"busco_gap_{lin}", gap, gap_note))
    qc.write_metrics(out, STEP, rows)


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--proteins", required=True)
    ap.add_argument("--genome")
    ap.add_argument("--out", required=True)
    ap.add_argument("--config")
    a = ap.parse_args(argv)
    run(a.out, a.proteins, a.genome, a.config)


if __name__ == "__main__":
    main()
