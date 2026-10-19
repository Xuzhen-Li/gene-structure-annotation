#!/usr/bin/env python3
"""QA step 5: RNA-seq splice-junction support of the gene models.

In:  --gff consensus GFF3; one of
     --bam RNA-seq BAM (samtools used when on PATH, else a built-in reader), or
     --junctions STAR SJ.out.tab, or a TSV: chrom start end [strand] reads
     (intron coordinates, 1-based, inclusive)
Out: <out>/rnaseq_junctions.tsv (observed junctions), <out>/metrics/qa05_rnaseq_junctions.tsv
Counts use the longest isoform of each multi-exon gene.
"""
from __future__ import annotations

import gzip
import struct
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa_common as qc  # noqa: E402

STEP = "qa05_rnaseq_junctions"
SKIP_FLAGS = 0x4 | 0x100 | 0x400 | 0x800  # unmapped, secondary, duplicate, supplementary
REF_OPS = set("MDN=X")


def junctions_from_cigar(chrom, pos1, cigar_ops):
    """cigar_ops: iterable of (op, length). pos1 = 1-based leftmost base."""
    cur = pos1
    for op, ln in cigar_ops:
        if op == "N":
            yield chrom, cur, cur + ln - 1
        if op in REF_OPS:
            cur += ln


def _split_cigar(cigar: str):
    num = ""
    for ch in cigar:
        if ch.isdigit():
            num += ch
        else:
            yield ch, int(num)
            num = ""


def read_bam_python(path):
    """Minimal sequential BAM reader: yields (chrom, pos1, flag, cigar_ops)."""
    with gzip.open(path, "rb") as fh:
        if fh.read(4) != b"BAM\x01":
            raise ValueError(f"{path}: not a BAM file")
        (l_text,) = struct.unpack("<i", fh.read(4))
        fh.read(l_text)
        (n_ref,) = struct.unpack("<i", fh.read(4))
        refs = []
        for _ in range(n_ref):
            (l_name,) = struct.unpack("<i", fh.read(4))
            refs.append(fh.read(l_name).rstrip(b"\x00").decode())
            fh.read(4)
        while True:
            head = fh.read(4)
            if len(head) < 4:
                return
            (block_size,) = struct.unpack("<i", head)
            block = fh.read(block_size)
            ref_id, pos, l_read_name, _mapq, _bin, n_cigar, flag, _l_seq = \
                struct.unpack("<iiBBHHHi", block[:20])
            if ref_id < 0:
                continue
            off = 32 + l_read_name
            ops = []
            for i in range(n_cigar):
                (v,) = struct.unpack("<I", block[off + 4 * i: off + 4 * i + 4])
                ops.append(("MIDNSHP=X"[v & 0xF], v >> 4))
            yield refs[ref_id], pos + 1, flag, ops


def read_bam_samtools(path):
    proc = subprocess.Popen(["samtools", "view", str(path)], stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        cols = line.split("\t", 6)
        if len(cols) < 6 or cols[5] == "*":
            continue
        yield cols[2], int(cols[3]), int(cols[1]), list(_split_cigar(cols[5]))
    if proc.wait() != 0:
        raise RuntimeError("samtools view failed")


def junctions_from_bam(path) -> Counter:
    reader = read_bam_samtools if qc.have("samtools") else read_bam_python
    counts: Counter = Counter()
    for chrom, pos1, flag, ops in reader(path):
        if flag & SKIP_FLAGS:
            continue
        for j in junctions_from_cigar(chrom, pos1, ops):
            counts[j] += 1
    return counts


def junctions_from_table(path) -> Counter:
    counts: Counter = Counter()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.strip() or line.startswith(("#", "chrom")):
                continue
            c = line.rstrip("\n").split("\t")
            if len(c) >= 9 and c[3] in "012" and c[6].isdigit():  # STAR SJ.out.tab
                reads = int(c[6]) + int(c[7])
            else:
                reads = int(c[-1])
            counts[(c[0], int(c[1]), int(c[2]))] += reads
    return counts


def run(gff, out, bam=None, junctions=None, config=None):
    cfg = qc.load_config(config)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    if not bam and not junctions:
        qc.write_metrics(out, STEP, [(m, None, "no RNA-seq BAM or junction table given") for m in
                                     ("rnaseq_gene_junction_support_share",
                                      "rnaseq_intron_support_share",
                                      "rnaseq_full_chain_support_share")])
        return
    try:
        counts = junctions_from_table(junctions) if junctions else junctions_from_bam(bam)
    except (OSError, EOFError, ValueError, RuntimeError, struct.error, IndexError) as exc:
        src = junctions or bam
        qc.warn(f"cannot read {src}: {exc}; RNA-seq rows = NA")
        qc.write_metrics(out, STEP, [(m, None, f"cannot read {Path(src).name}: {type(exc).__name__}")
                                     for m in ("rnaseq_gene_junction_support_share",
                                               "rnaseq_intron_support_share",
                                               "rnaseq_full_chain_support_share")])
        return
    with open(out / "rnaseq_junctions.tsv", "w", encoding="utf-8") as fh:
        fh.write("chrom\tstart\tend\treads\n")
        for (c, s, e), n in sorted(counts.items()):
            fh.write(f"{c}\t{s}\t{e}\t{n}\n")
    min_reads = int(qc.setting(cfg, "junction_min_reads", "1"))
    ok = {j for j, n in counts.items() if n >= min_reads}
    reps = [t for t in qc.longest_isoforms(qc.read_models(gff)).values() if t.introns()]
    gene_hit = full = 0
    introns = set()
    for t in reps:
        tj = [(t.seqid, s, e) for s, e in t.introns()]
        introns.update(tj)
        hit = sum(j in ok for j in tj)
        gene_hit += hit >= 1
        full += hit == len(tj)
    note = f"multi-exon genes={len(reps)}; min reads per junction={min_reads}"
    rows = [
        ("rnaseq_gene_junction_support_share", qc.share(gene_hit, len(reps)), note),
        ("rnaseq_intron_support_share", qc.share(sum(j in ok for j in introns), len(introns)),
         f"unique introns={len(introns)}"),
        ("rnaseq_full_chain_support_share", qc.share(full, len(reps)), note),
    ]
    qc.write_metrics(out, STEP, rows)


def main(argv=None):
    ap = qc.base_parser(__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--bam")
    g.add_argument("--junctions")
    a = ap.parse_args(argv)
    run(a.gff, a.out, a.bam, a.junctions, a.config)


if __name__ == "__main__":
    main()
