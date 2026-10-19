"""Shared helpers for the structure QA steps (standard library only).

Every step reads the consensus GFF3 and writes one metrics file:
    <out>/metrics/<step>.tsv   with columns  metric  value  note
qa10_summary.py then joins all metrics files with the thresholds in
config/structure_qa.ini into one QC summary table.
"""
from __future__ import annotations

import configparser
import gzip
import os
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO_ROOT / "config" / "structure_qa.ini"
NA = "NA"

# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------


def load_config(path: str | os.PathLike | None = None) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser(delimiters=("=",), inline_comment_prefixes=("#",),
                                    interpolation=None)
    cfg.optionxform = str  # keep metric names case-sensitive
    p = Path(path) if path else DEFAULT_CONFIG
    if not p.is_file():
        sys.exit(f"[ERR] config not found: {p}")
    cfg.read(p, encoding="utf-8")
    return cfg


def setting(cfg, key: str, default=None):
    if cfg.has_section("settings") and cfg.has_option("settings", key):
        return cfg.get("settings", key).strip()
    return default


def setting_list(cfg, key: str, default: str = "") -> list[str]:
    raw = setting(cfg, key, default) or ""
    return [x.strip() for x in raw.split(",") if x.strip()]


# --------------------------------------------------------------------------
# metrics files
# --------------------------------------------------------------------------


def write_metrics(out_dir: str | os.PathLike, step: str, rows: list[tuple]) -> Path:
    """rows: (metric, value, note). value may be float/int/str/None (None -> NA)."""
    mdir = Path(out_dir) / "metrics"
    mdir.mkdir(parents=True, exist_ok=True)
    path = mdir / f"{step}.tsv"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("metric\tvalue\tnote\n")
        for metric, value, note in rows:
            fh.write(f"{metric}\t{fmt(value)}\t{note or ''}\n")
    print(f"[OK] {path}")
    return path


def fmt(value) -> str:
    if value is None:
        return NA
    if isinstance(value, bool):
        return str(int(value))
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if value != value:  # NaN
            return NA
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value)


def share(num: int, den: int):
    return (num / den) if den else None


# --------------------------------------------------------------------------
# FASTA
# --------------------------------------------------------------------------


def _open(path):
    path = str(path)
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path, encoding="utf-8")


def read_fasta(path) -> dict[str, str]:
    seqs: dict[str, list[str]] = {}
    name = None
    with _open(path) as fh:
        for line in fh:
            line = line.rstrip("\n\r")
            if not line:
                continue
            if line.startswith(">"):
                name = line[1:].split()[0]
                seqs[name] = []
            elif name is not None:
                seqs[name].append(line.strip())
    return {k: "".join(v) for k, v in seqs.items()}


def write_fasta(path, records: list[tuple[str, str]], width: int = 60) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        for name, seq in records:
            fh.write(f">{name}\n")
            for i in range(0, len(seq), width):
                fh.write(seq[i:i + width] + "\n")


_COMP = str.maketrans("ACGTRYKMBDHVNacgtrykmbdhvn", "TGCAYRMKVHDBNtgcayrmkvhdbn")


def revcomp(seq: str) -> str:
    return seq.translate(_COMP)[::-1]


_BASES = "TCAG"
_AA = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODON_TABLE = {a + b + c: _AA[16 * i + 4 * j + k]
               for i, a in enumerate(_BASES) for j, b in enumerate(_BASES)
               for k, c in enumerate(_BASES)}


def translate(cds: str) -> str:
    cds = cds.upper()
    return "".join(CODON_TABLE.get(cds[i:i + 3], "X") for i in range(0, len(cds) - 2, 3))


# --------------------------------------------------------------------------
# GFF3 / GTF model
# --------------------------------------------------------------------------


class Transcript:
    __slots__ = ("id", "gene", "seqid", "strand", "exons", "cds", "attrs")

    def __init__(self, tid, gene, seqid, strand, attrs=None):
        self.id = tid
        self.gene = gene
        self.seqid = seqid
        self.strand = strand
        self.exons: list[tuple[int, int]] = []
        self.cds: list[tuple[int, int, int]] = []  # start, end, phase (1-based closed)
        self.attrs = attrs or {}

    # exon intervals; fall back to CDS when a model has no exon lines
    def exon_intervals(self) -> list[tuple[int, int]]:
        ivs = self.exons or [(s, e) for s, e, _ in self.cds]
        return merge_intervals(ivs)

    def cds_intervals(self) -> list[tuple[int, int]]:
        return sorted((s, e) for s, e, _ in self.cds)

    def introns(self) -> list[tuple[int, int]]:
        ex = self.exon_intervals()
        return [(ex[i][1] + 1, ex[i + 1][0] - 1) for i in range(len(ex) - 1)
                if ex[i + 1][0] - ex[i][1] > 1]

    def cds_length(self) -> int:
        return sum(e - s + 1 for s, e, _ in self.cds)

    def span(self) -> tuple[int, int]:
        ivs = self.exon_intervals()
        return ivs[0][0], ivs[-1][1]

    def cds_sequence(self, genome: dict[str, str]) -> str | None:
        chrom = genome.get(self.seqid)
        if chrom is None or not self.cds:
            return None
        parts = sorted(self.cds, key=lambda x: x[0])
        seq = "".join(chrom[s - 1:e] for s, e, _ in parts)
        if self.strand == "-":
            seq = revcomp(seq)
            first_phase = max(parts, key=lambda x: x[1])[2]
        else:
            first_phase = parts[0][2]
        return seq[first_phase:] if first_phase in (1, 2) else seq


def merge_intervals(ivs) -> list[tuple[int, int]]:
    out: list[list[int]] = []
    for s, e in sorted(ivs):
        if out and s <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [(s, e) for s, e in out]


def overlap_len(a: list[tuple[int, int]], b: list[tuple[int, int]]) -> int:
    """Bases shared by two sorted, merged interval lists."""
    i = j = total = 0
    while i < len(a) and j < len(b):
        s = max(a[i][0], b[j][0])
        e = min(a[i][1], b[j][1])
        if s <= e:
            total += e - s + 1
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return total


def total_len(ivs) -> int:
    return sum(e - s + 1 for s, e in ivs)


def _parse_attrs(col9: str, is_gtf: bool) -> dict[str, str]:
    attrs = {}
    col9 = col9.strip()
    if not col9 or col9 == ".":
        return attrs
    if is_gtf:
        for part in col9.split(";"):
            part = part.strip()
            if not part:
                continue
            key, _, val = part.partition(" ")
            attrs[key] = val.strip().strip('"')
    else:
        for part in col9.split(";"):
            if "=" in part:
                key, _, val = part.partition("=")
                attrs[key.strip()] = unquote(val.strip())
    return attrs


TRANSCRIPT_TYPES = {"mRNA", "transcript"}


def read_models(path) -> dict[str, Transcript]:
    """Read protein-coding transcripts from GFF3 or GTF. Returns {transcript_id: Transcript}.

    GFF3: gene -> mRNA (ID/Parent) -> exon/CDS (Parent). GTF: transcript_id / gene_id.
    A CDS/exon whose Parent has no mRNA line still creates a transcript (gene = parent).
    """
    path = str(path)
    is_gtf_name = path.endswith((".gtf", ".gtf.gz"))
    tx: dict[str, Transcript] = {}
    pending: list[tuple] = []
    with _open(path) as fh:
        for line in fh:
            if line.startswith("##FASTA"):
                break
            if not line.strip() or line.startswith("#"):
                continue
            cols = line.rstrip("\n\r").split("\t")
            if len(cols) < 9:
                continue
            seqid, _src, ftype, start, end, _score, strand, phase, col9 = cols[:9]
            is_gtf = is_gtf_name or ("=" not in col9 and '"' in col9)
            attrs = _parse_attrs(col9, is_gtf)
            start_i, end_i = int(start), int(end)
            if is_gtf:
                tid = attrs.get("transcript_id")
                if not tid:
                    continue
                gid = attrs.get("gene_id", tid)
                if tid not in tx:
                    tx[tid] = Transcript(tid, gid, seqid, strand, {})
                if ftype in TRANSCRIPT_TYPES:
                    tx[tid].attrs.update(attrs)
                elif ftype == "exon":
                    tx[tid].exons.append((start_i, end_i))
                elif ftype == "CDS":
                    tx[tid].cds.append((start_i, end_i, int(phase) if phase.isdigit() else 0))
                continue
            if ftype in TRANSCRIPT_TYPES:
                tid = attrs.get("ID")
                if tid:
                    t = tx.get(tid) or Transcript(tid, attrs.get("Parent", tid).split(",")[0],
                                                  seqid, strand)
                    t.gene = attrs.get("Parent", tid).split(",")[0]
                    t.attrs = attrs
                    tx[tid] = t
            elif ftype in ("exon", "CDS"):
                for parent in attrs.get("Parent", "").split(","):
                    if parent:
                        pending.append((parent, ftype, seqid, strand, start_i, end_i, phase))
    for parent, ftype, seqid, strand, s, e, phase in pending:
        t = tx.get(parent)
        if t is None:
            t = tx[parent] = Transcript(parent, parent, seqid, strand)
        if ftype == "exon":
            t.exons.append((s, e))
        else:
            t.cds.append((s, e, int(phase) if phase.isdigit() else 0))
    for t in tx.values():
        t.exons.sort()
        t.cds.sort()
    return tx


def coding(models: dict[str, Transcript]) -> dict[str, Transcript]:
    return {k: v for k, v in models.items() if v.cds}


def longest_isoforms(models: dict[str, Transcript]) -> dict[str, Transcript]:
    """One transcript per gene: longest CDS, ties broken by transcript ID."""
    best: dict[str, Transcript] = {}
    for t in sorted(coding(models).values(), key=lambda x: x.id):
        cur = best.get(t.gene)
        if cur is None or t.cds_length() > cur.cds_length():
            best[t.gene] = t
    return best


def index_by_chrom(models) -> dict[tuple[str, str], list]:
    idx = defaultdict(list)
    for t in models:
        idx[(t.seqid, t.strand)].append(t)
    for v in idx.values():
        v.sort(key=lambda t: t.span()[0])
    return idx


# --------------------------------------------------------------------------
# external tools
# --------------------------------------------------------------------------


def want_run() -> bool:
    """Heavy external tools only run when RUN=1 (print-first, like the shell steps)."""
    return os.environ.get("RUN", "0") == "1"


def have(tool: str) -> bool:
    return shutil.which(tool) is not None


def run_cmd(cmd: list[str], cwd=None) -> bool:
    print("[CMD] " + " ".join(cmd))
    if not want_run():
        print("[DRY] export RUN=1 to execute")
        return False
    res = subprocess.run(cmd, cwd=cwd)
    if res.returncode != 0:
        print(f"[WARN] command failed (exit {res.returncode}): {cmd[0]}", file=sys.stderr)
        return False
    return True


def base_parser(description: str):
    import argparse
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--gff", required=True, help="consensus GFF3 from the merge step")
    ap.add_argument("--out", required=True, help="QA output folder")
    ap.add_argument("--config", default=None, help="thresholds/settings (default config/structure_qa.ini)")
    return ap


class BinIndex:
    """Find features overlapping an interval (fixed-size bins, enough for one genome)."""

    def __init__(self, bin_size: int = 10000):
        self.bin = bin_size
        self.bins: dict[tuple, list] = defaultdict(list)

    def add(self, key, start: int, end: int, item) -> None:
        for b in range(start // self.bin, end // self.bin + 1):
            self.bins[(key, b)].append((start, end, item))

    def query(self, key, start: int, end: int) -> list:
        seen, out = set(), []
        for b in range(start // self.bin, end // self.bin + 1):
            for s, e, item in self.bins.get((key, b), ()):
                if s <= end and e >= start and id(item) not in seen:
                    seen.add(id(item))
                    out.append(item)
        return out


def rel(path, out) -> str:
    """Path shown in notes: relative to the QA output folder when inside it."""
    try:
        return str(Path(path).resolve().relative_to(Path(out).resolve()))
    except ValueError:
        return str(path)
