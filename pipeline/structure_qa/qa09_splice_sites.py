#!/usr/bin/env python3
"""QA step 9: splice-site dinucleotides (GT-AG, GC-AG, AT-AC, other).

In:  --gff consensus GFF3; --genome FASTA
Out: <out>/noncanonical_introns.tsv, <out>/metrics/qa09_splice_sites.tsv
Each unique intron of all coding transcripts is counted once.
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa_common as qc  # noqa: E402

STEP = "qa09_splice_sites"


def intron_motif(chrom_seq: str, start: int, end: int, strand: str) -> str:
    seq = chrom_seq[start - 1:end].upper()
    if strand == "-":
        seq = qc.revcomp(seq)
    return f"{seq[:2]}-{seq[-2:]}" if len(seq) >= 4 else "short"


def run(gff, out, genome_fa, config=None):
    qc.load_config(config)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    genome = qc.read_fasta(genome_fa)
    introns = {}
    for t in qc.coding(qc.read_models(gff)).values():
        for s, e in t.introns():
            introns.setdefault((t.seqid, s, e, t.strand), t.id)
    motifs = Counter()
    with open(out / "noncanonical_introns.tsv", "w", encoding="utf-8") as fh:
        fh.write("chrom\tstart\tend\tstrand\tmotif\texample_transcript\n")
        for (c, s, e, strand), tid in sorted(introns.items()):
            if c not in genome:
                motifs["seqid_missing"] += 1
                continue
            m = intron_motif(genome[c], s, e, strand)
            motifs[m] += 1
            if m != "GT-AG":
                fh.write(f"{c}\t{s}\t{e}\t{strand}\t{m}\t{tid}\n")
    n = sum(v for k, v in motifs.items() if k != "seqid_missing")
    other = n - motifs["GT-AG"] - motifs["GC-AG"] - motifs["AT-AC"]
    note = f"unique introns of all coding transcripts={n}"
    rows = [
        ("splice_gt_ag_share", qc.share(motifs["GT-AG"], n), note),
        ("splice_gc_ag_share", qc.share(motifs["GC-AG"], n), note),
        ("splice_at_ac_share", qc.share(motifs["AT-AC"], n), note),
        ("splice_noncanonical_share", qc.share(other, n), "listed in noncanonical_introns.tsv"),
    ]
    qc.write_metrics(out, STEP, rows)


def main(argv=None):
    ap = qc.base_parser(__doc__.splitlines()[0])
    ap.add_argument("--genome", required=True)
    a = ap.parse_args(argv)
    run(a.gff, a.out, a.genome, a.config)


if __name__ == "__main__":
    main()
