#!/usr/bin/env python3
"""Regenerate the simulated toy inputs for the A4a-A4e aggregation steps.

Usage: make_toy.py [OUT_DIR]   (default: the directory of this script)

Everything is simulated and deterministic (fixed seed): one 9 kb contig `chr1`
with three protein-coding genes.
  g1  + strand, 3 exons, CDS 651 nt, 5'/3' UTRs  (all evidence types)
  g2  - strand, 2 exons, CDS 501 nt, UTRs        (BRAKER, GeMoMa, miniprot, StringTie)
  g3  + strand, 1 exon,  CDS 600 nt               (BRAKER only, no evidence)
plus one unstranded single-exon StringTie transcript (STRG.9.1) that A4c drops.
tests/test_aggregation.py checks that the committed files equal this output.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

SEQID = "chr1"
GENOME_LEN = 9000
STOPS = {"TAA", "TAG", "TGA"}
COMP = str.maketrans("ACGT", "TGCA")

# Genome coordinates, 1-based inclusive. exons/cds listed low -> high.
GENES = {
    "g1": {"strand": "+", "exons": [(1001, 1300), (1501, 1700), (1901, 2300)],
           "cds": [(1101, 1300), (1501, 1700), (1901, 2151)]},
    "g2": {"strand": "-", "exons": [(4001, 4400), (4601, 5000)],
           "cds": [(4200, 4400), (4601, 4900)]},
    "g3": {"strand": "+", "exons": [(7001, 7600)], "cds": [(7001, 7600)]},
}


def revcomp(s: str) -> str:
    return s.translate(COMP)[::-1]


def tx_order(segs, strand):
    """Segments in transcript (5'->3') order."""
    return sorted(segs) if strand == "+" else sorted(segs, reverse=True)


def build_genome(rng: random.Random) -> str:
    seq = [rng.choice("ACGT") for _ in range(GENOME_LEN)]

    def put(start: int, s: str) -> None:
        seq[start - 1:start - 1 + len(s)] = list(s)

    for g in GENES.values():
        strand, cds = g["strand"], g["cds"]
        total = sum(e - s + 1 for s, e in cds)
        assert total % 3 == 0
        codons = ["ATG"]
        while len(codons) < total // 3 - 1:
            c = "".join(rng.choice("ACGT") for _ in range(3))
            if c not in STOPS:
                codons.append(c)
        codons.append("TAA")
        orf = "".join(codons)
        pos = 0
        for s, e in tx_order(cds, strand):
            piece = orf[pos:pos + e - s + 1]
            pos += e - s + 1
            put(s, piece if strand == "+" else revcomp(piece))
        # canonical GT..AG introns (in transcript orientation)
        ex = sorted(g["exons"])
        for (_, e1), (s2, _) in zip(ex, ex[1:]):
            if strand == "+":
                put(e1 + 1, "GT")
                put(s2 - 2, "AG")
            else:
                put(e1 + 1, "CT")
                put(s2 - 2, "AC")
    return "".join(seq)


def drop_stop(cds, strand):
    """CDS without the terminal stop codon (AUGUSTUS/miniprot style)."""
    segs = sorted(cds)
    if strand == "+":
        s, e = segs[-1]
        return segs[:-1] + [(s, e - 3)], (e - 2, e)
    s, e = segs[0]
    return [(s + 3, e)] + segs[1:], (s, s + 2)


def start_codon(cds, strand):
    segs = sorted(cds)
    if strand == "+":
        s = segs[0][0]
        return (s, s + 2)
    e = segs[-1][1]
    return (e - 2, e)


def phases(segs, strand):
    out, acc = {}, 0
    for s, e in tx_order(segs, strand):
        out[(s, e)] = (3 - acc % 3) % 3
        acc += e - s + 1
    return out


def gtf(fields, attrs):
    return "\t".join([SEQID] + [str(x) for x in fields] + [attrs])


def augustus_gtf(names, source="AUGUSTUS"):
    lines = []
    for name in names:
        g = GENES[name]
        st = g["strand"]
        tid = f"{name}.t1"
        a = f'transcript_id "{tid}"; gene_id "{name}";'
        segs, stop = drop_stop(g["cds"], st)
        lo, hi = min(s for s, _ in g["cds"]), max(e for _, e in g["cds"])
        lines.append(gtf([source, "gene", lo, hi, "1", st, "."], f'gene_id "{name}";'))
        lines.append(gtf([source, "transcript", lo, hi, "1", st, "."], a))
        sc = start_codon(g["cds"], st)
        lines.append(gtf([source, "start_codon", sc[0], sc[1], ".", st, "0"], a))
        ph = phases(segs, st)
        for s, e in sorted(segs):
            lines.append(gtf([source, "CDS", s, e, "1", st, ph[(s, e)]], a))
        lines.append(gtf([source, "stop_codon", stop[0], stop[1], ".", st, "0"], a))
    return "\n".join(lines) + "\n"


def gemoma_gff3():
    lines = ["##gff-version 3"]
    for name in ("g1", "g2"):
        g = GENES[name]
        st = g["strand"]
        lo, hi = min(s for s, _ in g["cds"]), max(e for _, e in g["cds"])
        gid, mid = f"gene_{name}", f"{name.upper()}_R1"
        lines.append(gtf(["GAF", "gene", lo, hi, ".", st, "."], f"ID={gid};transcripts=1"))
        lines.append(gtf(["GeMoMa", "mRNA", lo, hi, ".", st, "."],
                         f"ID={mid};ref-gene=REF_{name};Parent={gid};score=250"))
        ph = phases(g["cds"], st)
        for s, e in sorted(g["cds"]):
            lines.append(gtf(["GeMoMa", "CDS", s, e, ".", st, ph[(s, e)]], f"Parent={mid}"))
    return "\n".join(lines) + "\n"


def miniprot_gff():
    lines = ["##gff-version 3"]
    for n, name in enumerate(("g1", "g2"), start=1):
        g = GENES[name]
        st = g["strand"]
        segs, stop = drop_stop(g["cds"], st)
        aa_len = sum(e - s + 1 for s, e in segs) // 3
        mid, prot = f"MP{n:06d}", f"PROT_{name}"
        lo, hi = min(min(s for s, _ in segs), stop[0]), max(max(e for _, e in segs), stop[1])
        lines.append(f"##PAF\t{prot}\t{aa_len}\t0\t{aa_len}\t{st}\t{SEQID}\t{GENOME_LEN}")
        lines.append(gtf(["miniprot", "mRNA", lo, hi, "500", st, "."],
                         f"ID={mid};Rank=1;Identity=0.9500;Positive=0.9700;Target={prot} 1 {aa_len}"))
        ph = phases(segs, st)
        acc = 0
        rows = []
        for s, e in tx_order(segs, st):
            ln = e - s + 1
            a1, a2 = acc // 3 + 1, (acc + ln - 1) // 3 + 1
            acc += ln
            rows.append(gtf(["miniprot", "CDS", s, e, "500", st, ph[(s, e)]],
                            f"Parent={mid};Rank=1;Identity=0.9500;Target={prot} {a1} {a2}"))
        lines.extend(sorted(rows, key=lambda r: int(r.split("\t")[3])))
        lines.append(gtf(["miniprot", "stop_codon", stop[0], stop[1], "0", st, "0"],
                         f"Parent={mid};Rank=1"))
    return "\n".join(lines) + "\n"


def stringtie_gtf():
    lines = ["# StringTie-style GTF (simulated)"]
    items = [("STRG.1", "g1"), ("STRG.2", "g2")]
    for sg, name in items:
        g = GENES[name]
        st, ex = g["strand"], sorted(g["exons"])
        tid = f"{sg}.1"
        a = f'gene_id "{sg}"; transcript_id "{tid}";'
        lines.append(gtf(["StringTie", "transcript", ex[0][0], ex[-1][1], "1000", st, "."],
                         a + ' cov "25.0"; FPKM "10.0"; TPM "20.0";'))
        for i, (s, e) in enumerate(ex, start=1):
            lines.append(gtf(["StringTie", "exon", s, e, "1000", st, "."],
                             a + f' exon_number "{i}"; cov "25.0";'))
    a = 'gene_id "STRG.9"; transcript_id "STRG.9.1";'
    lines.append(gtf(["StringTie", "transcript", 8001, 8300, "1000", ".", "."], a + ' cov "3.0";'))
    lines.append(gtf(["StringTie", "exon", 8001, 8300, "1000", ".", "."], a + ' exon_number "1";'))
    return "\n".join(lines) + "\n"


def pasa_gff3():
    g = GENES["g1"]
    st = g["strand"]
    lines = []
    acc = 0
    for s, e in tx_order(g["exons"], st):
        ln = e - s + 1
        lines.append(gtf(["assembler-pasa_toy", "cDNA_match", s, e, ".", st, "."],
                         f"ID=align_1;Target=asmbl_1 {acc + 1} {acc + ln} +"))
        acc += ln
    return "\n".join(lines) + "\n"


def mature(genome, name):
    g = GENES[name]
    s = "".join(genome[a - 1:b] for a, b in sorted(g["exons"]))
    return s if g["strand"] == "+" else revcomp(s)


def wrap(s, n=60):
    return "\n".join(s[i:i + n] for i in range(0, len(s), n))


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
    rng = random.Random(20261019)
    genome = build_genome(rng)
    files = {
        "genome.fa": f">{SEQID} simulated toy contig\n{wrap(genome)}\n",
        "braker.gtf": augustus_gtf(["g1", "g2", "g3"]),
        "gemoma.gff3": gemoma_gff3(),
        "miniprot.gff": miniprot_gff(),
        "stringtie.gtf": stringtie_gtf(),
        "pasa_assemblies.gff3": pasa_gff3(),
        "mikado_list.tsv": "stringtie.gtf\tst\tTrue\t1\tFalse\tTrue\tTrue\n",
        # BRAKER1 (RNA) and BRAKER2 (protein) runs for the optional TSEBRA branch.
        "tsebra/braker1/augustus.hints.gtf": augustus_gtf(["g1", "g3"]),
        "tsebra/braker2/augustus.hints.gtf": augustus_gtf(["g1", "g2"]),
        "tsebra/braker1/hintsfile.gff": (
            f"{SEQID}\tb2h\tintron\t1301\t1500\t1\t+\t.\tsrc=E;mult=12;pri=4;\n"
            f"{SEQID}\tb2h\tintron\t1701\t1900\t1\t+\t.\tsrc=E;mult=10;pri=4;\n"),
        "tsebra/braker2/hintsfile.gff": (
            f"{SEQID}\tProtHint\tintron\t1301\t1500\t1\t+\t.\tsrc=P;mult=3;pri=4;al_score=0.6;\n"
            f"{SEQID}\tProtHint\tintron\t4401\t4600\t1\t-\t.\tsrc=P;mult=2;pri=4;al_score=0.5;\n"),
        "pasa/transcripts.fasta.clean": (
            f">asmbl_1\n{wrap(mature(genome, 'g1'))}\n>asmbl_2\n{wrap(mature(genome, 'g2'))}\n"),
        # Minimal configs; real runs start from $PASA_HOME/pasa_conf/*.Template.txt
        "pasa/alignAssembly.config": (
            "DATABASE=pasa_toy.sqlite\n"
            "validate_alignments_in_db.dbi:--MIN_PERCENT_ALIGNED=75\n"
            "validate_alignments_in_db.dbi:--MIN_AVG_PER_ID=95\n"),
        "pasa/annotCompare.config": "DATABASE=pasa_toy.sqlite\n",
    }
    for rel, text in files.items():
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


if __name__ == "__main__":
    main()
