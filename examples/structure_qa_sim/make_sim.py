#!/usr/bin/env python3
"""Build the small simulated example for pipeline/structure_qa (deterministic).

Writes into this folder: genome.fa, consensus.gff3, proteins.faa,
evidence_transcripts.gtf, evidence_proteins.gff3, rnaseq.bam, te.gff3.
Planted problems: g05 internal stop, g04 GC-AG intron, g06 no evidence (AED 1),
g07 CDS inside a TE, g08 last exon without evidence.
"""
from __future__ import annotations

import random
import struct
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "pipeline" / "structure_qa"))
import qa_common as qc  # noqa: E402

rng = random.Random(20261019)
STOPS = {"TAA", "TAG", "TGA"}
CHROM_LEN = 30000


def rand_dna(n):
    return "".join(rng.choice("ACGT") for _ in range(n))


def rand_codons(n):
    out = []
    while len(out) < n:
        c = rand_dna(3)
        if c not in STOPS:
            out.append(c)
    return "".join(out)


def intron_seq(n, donor="GT", acceptor="AG"):
    return donor + rand_dna(n - 4) + acceptor


# gene id, chrom, start, strand, exon CDS lengths (sum % 3 == 0), intron lengths,
# special flags
GENES = [
    ("g01", "chr1", 1001, "+", [150, 111, 240], [300, 450], {"isoform_skip": 1}),
    ("g02", "chr1", 5001, "-", [120, 99, 201, 180], [250, 600, 180], {}),
    ("g03", "chr1", 10001, "+", [903], [], {}),
    ("g04", "chr1", 14001, "-", [210, 291], [400], {"gc_ag": 0}),
    ("g05", "chr1", 18001, "+", [180, 150, 171], [350, 220], {"internal_stop": True}),
    ("g06", "chr1", 23001, "+", [240, 162], [500], {"no_evidence": True}),
    ("g07", "chr2", 1001, "-", [600], [], {"in_te": True}),
    ("g08", "chr2", 5001, "+", [120, 90, 105, 96, 141], [200, 300, 250, 400], {"drop_last_exon_ev": True}),
    ("g09", "chr2", 11001, "-", [180, 210, 162], [700, 260], {}),
    ("g10", "chr2", 16001, "+", [300, 201], [320], {}),
]
UTR = 60


def build():
    genome = {"chr1": list(rand_dna(CHROM_LEN)), "chr2": list(rand_dna(CHROM_LEN))}
    models = []  # (gene, tid, chrom, strand, exons, cds[(s,e,phase)], flags)
    for gid, chrom, gstart, strand, exl, inl, flags in GENES:
        total = sum(exl)
        assert total % 3 == 0, gid
        cds = "ATG" + rand_codons(total // 3 - 2) + "TAA"
        if flags.get("internal_stop"):
            mid = (total // 3 // 2) * 3
            cds = cds[:mid] + "TGA" + cds[mid + 3:]
        # transcript-order pieces: CDS exon segments and introns
        pieces, pos = [], 0
        for i, ln in enumerate(exl):
            pieces.append(("exon", cds[pos:pos + ln]))
            pos += ln
            if i < len(inl):
                donor, acc = ("GC", "AG") if flags.get("gc_ag") == i else ("GT", "AG")
                pieces.append(("intron", intron_seq(inl[i], donor, acc)))
        tx_seq = rand_dna(UTR) + "".join(p for _, p in pieces) + rand_dna(UTR)
        genomic = tx_seq if strand == "+" else qc.revcomp(tx_seq)
        genome[chrom][gstart - 1:gstart - 1 + len(genomic)] = list(genomic)
        # coordinates in transcript order, then map to genome
        segs, cur = [], UTR
        for kind, p in pieces:
            if kind == "exon":
                segs.append((cur, cur + len(p) - 1))
            cur += len(p)
        L = len(tx_seq)

        def to_g(a, b):
            if strand == "+":
                return gstart + a, gstart + b
            return gstart + (L - 1 - b), gstart + (L - 1 - a)

        cds_g, done = [], 0
        for a, b in segs:
            s, e = to_g(a, b)
            cds_g.append((s, e, (3 - done % 3) % 3))
            done += b - a + 1
        exons_g = [(s, e) for s, e, _ in cds_g]
        # extend first/last exon by the UTR
        first, last = (0, -1) if strand == "+" else (-1, 0)
        exons_tx = list(exons_g)
        if strand == "+":
            exons_tx[0] = (exons_tx[0][0] - UTR, exons_tx[0][1])
            exons_tx[-1] = (exons_tx[-1][0], exons_tx[-1][1] + UTR)
        else:
            exons_tx[-1] = (exons_tx[-1][0] - UTR, exons_tx[-1][1])
            exons_tx[0] = (exons_tx[0][0], exons_tx[0][1] + UTR)
        del first, last
        models.append((gid, f"{gid}.t1", chrom, strand, sorted(exons_tx), sorted(cds_g), flags))
        if "isoform_skip" in flags:
            k = flags["isoform_skip"]
            assert exl[k] % 3 == 0
            ex2 = [x for i, x in enumerate(exons_tx) if i != k]
            # recompute phases without the skipped exon
            kept = [c for i, c in enumerate(cds_g) if i != k]
            done, cds2 = 0, []
            for s, e, _ in kept:
                cds2.append((s, e, (3 - done % 3) % 3))
                done += e - s + 1
            models.append((gid, f"{gid}.t2", chrom, strand, sorted(ex2), sorted(cds2), flags))
    genome = {k: "".join(v) for k, v in genome.items()}
    # TE: one over g07, two intergenic
    g07 = next(m for m in models if m[0] == "g07")
    te = [("chr2", g07[5][0][0] - 200, g07[5][-1][1] + 150, "LTR_retrotransposon"),
          ("chr1", 26001, 27500, "Gypsy_LTR_retrotransposon"),
          ("chr2", 21001, 21800, "hAT_TIR_transposon")]
    return genome, models, te


def write_gff3(path, models):
    with open(path, "w") as fh:
        fh.write("##gff-version 3\n")
        seen = set()
        for gid, tid, chrom, strand, exons, cds, _ in models:
            if gid not in seen:
                spans = [m for m in models if m[0] == gid]
                s = min(m[4][0][0] for m in spans)
                e = max(m[4][-1][1] for m in spans)
                fh.write(f"{chrom}\tsim\tgene\t{s}\t{e}\t.\t{strand}\t.\tID={gid}\n")
                seen.add(gid)
            fh.write(f"{chrom}\tsim\tmRNA\t{exons[0][0]}\t{exons[-1][1]}\t.\t{strand}\t.\t"
                     f"ID={tid};Parent={gid}\n")
            for i, (s, e) in enumerate(exons, 1):
                fh.write(f"{chrom}\tsim\texon\t{s}\t{e}\t.\t{strand}\t.\tID={tid}.exon{i};Parent={tid}\n")
            for i, (s, e, ph) in enumerate(cds, 1):
                fh.write(f"{chrom}\tsim\tCDS\t{s}\t{e}\t.\t{strand}\t{ph}\tID={tid}.cds{i};Parent={tid}\n")


def evidence_models(models):
    out = []
    for gid, tid, chrom, strand, exons, cds, flags in models:
        if flags.get("no_evidence"):
            continue
        ex = list(exons)
        if flags.get("drop_last_exon_ev"):
            ex = ex[:-1] if strand == "+" else ex[1:]
        out.append((gid, tid, chrom, strand, ex, cds))
    return out


def write_gtf(path, ev):
    with open(path, "w") as fh:
        for gid, tid, chrom, strand, ex, _ in ev:
            a = f'gene_id "STRG.{gid}"; transcript_id "STRG.{tid}";'
            fh.write(f"{chrom}\tStringTie\ttranscript\t{ex[0][0]}\t{ex[-1][1]}\t1000\t{strand}\t.\t{a}\n")
            for s, e in ex:
                fh.write(f"{chrom}\tStringTie\texon\t{s}\t{e}\t1000\t{strand}\t.\t{a}\n")


def write_protein_gff(path, ev):
    with open(path, "w") as fh:
        fh.write("##gff-version 3\n")
        for gid, tid, chrom, strand, _, cds in ev:
            mid = f"MP.{tid}"
            fh.write(f"{chrom}\tminiprot\tmRNA\t{cds[0][0]}\t{cds[-1][1]}\t.\t{strand}\t.\tID={mid}\n")
            for s, e, ph in cds:
                fh.write(f"{chrom}\tminiprot\tCDS\t{s}\t{e}\t.\t{strand}\t{ph}\tParent={mid}\n")


# ---- minimal BGZF + BAM writer (so samtools can read it too) -------------

def bgzf_block(data: bytes) -> bytes:
    comp = zlib.compressobj(6, zlib.DEFLATED, -15)
    cdata = comp.compress(data) + comp.flush()
    bsize = len(cdata) + 25
    header = struct.pack("<BBBBIBBHBBHH", 31, 139, 8, 4, 0, 0, 255, 6, 66, 67, 2, bsize)
    return header + cdata + struct.pack("<II", zlib.crc32(data) & 0xFFFFFFFF, len(data))


EOF_BLOCK = bytes.fromhex("1f8b08040000000000ff0600424302001b0003000000000000000000")


def reg2bin(beg, end):
    end -= 1
    if beg >> 14 == end >> 14:
        return ((1 << 15) - 1) // 7 + (beg >> 14)
    if beg >> 17 == end >> 17:
        return ((1 << 12) - 1) // 7 + (beg >> 17)
    if beg >> 20 == end >> 20:
        return ((1 << 9) - 1) // 7 + (beg >> 20)
    if beg >> 23 == end >> 23:
        return ((1 << 6) - 1) // 7 + (beg >> 23)
    if beg >> 26 == end >> 26:
        return ((1 << 3) - 1) // 7 + (beg >> 26)
    return 0


def bam_record(ref_id, pos0, name, cigar, seq):
    ops = {"M": 0, "I": 1, "D": 2, "N": 3, "S": 4}
    cig = b"".join(struct.pack("<I", ln << 4 | ops[op]) for op, ln in cigar)
    ref_len = sum(ln for op, ln in cigar if op in "MDN")
    nt = {"=": 0, "A": 1, "C": 2, "G": 4, "T": 8, "N": 15}
    packed = bytearray()
    for i in range(0, len(seq), 2):
        hi = nt[seq[i]]
        lo = nt[seq[i + 1]] if i + 1 < len(seq) else 0
        packed.append(hi << 4 | lo)
    rname = name.encode() + b"\x00"
    body = struct.pack("<iiBBHHHiiii", ref_id, pos0, len(rname), 60,
                       reg2bin(pos0, pos0 + ref_len), len(cigar), 0, len(seq), -1, -1, 0)
    body += rname + cig + bytes(packed) + b"\xff" * len(seq)
    return struct.pack("<i", len(body)) + body


def write_bam(path, genome, ev):
    chroms = sorted(genome)
    text = "@HD\tVN:1.6\tSO:coordinate\n" + "".join(
        f"@SQ\tSN:{c}\tLN:{len(genome[c])}\n" for c in chroms)
    head = b"BAM\x01" + struct.pack("<i", len(text)) + text.encode()
    head += struct.pack("<i", len(chroms))
    for c in chroms:
        n = c.encode() + b"\x00"
        head += struct.pack("<i", len(n)) + n + struct.pack("<i", len(genome[c]))
    recs = []
    k = 0
    for gid, tid, chrom, strand, ex, _ in ev:
        if tid.endswith(".t2"):
            reads_per = 2
        else:
            reads_per = 3
        for i in range(len(ex) - 1):
            a_end, b_start = ex[i][1], ex[i + 1][0]
            for r in range(reads_per):
                left = 40 + r * 5
                right = 60 - r * 5
                pos1 = a_end - left + 1
                seq = genome[chrom][pos1 - 1:a_end] + genome[chrom][b_start - 1:b_start - 1 + right]
                cigar = [("M", left), ("N", b_start - a_end - 1), ("M", right)]
                k += 1
                recs.append((chroms.index(chrom), pos1 - 1, f"r{k}", cigar, seq.upper()))
        # one unspliced read per gene
        s = ex[0][0]
        k += 1
        recs.append((chroms.index(chrom), s - 1, f"r{k}", [("M", 50)], genome[chrom][s - 1:s + 49]))
    recs.sort(key=lambda r: (r[0], r[1]))
    data = head + b"".join(bam_record(*r) for r in recs)
    with open(path, "wb") as fh:
        for i in range(0, len(data), 60000):
            fh.write(bgzf_block(data[i:i + 60000]))
        fh.write(EOF_BLOCK)


def main():
    genome, models, te = build()
    qc.write_fasta(HERE / "genome.fa", sorted(genome.items()))
    write_gff3(HERE / "consensus.gff3", models)
    prots = []
    for _, tid, chrom, strand, exons, cds, _ in models:
        t = qc.Transcript(tid, "", chrom, strand)
        t.cds = cds
        prots.append((tid, qc.translate(t.cds_sequence(genome)).replace("*", ".")))
    qc.write_fasta(HERE / "proteins.faa", prots)  # '.' for stops, like gffread -y
    ev = evidence_models(models)
    write_gtf(HERE / "evidence_transcripts.gtf", ev)
    write_protein_gff(HERE / "evidence_proteins.gff3", ev)
    write_bam(HERE / "rnaseq.bam", genome, ev)
    with open(HERE / "te.gff3", "w") as fh:
        fh.write("##gff-version 3\n")
        for i, (c, s, e, t) in enumerate(te, 1):
            fh.write(f"{c}\tEDTA\t{t}\t{s}\t{e}\t.\t+\t.\tID=TE_{i:03d}\n")
    print(f"[OK] simulated example written to {HERE}")


if __name__ == "__main__":
    main()
