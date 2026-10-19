#!/usr/bin/env python3
"""QA step 4: agreement with evidence (gffcompare) and AED per transcript.

In:  --gff consensus GFF3; --evidence NAME=PATH (GTF/GFF3, repeatable), e.g.
     transcripts=stringtie.gtf  proteins=miniprot.gff3
Out: <out>/gffcompare/<NAME>.stats, <out>/aed_per_transcript.tsv,
     <out>/aed1_flagged.tsv (flag list only, nothing is deleted),
     <out>/metrics/qa04_evidence_aed.tsv
AED here = 1 - (SN + SP) / 2 on exon bases against all evidence models on the
same strand that overlap the transcript (Eilbeck et al. 2009). A transcript
attribute named in config (aed_attribute, e.g. _AED from MAKER) is used instead
when present.
"""
from __future__ import annotations

import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa_common as qc  # noqa: E402

STEP = "qa04_evidence_aed"
LEVELS = {"Base level": "base", "Exon level": "exon", "Intron level": "intron",
          "Intron chain level": "intron_chain", "Transcript level": "transcript",
          "Locus level": "locus"}
LEVEL_RE = re.compile(r"^\s*([A-Za-z ]+level):\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|", re.M)


def parse_gffcompare_stats(path) -> dict[str, tuple[float, float]]:
    out = {}
    for m in LEVEL_RE.finditer(Path(path).read_text(encoding="utf-8", errors="replace")):
        key = LEVELS.get(m.group(1).strip())
        if key:
            out[key] = (float(m.group(2)), float(m.group(3)))
    return out


def gffcompare_one(name, ev_path, gff, out: Path):
    gdir = out / "gffcompare"
    stats = [gdir / f"{name}.stats", gdir / name]
    found = next((p for p in stats if p.is_file()), None)
    if found is None:
        if not qc.have("gffcompare"):
            qc.warn(f"gffcompare not on PATH and no stats for '{name}'; gffcompare rows = NA")
            return None, "gffcompare not on PATH and no stats found"
        gdir.mkdir(parents=True, exist_ok=True)
        why = qc.run_cmd(["gffcompare", "-r", str(ev_path), "-o", str(gdir / name), str(gff)])
        if why:
            return None, why
        found = next((p for p in stats if p.is_file()), None)
        if found is None:
            return None, "gffcompare ran but no stats found"
    vals = parse_gffcompare_stats(found)
    return (vals or None), qc.rel(found, out) if vals else f"could not parse {found}"


STRANDED = ("+", "-")


def _strand_keys(strand: str) -> tuple[str, ...]:
    # unstranded evidence or models ('.', '?') can match either strand
    return (strand,) if strand in STRANDED else STRANDED


def compute_aed(models, evidence_models, attr_name=""):
    """{transcript_id: (aed, source)}. Without evidence, only transcripts that carry
    the AED attribute get a value; the rest are left out (reported as NA), never 1."""
    idx = qc.BinIndex()
    for ev in evidence_models:
        s, e = ev.span()
        for st in _strand_keys(ev.strand):
            idx.add((ev.seqid, st), s, e, ev)
    result = {}
    for t in sorted(qc.coding(models).values(), key=lambda x: x.id):
        if attr_name and attr_name in t.attrs:
            try:
                result[t.id] = (float(t.attrs[attr_name]), "attribute")
                continue
            except ValueError:
                pass
        if not evidence_models:
            continue
        pred = t.exon_intervals()
        s, e = pred[0][0], pred[-1][1]
        hits = []
        for st in _strand_keys(t.strand):
            hits.extend(h for h in idx.query((t.seqid, st), s, e) if h not in hits)
        ev_ivs = qc.merge_intervals([iv for h in hits for iv in h.exon_intervals()])
        shared = qc.overlap_len(pred, ev_ivs)
        if not ev_ivs or shared == 0:
            result[t.id] = (1.0, "computed")
            continue
        sn = shared / qc.total_len(ev_ivs)
        sp = shared / qc.total_len(pred)
        result[t.id] = (round(1 - (sn + sp) / 2, 4), "computed")
    return result


def run(gff, out, evidence: dict[str, str], config=None):
    cfg = qc.load_config(config)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    models = qc.read_models(gff)
    rows = []
    for name, path in evidence.items():
        vals, note = gffcompare_one(name, path, gff, out)
        for level in ("base", "exon", "intron", "transcript"):
            sn, sp = vals.get(level, (None, None)) if vals else (None, None)
            rows.append((f"gffcompare_{name}_{level}_sensitivity", sn, note))
            rows.append((f"gffcompare_{name}_{level}_precision", sp, note))
    ev_models = [t for p in evidence.values() for t in qc.read_models(p).values()]
    attr = qc.setting(cfg, "aed_attribute", "")
    has_attr = bool(attr) and any(attr in t.attrs for t in models.values())
    aed = compute_aed(models, ev_models, attr if has_attr else "") if (ev_models or has_attr) else {}
    with open(out / "aed_per_transcript.tsv", "w", encoding="utf-8") as fh, \
            open(out / "aed1_flagged.tsv", "w", encoding="utf-8") as flag:
        fh.write("transcript_id\tgene_id\taed\tsource\n")
        flag.write("transcript_id\tgene_id\tnote\n")
        for tid, (val, src) in aed.items():
            gene = models[tid].gene
            fh.write(f"{tid}\t{gene}\t{val}\t{src}\n")
            if val >= 1.0:
                flag.write(f"{tid}\t{gene}\tno evidence support; review, do not delete\n")
    vals = [v for v, _ in aed.values()]
    n = len(vals)
    if n:
        note = "" if ev_models else f"from the {attr} attribute only"
    else:
        note = f"no evidence given and no {attr or 'AED'} attribute in the GFF3"
    rows += [
        ("aed_transcripts", n if n else None, note),
        ("aed_le_0.5_share", qc.share(sum(v <= 0.5 for v in vals), n), note),
        ("aed_median", statistics.median(vals) if n else None, note),
        ("aed_eq_1_count", sum(v >= 1.0 for v in vals) if n else None,
         "listed in aed1_flagged.tsv; not deleted" if n else note),
        ("aed_eq_1_share", qc.share(sum(v >= 1.0 for v in vals), n), note),
    ]
    qc.write_metrics(out, STEP, rows)


def parse_evidence(items):
    ev = {}
    for item in items or []:
        name, sep, path = item.partition("=")
        if not sep or not name or not path:
            sys.exit(f"[ERR] --evidence wants NAME=PATH, got {item!r}")
        ev[name] = path
    return ev


def main(argv=None):
    ap = qc.base_parser(__doc__.splitlines()[0])
    ap.add_argument("--evidence", action="append", metavar="NAME=PATH")
    a = ap.parse_args(argv)
    run(a.gff, a.out, parse_evidence(a.evidence), a.config)


if __name__ == "__main__":
    main()
