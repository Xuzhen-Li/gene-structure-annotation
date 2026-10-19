#!/usr/bin/env python3
"""Build the tiny toy for scripts/first_run.sh (deterministic, simulated, ~70 kB).

Reuses the simulator in examples/structure_qa_sim/make_sim.py and writes here:
  genome.fa            2 simulated chromosomes, 30 kb each
  draft.gff3           stands in for the BRAKER output (10 genes, 11 mRNAs)
  protein_db.faa       protein evidence subset (6 genes, a few residues changed)
  rnaseq.bam           spliced RNA-seq reads (BGZF BAM, readable by samtools)
  rnaseq_junctions.tsv the same junctions as a table (chrom start end reads)
  transcripts.gtf      transcript evidence (stands in for StringTie)
  te.gff3, te_lib.fa   TE annotation and a TE library cut from the genome
Nothing here is real data.
"""
from __future__ import annotations

import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "examples" / "structure_qa_sim"))
sys.path.insert(0, str(REPO / "pipeline" / "structure_qa"))
import make_sim as ms  # noqa: E402
import qa_common as qc  # noqa: E402
import qa05_rnaseq_junctions as q5  # noqa: E402


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Build the toy (default: into this folder).")
    ap.add_argument("--out", type=Path, default=HERE)
    out = ap.parse_args().out
    out.mkdir(parents=True, exist_ok=True)
    genome, models, te = ms.build()
    qc.write_fasta(out / "genome.fa", sorted(genome.items()))
    ms.write_gff3(out / "draft.gff3", models)
    ev = ms.evidence_models(models)
    ms.write_gtf(out / "transcripts.gtf", ev)
    ms.write_bam(out / "rnaseq.bam", genome, ev)
    counts: Counter = q5.junctions_from_bam(out / "rnaseq.bam")
    with open(out / "rnaseq_junctions.tsv", "w") as fh:
        fh.write("chrom\tstart\tend\treads\n")
        for (c, s, e), n in sorted(counts.items()):
            fh.write(f"{c}\t{s}\t{e}\t{n}\n")
    rng = random.Random(7)
    prots = []
    for gid, tid, chrom, strand, exons, cds, _ in models:
        if gid not in {"g01", "g02", "g03", "g08", "g09", "g10"} or not tid.endswith(".t1"):
            continue
        t = qc.Transcript(tid, gid, chrom, strand)
        t.cds = cds
        p = list(qc.translate(t.cds_sequence(genome)).rstrip("*"))
        for _ in range(max(1, len(p) // 20)):  # ~5 % changed: a "close relative"
            i = rng.randrange(1, len(p))
            p[i] = rng.choice("ACDEFGHIKLMNPQRSTVWY")
        prots.append((f"rel_{gid}", "".join(p)))
    qc.write_fasta(out / "protein_db.faa", prots)
    with open(out / "te.gff3", "w") as fh:
        fh.write("##gff-version 3\n")
        for i, (c, s, e, t) in enumerate(te, 1):
            fh.write(f"{c}\tEDTA\t{t}\t{s}\t{e}\t.\t+\t.\tID=TE_{i:03d}\n")
    qc.write_fasta(out / "te_lib.fa",
                   [(f"TE_{i:03d}#{t}", genome[c][s - 1:e]) for i, (c, s, e, t) in enumerate(te, 1)])
    print(f"[OK] toy written to {out}")


if __name__ == "__main__":
    main()
