"""Tiny synthetic genome + gene models shared by the tests (no real data)."""
from __future__ import annotations

import os
import shutil
import stat
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PIPE = REPO / "pipeline"
FILL = "C" * 100          # no T in filler → no accidental stop codons


def build(tmp: Path) -> dict[str, Path]:
    """Write toy.fa and toy.gff3.

    g1      complete 2-exon gene (ATG … TAA)
    gene-L2 NCBI-style gene with two isoforms rna-XM_0001.1 (longer) and rna-XM_0002.1, plus a tRNA child
    g3      gene with an in-frame internal stop (TGA in the middle)
    g4      gene with one good and one partial isoform (partial lacks the stop codon)
    """
    parts, feats = [], []
    pos = 0

    def add(seq: str) -> tuple[int, int]:
        nonlocal pos
        start = pos + 1
        parts.append(seq)
        pos += len(seq)
        return start, pos

    add(FILL)
    cds1 = "ATG" + "GCC" * 60 + "TAA"
    a = add(cds1[:90])
    add("GT" + "C" * 96 + "AG")
    b = add(cds1[90:])
    feats += [("gene", a[0], b[1], "ID=g1"), ("mRNA", a[0], b[1], "ID=g1.t1;Parent=g1"),
              ("exon", *a, "Parent=g1.t1"), ("exon", *b, "Parent=g1.t1"),
              ("CDS", *a, "Parent=g1.t1"), ("CDS", *b, "Parent=g1.t1")]
    add(FILL)
    cds2 = "ATG" + "GGC" * 70 + "TGA"
    s2, e2 = add(cds2)
    # shorter isoform: same stop, starts 30 codons later at an internal ATG-free frame → use a later ATG
    feats += [("gene", s2, e2, "ID=gene-L2"),
              ("mRNA", s2, e2, "ID=rna-XM_0001.1;Parent=gene-L2"),
              ("exon", s2, e2, "Parent=rna-XM_0001.1"), ("CDS", s2, e2, "Parent=rna-XM_0001.1"),
              ("mRNA", s2 + 90, e2, "ID=rna-XM_0002.1;Parent=gene-L2"),
              ("exon", s2 + 90, e2, "Parent=rna-XM_0002.1"), ("CDS", s2 + 90, e2, "Parent=rna-XM_0002.1"),
              ("tRNA", s2, s2 + 71, "ID=trna-1;Parent=gene-L2"),
              ("exon", s2, s2 + 71, "Parent=trna-1")]
    add(FILL)
    cds3 = "ATG" + "GCC" * 30 + "TGA" + "GCC" * 30 + "TAA"
    s3, e3 = add(cds3)
    feats += [("gene", s3, e3, "ID=g3"), ("mRNA", s3, e3, "ID=g3.t1;Parent=g3"),
              ("exon", s3, e3, "Parent=g3.t1"), ("CDS", s3, e3, "Parent=g3.t1")]
    add(FILL)
    cds4 = "ATG" + "GCA" * 65 + "TAG"
    s4, e4 = add(cds4)
    feats += [("gene", s4, e4, "ID=g4"),
              ("mRNA", s4, e4, "ID=g4.t1;Parent=g4"),
              ("exon", s4, e4, "Parent=g4.t1"), ("CDS", s4, e4, "Parent=g4.t1"),
              ("mRNA", s4, e4 - 3, "ID=g4.t2;Parent=g4"),
              ("exon", s4, e4 - 3, "Parent=g4.t2"), ("CDS", s4, e4 - 3, "Parent=g4.t2")]
    add(FILL)

    fa = tmp / "toy.fa"
    fa.write_text(">chr1\n" + "".join(parts) + "\n")
    gff = tmp / "toy.gff3"
    lines = ["##gff-version 3"]
    for typ, s, e, attr in feats:
        phase = "0" if typ == "CDS" else "."
        lines.append(f"chr1\ttoy\t{typ}\t{s}\t{e}\t.\t+\t{phase}\t{attr}")
    gff.write_text("\n".join(lines) + "\n")
    return {"fa": fa, "gff": gff}


def have(tool: str) -> bool:
    return shutil.which(tool) is not None


def fake_tool(bindir: Path, name: str, body: str) -> Path:
    """Write an executable stub that logs its argv to $FAKE_LOG and then runs body."""
    bindir.mkdir(parents=True, exist_ok=True)
    p = bindir / name
    p.write_text("#!/usr/bin/env bash\n"
                 f'echo "{name} $*" >> "$FAKE_LOG"\n' + body + "\n")
    p.chmod(p.stat().st_mode | stat.S_IEXEC)
    return p


def run(cmd: list[str], env: dict[str, str] | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess:
    full = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/tmp")}
    full.update(env or {})
    return subprocess.run(cmd, env=full, cwd=cwd or REPO, capture_output=True, text=True)
