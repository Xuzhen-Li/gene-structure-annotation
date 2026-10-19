#!/usr/bin/env python3
"""QA step 6: gene counts, exon/intron statistics and single-exon share.

In:  --gff consensus GFF3
Out: <out>/intron_length_hist.tsv, <out>/metrics/qa06_gene_stats.tsv
Exon and intron numbers use the longest isoform of each gene.
"""
from __future__ import annotations

import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa_common as qc  # noqa: E402

STEP = "qa06_gene_stats"
HIST_EDGES = [0, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 25000, 50000, 100000]


def percentile(sorted_vals, q):
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)


def run(gff, out, config=None):
    cfg = qc.load_config(config)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    models = qc.read_models(gff)
    reps = list(qc.longest_isoforms(models).values())
    n = len(reps)
    exon_counts = [len(t.exon_intervals()) for t in reps]
    exon_lens = [e - s + 1 for t in reps for s, e in t.exon_intervals()]
    cds_lens = [t.cds_length() for t in reps]
    introns = sorted(e - s + 1 for t in reps for s, e in t.introns())
    short_bp = int(qc.setting(cfg, "intron_short_bp", "20"))
    long_bp = int(qc.setting(cfg, "intron_long_bp", "25000"))
    with open(out / "intron_length_hist.tsv", "w", encoding="utf-8") as fh:
        fh.write("bin_from_bp\tbin_to_bp\tintrons\n")
        edges = HIST_EDGES + [float("inf")]
        for lo, hi in zip(edges[:-1], edges[1:]):
            cnt = sum(lo <= x < hi for x in introns)
            fh.write(f"{lo}\t{'inf' if hi == float('inf') else hi}\t{cnt}\n")
    mean = statistics.mean
    rows = [
        ("gene_count", n, "genes with a CDS"),
        ("transcript_count", len(qc.coding(models)), "coding transcripts"),
        ("exons_per_gene_mean", mean(exon_counts) if n else None, "longest isoform"),
        ("exon_length_mean_bp", mean(exon_lens) if exon_lens else None, "exon lines, else CDS"),
        ("cds_length_mean_bp", mean(cds_lens) if n else None, ""),
        ("intron_count", len(introns), "longest isoform of each gene (qa09 counts unique introns of all transcripts)"),
        ("intron_length_median_bp", statistics.median(introns) if introns else None, ""),
        ("intron_length_p05_bp", percentile(introns, 0.05), ""),
        ("intron_length_p95_bp", percentile(introns, 0.95), ""),
        ("intron_length_max_bp", introns[-1] if introns else None, ""),
        ("intron_short_share", qc.share(sum(x < short_bp for x in introns), len(introns)),
         f"introns < {short_bp} bp"),
        ("intron_long_share", qc.share(sum(x > long_bp for x in introns), len(introns)),
         f"introns > {long_bp} bp"),
        ("single_exon_share", qc.share(sum(c == 1 for c in exon_counts), n), "longest isoform"),
    ]
    qc.write_metrics(out, STEP, rows)


def main(argv=None):
    ap = qc.base_parser(__doc__.splitlines()[0])
    a = ap.parse_args(argv)
    run(a.gff, a.out, a.config)


if __name__ == "__main__":
    main()
