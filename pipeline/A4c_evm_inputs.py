#!/usr/bin/env python3
"""A4c: convert gene predictions and evidence into EVidenceModeler 2.x inputs.

Writes into OUT_DIR:
  gene_predictions.gff3       ABINITIO_PREDICTION + OTHER_PREDICTION (gene->mRNA->exon->CDS)
  transcript_alignments.gff3  TRANSCRIPT (spliced-alignment GFF3: rows share ID=, carry Target=)
  protein_alignments.gff3     PROTEIN    (nucleotide_to_protein_match, Target in amino acids)
  weights.txt                 rows of the weights template whose SOURCE is present (no comments)
  summary.tsv                 per-source counts, dropped records

Usage (any subset of inputs; at least one gene-prediction input):
  A4c_evm_inputs.py -o OUT_DIR -w config/evm_weights_aggregate.txt [--genome GENOME.fa] \\
      [--braker braker.gtf | --tsebra tsebra.gtf] [--augustus augustus.gff3] [--gemoma final_annotation.gff] \\
      [--stringtie stringtie.gtf] [--pasa pasa_assemblies.gff3] [--mikado mikado.loci.gff3] \\
      [--miniprot miniprot.gff]
  A4c_evm_inputs.py --validate FILE --kind gene|alignment

Format reference: EVidenceModeler wiki "Preparing Inputs to EVM" and testing/*.gff3,
EVidenceModeler-v2.1.0 (https://github.com/EVidenceModeler/EVidenceModeler/wiki).
Pure standard library; no external tools needed.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Fixed SOURCE names (GFF3 column 2). config/evm_weights_aggregate.txt uses the
# same strings; EVM matches column 2 against the weights file exactly.
# ---------------------------------------------------------------------------
INPUTS = OrderedDict([
    # option      (EVM class,              source,      kind)
    ("braker",   ("ABINITIO_PREDICTION", "BRAKER",    "gene")),
    ("tsebra",   ("ABINITIO_PREDICTION", "TSEBRA",    "gene")),
    ("augustus", ("ABINITIO_PREDICTION", "AUGUSTUS",  "gene")),
    ("gemoma",   ("OTHER_PREDICTION",    "GeMoMa",    "gene")),
    ("stringtie", ("TRANSCRIPT",         "StringTie", "transcript")),
    ("pasa",     ("TRANSCRIPT",          "PASA",      "transcript")),
    # Mikado chooses among transcript assemblies -> transcript-evidence side.
    ("mikado",   ("TRANSCRIPT",          "Mikado",    "transcript")),
    ("miniprot", ("PROTEIN",             "miniprot",  "protein")),
])
EVM_CLASSES = ("ABINITIO_PREDICTION", "OTHER_PREDICTION", "PROTEIN", "TRANSCRIPT")
GENE_TYPES = {"gene", "mRNA", "exon", "CDS"}
TX_TYPES = {"mRNA", "transcript"}
GTF_ATTR = re.compile(r'(\S+)\s+"([^"]*)"')


class InputError(Exception):
    pass


# ----------------------------- parsing helpers -----------------------------

def read_rows(path: Path):
    """Yield (lineno, fields[9]) for feature lines."""
    with open(path) as fh:
        for n, line in enumerate(fh, start=1):
            if not line.strip() or line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) != 9:
                raise InputError(f"{path}:{n}: expected 9 tab-separated columns, got {len(f)}")
            yield n, f


def parse_attrs(col9: str) -> dict:
    """GFF3 (key=value;) or GTF (key "value";) attributes."""
    if GTF_ATTR.search(col9) and "=" not in col9.split(";")[0]:
        return {k: v for k, v in GTF_ATTR.findall(col9)}
    out = {}
    for part in col9.strip().strip(";").split(";"):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def safe_id(s: str) -> str:
    return re.sub(r"[;=,\s]", "_", s)


def merge_intervals(iv):
    """Merge overlapping or adjacent intervals (CDS + separate stop_codon)."""
    out = []
    for s, e in sorted(iv):
        if out and s <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [tuple(x) for x in out]


def tx_order(segs, strand):
    return sorted(segs) if strand == "+" else sorted(segs, reverse=True)


def _parents(attrs: dict):
    p = attrs.get("Parent") or attrs.get("transcript_id")
    return [x for x in (p or "").split(",") if x]


def collect_models(path: Path, features):
    """Group `features` rows by transcript.

    Returns OrderedDict tx_id -> {seqid, strand, gene, segs[]} and dropped counts.
    GTF: transcript_id / gene_id. GFF3: Parent of the feature, then Parent of the
    mRNA/transcript row for the gene (missing gene -> '<tx>.gene').
    """
    tx_gene = {}
    rows = []
    for _, f in read_rows(path):
        a = parse_attrs(f[8])
        if f[2] in TX_TYPES and "ID" in a:
            tx_gene[a["ID"]] = (a.get("Parent") or "").split(",")[0]
        if f[2] in features:
            rows.append((f, a))
    models = OrderedDict()
    dropped = defaultdict(int)
    for f, a in rows:
        parents = _parents(a)
        if not parents:
            dropped["no_parent"] += 1
            continue
        for tid in parents:
            m = models.setdefault(tid, {"seqid": f[0], "strand": f[6], "segs": [],
                                        "gene": a.get("gene_id") or tx_gene.get(tid) or ""})
            if m["seqid"] != f[0] or m["strand"] != f[6]:
                raise InputError(f"{path}: transcript {tid} mixes sequences or strands")
            m["segs"].append((int(f[3]), int(f[4])))
    for tid, m in list(models.items()):
        if m["strand"] not in ("+", "-"):
            dropped["unstranded"] += 1
            del models[tid]
            continue
        if not m["gene"]:
            m["gene"] = f"{tid}.gene"
        m["segs"] = merge_intervals(m["segs"])
    return models, dropped


# ------------------------------- converters --------------------------------

def gene_prediction_lines(path: Path, source: str):
    """CDS(+stop_codon) per transcript -> EVM gene-structure GFF3.

    As in EvmUtils/misc/braker_GTF_to_EVM_GFF3.pl, exons are written equal to the
    CDS segments (UTRs dropped; EVM scores coding structure, PASA A4e adds UTRs).
    Gene/mRNA/exon IDs are unique and prefixed by SOURCE; exons are never shared.
    """
    models, dropped = collect_models(path, {"CDS", "stop_codon"})
    by_gene = OrderedDict()
    for tid, m in models.items():
        by_gene.setdefault((m["seqid"], m["strand"], m["gene"]), []).append((tid, m))
    genes = []
    for (seqid, strand, gene), txs in by_gene.items():
        lo = min(s for _, m in txs for s, _ in m["segs"])
        hi = max(e for _, m in txs for _, e in m["segs"])
        genes.append((seqid, lo, hi, strand, gene, txs))
    genes.sort(key=lambda g: (g[0], g[1], g[2]))
    lines = []
    n_tx = 0
    warn = defaultdict(int)
    for seqid, lo, hi, strand, gene, txs in genes:
        gid = f"{source}.{safe_id(gene)}"
        lines.append("\t".join([seqid, source, "gene", str(lo), str(hi), ".", strand, ".",
                                f"ID={gid};Name={source} model {safe_id(gene)}"]))
        for tid, m in txs:
            n_tx += 1
            mid = f"{source}.{safe_id(tid)}"
            segs = m["segs"]
            if sum(e - s + 1 for s, e in segs) % 3:
                warn["cds_len_not_multiple_of_3"] += 1
            lines.append("\t".join([seqid, source, "mRNA", str(segs[0][0]), str(segs[-1][1]),
                                    ".", strand, ".", f"ID={mid};Parent={gid}"]))
            acc = 0
            phase = {}
            for s, e in tx_order(segs, strand):
                phase[(s, e)] = (3 - acc % 3) % 3
                acc += e - s + 1
            for i, (s, e) in enumerate(tx_order(segs, strand), start=1):
                lines.append("\t".join([seqid, source, "exon", str(s), str(e), ".", strand, ".",
                                        f"ID={mid}.exon{i};Parent={mid}"]))
                lines.append("\t".join([seqid, source, "CDS", str(s), str(e), ".", strand,
                                        str(phase[(s, e)]), f"ID=cds.{mid};Parent={mid}"]))
    stats = {"genes": len(genes), "models": n_tx, **dropped, **warn}
    return lines, stats


def alignment_lines_from_exons(path: Path, source: str):
    """Transcript exon chains (StringTie GTF, Mikado loci GFF3, PASA GTF) ->
    EVM spliced-alignment GFF3 (EST_match), mirroring Gene_obj::to_alignment_GFF3_format:
    one row per exon, shared ID, score 100, Target=<tx> <from> <to> + in transcript coords.
    Unstranded transcripts are dropped (no orientation, no intron evidence)."""
    models, dropped = collect_models(path, {"exon"})
    lines = []
    for tid, m in sorted(models.items(), key=lambda kv: (kv[1]["seqid"], kv[1]["segs"][0][0])):
        aid = f"{source}.{safe_id(tid)}"
        acc = 0
        for s, e in tx_order(m["segs"], m["strand"]):
            ln = e - s + 1
            lines.append("\t".join([m["seqid"], source, "EST_match", str(s), str(e), "100",
                                    m["strand"], ".",
                                    f"ID={aid};Target={safe_id(tid)} {acc + 1} {acc + ln} +"]))
            acc += ln
    return lines, {"alignments": len(models), **dropped}


def pasa_lines(path: Path, source: str):
    """PASA alignment assemblies (*.pasa_assemblies.gff3, cDNA_match rows with
    ID + Target) are already EVM spliced-alignment GFF3: only column 2 and the ID
    prefix change. A GTF of assemblies falls back to the exon-chain converter."""
    rows = [(n, f) for n, f in read_rows(path) if f[2] in ("cDNA_match", "EST_match", "match")]
    if not rows:
        return alignment_lines_from_exons(path, source)
    lines, ids = [], set()
    for n, f in rows:
        a = parse_attrs(f[8])
        if "ID" not in a or "Target" not in a:
            raise InputError(f"{path}:{n}: PASA alignment row needs ID= and Target=")
        if f[6] not in ("+", "-"):
            continue
        aid = f"{source}.{safe_id(a['ID'])}"
        ids.add(aid)
        lines.append("\t".join(f[:1] + [source, f[2]] + f[3:8] + [f"ID={aid};Target={a['Target']}"]))
    return lines, {"alignments": len(ids)}


def miniprot_lines(path: Path, source: str):
    """miniprot --gff -> EVM protein spliced alignment (as EvmUtils/misc/
    miniprot_GFF_2_EVM_alignment_GFF3.py): CDS rows only (stop_codon has no amino
    acid), type nucleotide_to_protein_match, ID = mRNA ID, score = Identity*100,
    Target = protein <aa_from> <aa_to>."""
    ident, rows = {}, []
    for n, f in read_rows(path):
        a = parse_attrs(f[8])
        if f[2] == "mRNA" and "ID" in a:
            ident[a["ID"]] = a.get("Identity")
        elif f[2] == "CDS":
            rows.append((n, f, a))
    lines, ids = [], set()
    for n, f, a in rows:
        par = a.get("Parent")
        if not par or "Target" not in a:
            raise InputError(f"{path}:{n}: miniprot CDS needs Parent= and Target=")
        idv = a.get("Identity") or ident.get(par)
        score = f"{float(idv) * 100:.2f}" if idv else "."
        aid = f"{source}.{safe_id(par)}"
        ids.add(aid)
        lines.append("\t".join([f[0], source, "nucleotide_to_protein_match", f[3], f[4], score,
                                f[6], ".", f"ID={aid};Target={a['Target']}"]))
    return lines, {"alignments": len(ids)}


# ------------------------------- validators --------------------------------

def validate_gene_gff3(lines):
    """EVM gene-structure rules: gene->(mRNA->(exon->CDS?)+)+, unique gene/mRNA/
    exon IDs (CDS IDs may repeat), every CDS inside an exon of its mRNA."""
    errs, ids = [], set()
    genes, mrna, exons, cds = {}, {}, defaultdict(list), []
    for i, line in enumerate(lines, start=1):
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split("\t")
        if len(f) != 9:
            errs.append(f"line {i}: not 9 columns")
            continue
        if f[2] not in GENE_TYPES:
            errs.append(f"line {i}: feature type {f[2]} not allowed")
        s, e = int(f[3]), int(f[4])
        if s > e or s < 1:
            errs.append(f"line {i}: bad coordinates {s}-{e}")
        if f[6] not in ("+", "-"):
            errs.append(f"line {i}: strand must be + or -")
        a = parse_attrs(f[8])
        fid = a.get("ID")
        if not fid:
            errs.append(f"line {i}: missing ID")
            continue
        if f[2] != "CDS":
            if fid in ids:
                errs.append(f"line {i}: duplicate ID {fid}")
            ids.add(fid)
        if f[2] == "gene":
            genes[fid] = f
        elif f[2] == "mRNA":
            if a.get("Parent") not in genes:
                errs.append(f"line {i}: mRNA {fid} parent gene not defined before it")
            mrna[fid] = f
        elif f[2] in ("exon", "CDS"):
            p = a.get("Parent")
            if p not in mrna:
                errs.append(f"line {i}: {f[2]} parent mRNA {p} not defined before it")
                continue
            if f[0] != mrna[p][0] or f[6] != mrna[p][6]:
                errs.append(f"line {i}: {f[2]} seqid/strand differs from mRNA {p}")
            if f[2] == "exon":
                exons[p].append((s, e))
            else:
                cds.append((i, p, s, e))
    for i, p, s, e in cds:
        if not any(es <= s and e <= ee for es, ee in exons[p]):
            errs.append(f"line {i}: CDS {s}-{e} not contained in an exon of {p}")
    for m in mrna:
        if not exons[m]:
            errs.append(f"mRNA {m} has no exon")
    return errs


def validate_alignment_gff3(lines):
    """EVM spliced-alignment rules: rows of one alignment share ID=, each row has
    Target=<id> <from> <to> [strand], one seqid/strand per ID, no overlapping rows."""
    errs, chains = [], defaultdict(list)
    for i, line in enumerate(lines, start=1):
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split("\t")
        if len(f) != 9:
            errs.append(f"line {i}: not 9 columns")
            continue
        a = parse_attrs(f[8])
        if "ID" not in a:
            errs.append(f"line {i}: missing ID")
            continue
        t = a.get("Target", "").split()
        if len(t) not in (3, 4) or not (t[1:3] and all(x.isdigit() for x in t[1:3])):
            errs.append(f"line {i}: Target must be '<id> <from> <to> [strand]'")
        if f[6] not in ("+", "-"):
            errs.append(f"line {i}: strand must be + or -")
        chains[a["ID"]].append((f[0], f[6], int(f[3]), int(f[4]), i))
    for aid, rows in chains.items():
        if len({(r[0], r[1]) for r in rows}) > 1:
            errs.append(f"alignment {aid}: mixed seqid/strand")
        iv = sorted((r[2], r[3]) for r in rows)
        for (s1, e1), (s2, _) in zip(iv, iv[1:]):
            if s2 <= e1:
                errs.append(f"alignment {aid}: overlapping segments")
                break
    return errs


# --------------------------------- weights ---------------------------------

def read_weights(path: Path):
    out = []
    for n, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        f = line.split()
        if len(f) != 3 or f[0] not in EVM_CLASSES:
            raise InputError(f"{path}:{n}: expected '<CLASS> <SOURCE> <WEIGHT>' with CLASS in {EVM_CLASSES}")
        try:
            float(f[2])
        except ValueError as exc:
            raise InputError(f"{path}:{n}: weight is not a number") from exc
        out.append((f[0], f[1], f[2]))
    return out


def fasta_ids(path: Path):
    with open(path) as fh:
        return {line[1:].split()[0] for line in fh if line.startswith(">")}


# ----------------------------------- main -----------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--outdir", type=Path)
    ap.add_argument("-w", "--weights", type=Path, help="weights template (config/evm_weights_aggregate.txt)")
    ap.add_argument("--genome", type=Path, help="optional FASTA; check every seqid exists")
    for opt in INPUTS:
        ap.add_argument(f"--{opt}", type=Path)
    ap.add_argument("--validate", type=Path, help="only validate an EVM GFF3 file")
    ap.add_argument("--kind", choices=["gene", "alignment"])
    args = ap.parse_args(argv)

    try:
        if args.validate:
            if not args.kind:
                ap.error("--validate needs --kind")
            fn = validate_gene_gff3 if args.kind == "gene" else validate_alignment_gff3
            errs = fn(args.validate.read_text().splitlines())
            for e in errs:
                print(f"[ERR] {e}", file=sys.stderr)
            print(f"[A4c] {args.validate}: {'OK' if not errs else f'{len(errs)} error(s)'}")
            return 1 if errs else 0

        if not args.outdir or not args.weights:
            ap.error("-o/--outdir and -w/--weights are required")
        given = {k: getattr(args, k) for k in INPUTS if getattr(args, k)}
        if args.braker and args.tsebra:
            raise InputError("--braker and --tsebra are alternatives: TSEBRA output is a selection "
                             "of the BRAKER1+2 models, giving both counts the same models twice")
        if not any(INPUTS[k][2] == "gene" for k in given):
            raise InputError("need at least one gene-prediction input (--braker/--tsebra/--augustus/--gemoma)")
        for k, p in given.items():
            if not p.is_file():
                raise InputError(f"--{k} {p}: file not found")
        if args.augustus and (args.braker or args.tsebra):
            print("[WARN] --augustus together with BRAKER/TSEBRA: BRAKER models are AUGUSTUS models; "
                  "make sure they are different runs", file=sys.stderr)
        if args.mikado and args.stringtie:
            print("[WARN] --mikado together with --stringtie: if Mikado was built from the same "
                  "StringTie GTF the transcript evidence is counted twice", file=sys.stderr)

        out = {"gene": [], "transcript": [], "protein": []}
        summary = []
        for k, p in given.items():
            cls, src, kind = INPUTS[k]
            if kind == "gene":
                lines, st = gene_prediction_lines(p, src)
            elif k == "pasa":
                lines, st = pasa_lines(p, src)
            elif kind == "transcript":
                lines, st = alignment_lines_from_exons(p, src)
            else:
                lines, st = miniprot_lines(p, src)
            if not lines:
                raise InputError(f"--{k} {p}: no usable records")
            out[kind].extend(lines)
            summary.append((cls, src, str(p), st))

        files = {"gene": "gene_predictions.gff3", "transcript": "transcript_alignments.gff3",
                 "protein": "protein_alignments.gff3"}
        errs = validate_gene_gff3(out["gene"])
        errs += validate_alignment_gff3(out["transcript"]) + validate_alignment_gff3(out["protein"])
        if args.genome:
            known = fasta_ids(args.genome)
            seen = {l.split("\t", 1)[0] for v in out.values() for l in v}
            errs += [f"seqid {s} not in {args.genome}" for s in sorted(seen - known)]
        if errs:
            raise InputError("validation failed:\n  " + "\n  ".join(errs))

        weights = read_weights(args.weights)
        present = [(cls, src) for cls, src, _, _ in summary]
        wmap = {(c, s): w for c, s, w in weights}
        missing = [f"{c}\t{s}" for c, s in present if (c, s) not in wmap]
        if missing:
            raise InputError(f"no weight in {args.weights} for: {', '.join(missing)}")

        args.outdir.mkdir(parents=True, exist_ok=True)
        for kind, name in files.items():
            target = args.outdir / name
            if out[kind]:
                target.write_text("\n".join(out[kind]) + "\n")
            elif target.exists():
                target.unlink()  # stale file from an earlier run would be picked up by A4d
        used = [(c, s, w) for c, s, w in weights if (c, s) in set(present)]
        (args.outdir / "weights.txt").write_text("".join(f"{c}\t{s}\t{w}\n" for c, s, w in used))
        with open(args.outdir / "summary.tsv", "w") as fh:
            fh.write("class\tsource\tweight\tinput\tcounts\n")
            for cls, src, path, st in summary:
                counts = ";".join(f"{k}={v}" for k, v in st.items())
                fh.write(f"{cls}\t{src}\t{wmap[(cls, src)]}\t{path}\t{counts}\n")
        for cls, src, path, st in summary:
            print(f"[A4c] {cls:<19} {src:<10} {st}")
        print(f"[A4c] wrote {args.outdir}/" + ", ".join(
            [files[k] for k in files if out[k]] + ["weights.txt", "summary.tsv"]))
        print("[A4c] next: A4d_evm_run.sh (EVM_INPUT_DIR=" + str(args.outdir) + ")")
        return 0
    except InputError as exc:
        print(f"[A4c error] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
