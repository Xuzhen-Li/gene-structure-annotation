#!/usr/bin/env python3
"""QA step 1: one protein per gene (longest CDS) for BUSCO and OMArk.

In:  --gff consensus GFF3; --proteins FASTA (IDs = mRNA IDs) and/or --genome FASTA
Out: <out>/longest_isoform.proteins.faa, <out>/longest_isoform.ids.tsv,
     <out>/metrics/qa01_longest_isoform.tsv
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa_common as qc  # noqa: E402

STEP = "qa01_longest_isoform"


def protein_for(t, proteins, genome):
    # match on the mRNA ID only; the gene is known from the GFF3 Parent link
    if proteins is not None:
        for key in (t.id,):
            if key and key in proteins:
                return proteins[key], "proteins"
    if genome is not None:
        cds = t.cds_sequence(genome)
        if cds:
            return qc.translate(cds), "genome"
    return None, None


def _strip_stop(prot: str) -> str:
    prot = prot.strip()
    return prot[:-1] if prot.endswith(("*", ".")) else prot


def pick_longest(models, proteins, genome):
    """Longest isoform per gene, grouped by the GFF3 Parent link.

    Same rule as pipeline/longest_isoform.py (PR #6): longest protein with the
    terminal stop not counted; ties go to the first transcript ID in sort order.
    Transcripts without a protein fall back to CDS length / 3.
    TODO: once pipeline/longest_isoform.py is on main, import its pick_longest
    instead of keeping this copy.
    """
    best: dict[str, tuple[int, str]] = {}
    seqs: dict[str, tuple[str | None, str | None]] = {}
    for t in qc.coding(models).values():
        prot, src = protein_for(t, proteins, genome)
        seqs[t.id] = (prot, src)
        length = len(_strip_stop(prot).rstrip("*.")) if prot else t.cds_length() // 3
        prev = best.get(t.gene)
        if prev is None or length > prev[0] or (length == prev[0] and t.id < prev[1]):
            best[t.gene] = (length, t.id)
    return {g: models[tid] for g, (_, tid) in best.items()}, seqs


def run(gff, out, proteins_fa=None, genome_fa=None):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    models = qc.read_models(gff)
    proteins = qc.read_fasta(proteins_fa) if proteins_fa else None
    genome = qc.read_fasta(genome_fa) if genome_fa else None
    reps, seqs = pick_longest(models, proteins, genome)
    records, missing, from_genome = [], 0, 0
    with open(out / "longest_isoform.ids.tsv", "w", encoding="utf-8") as fh:
        fh.write("gene_id\ttranscript_id\tcds_length\tprotein_source\n")
        for gene in sorted(reps):
            t = reps[gene]
            prot, src = seqs[t.id]
            fh.write(f"{gene}\t{t.id}\t{t.cds_length()}\t{src or 'missing'}\n")
            if not prot:
                missing += 1
                continue
            from_genome += src == "genome"
            records.append((t.id, _strip_stop(prot)))
    faa = out / "longest_isoform.proteins.faa"
    qc.write_fasta(faa, records)
    n_tx = len(qc.coding(models))
    rows = [
        ("coding_gene_count", len(reps), "genes with at least one CDS"),
        ("transcripts_per_gene_mean", qc.share(n_tx, len(reps)), "coding transcripts / coding genes"),
        ("longest_isoform_proteins", len(records), qc.rel(faa, out)),
        ("longest_isoform_missing_protein", missing,
         "listed as 'missing' in longest_isoform.ids.tsv" if missing else ""),
        ("longest_isoform_translated_from_genome", from_genome, ""),
    ]
    qc.write_metrics(out, STEP, rows)
    return faa


def main(argv=None):
    ap = qc.base_parser(__doc__.splitlines()[0])
    ap.add_argument("--proteins", help="protein FASTA from the consensus GFF3")
    ap.add_argument("--genome", help="genome FASTA (used when a protein is missing)")
    a = ap.parse_args(argv)
    if not a.proteins and not a.genome:
        ap.error("give --proteins and/or --genome")
    run(a.gff, a.out, a.proteins, a.genome)


if __name__ == "__main__":
    main()
