#!/usr/bin/env python3
"""QA step 8: overlap of coding sequence with TE annotation.

In:  --gff consensus GFF3; --te TE annotation (GFF3, BED, or RepeatMasker .out)
Out: <out>/te_overlap_genes.tsv (flag list only), <out>/metrics/qa08_te_overlap.tsv
A gene counts as TE-overlapping when at least te_cds_overlap_fraction of the CDS
bases of its longest isoform fall inside TE features (either strand).
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa_common as qc  # noqa: E402

STEP = "qa08_te_overlap"
GFF_SKIP_TYPES = {"region", "chromosome", "contig", "scaffold", "gene", "mRNA", "exon", "CDS"}


def read_te(path, exclude_classes) -> dict[str, list[tuple[int, int]]]:
    ivs = defaultdict(list)
    p = str(path)
    with qc._open(p) as fh:
        for line in fh:
            if not line.strip() or line.startswith("#"):
                continue
            if p.endswith((".bed", ".bed.gz")):
                c = line.split("\t")
                ivs[c[0]].append((int(c[1]) + 1, int(c[2])))
            elif p.endswith((".out", ".out.gz")):
                c = line.split()
                if len(c) < 11 or not c[0].isdigit():
                    continue  # header lines
                if c[10].split("/")[0] in exclude_classes:
                    continue
                ivs[c[4]].append((int(c[5]), int(c[6])))
            else:
                c = line.rstrip("\n").split("\t")
                if len(c) < 9 or c[2] in GFF_SKIP_TYPES:
                    continue
                if c[2] in exclude_classes:
                    continue
                ivs[c[0]].append((int(c[3]), int(c[4])))
    return {k: qc.merge_intervals(v) for k, v in ivs.items()}


def run(gff, out, te=None, config=None):
    cfg = qc.load_config(config)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    if not te:
        qc.write_metrics(out, STEP, [("te_overlap_gene_share", None, "no --te given"),
                                     ("te_overlap_cds_base_share", None, "no --te given")])
        return
    frac = float(qc.setting(cfg, "te_cds_overlap_fraction", "0.5"))
    excl = set(qc.setting_list(cfg, "te_exclude_classes", "Simple_repeat,Low_complexity"))
    te_ivs = read_te(te, excl)
    reps = qc.longest_isoforms(qc.read_models(gff))
    hit_genes, cds_total, cds_in_te = 0, 0, 0
    with open(out / "te_overlap_genes.tsv", "w", encoding="utf-8") as fh:
        fh.write("gene_id\ttranscript_id\tcds_bp\tcds_bp_in_te\tfraction\tnote\n")
        for gene in sorted(reps):
            t = reps[gene]
            cds = qc.merge_intervals(t.cds_intervals())
            tot = qc.total_len(cds)
            ov = qc.overlap_len(cds, te_ivs.get(t.seqid, []))
            cds_total += tot
            cds_in_te += ov
            if tot and ov / tot >= frac:
                hit_genes += 1
                fh.write(f"{gene}\t{t.id}\t{tot}\t{ov}\t{ov / tot:.3f}\treview; do not delete\n")
    rows = [
        ("te_overlap_gene_share", qc.share(hit_genes, len(reps)),
         f"CDS >= {frac:g} inside TE; listed in te_overlap_genes.tsv"),
        ("te_overlap_cds_base_share", qc.share(cds_in_te, cds_total), "all CDS bases"),
    ]
    qc.write_metrics(out, STEP, rows)


def main(argv=None):
    ap = qc.base_parser(__doc__.splitlines()[0])
    ap.add_argument("--te", help="TE annotation: GFF3 / BED / RepeatMasker .out")
    a = ap.parse_args(argv)
    run(a.gff, a.out, a.te, a.config)


if __name__ == "__main__":
    main()
