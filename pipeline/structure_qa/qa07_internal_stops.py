#!/usr/bin/env python3
"""QA step 7: internal stop codons, start/stop presence and CDS frame.

In:  --gff consensus GFF3; --genome FASTA; --proteins FASTA (optional, checked too)
Out: <out>/internal_stops.tsv, <out>/metrics/qa07_internal_stops.tsv
All coding transcripts are checked, not only the longest isoform.
A stop ('*' or '.') at the very end is a terminal stop, not an internal one.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa_common as qc  # noqa: E402

STEP = "qa07_internal_stops"


def protein_stops(seq: str) -> tuple[int, bool]:
    """(internal stops, has terminal stop). Stops may be '*' or '.' (gffread -y)."""
    seq = seq.strip()
    terminal = seq.endswith(("*", "."))
    body = seq[:-1] if terminal else seq
    return body.count("*") + body.count("."), terminal


def run(gff, out, genome_fa, proteins_fa=None, config=None):
    qc.load_config(config)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    models = qc.coding(qc.read_models(gff))
    genome = qc.read_fasta(genome_fa)
    n = bad = no_start = no_stop = frame = missing_seq = 0
    with open(out / "internal_stops.tsv", "w", encoding="utf-8") as fh:
        fh.write("transcript_id\tgene_id\tsource\tinternal_stops\n")
        for t in sorted(models.values(), key=lambda x: x.id):
            cds = t.cds_sequence(genome)
            if cds is None:
                missing_seq += 1
                continue
            n += 1
            frame += len(cds) % 3 != 0
            prot = qc.translate(cds)
            no_start += not prot.startswith("M")
            no_stop += not prot.endswith("*")
            body = prot[:-1] if prot.endswith("*") else prot
            stops = body.count("*")
            if stops:
                bad += 1
                fh.write(f"{t.id}\t{t.gene}\tgenome\t{stops}\n")
        prot_bad = prot_term = None
        n_prot = 0
        if proteins_fa:
            prot_bad = prot_term = 0
            for name, seq in sorted(qc.read_fasta(proteins_fa).items()):
                n_prot += 1
                internal, terminal = protein_stops(seq)
                prot_term += terminal
                if internal:
                    prot_bad += 1
                    fh.write(f"{name}\t\tproteins_fasta\t{internal}\n")
    note = f"transcripts checked={n}; seqid missing from genome={missing_seq}"
    rows = [
        ("internal_stop_share", qc.share(bad, n), note),
        ("internal_stop_count", bad if n else None, "listed in internal_stops.tsv"),
        ("protein_fasta_internal_stop_count", prot_bad,
         "" if proteins_fa else "no --proteins given"),
        ("protein_fasta_terminal_stop_share", qc.share(prot_term or 0, n_prot) if n_prot else None,
         "proteins ending in '*' or '.'; not an error" if proteins_fa else "no --proteins given"),
        ("cds_not_multiple_of_3_share", qc.share(frame, n), "after first-CDS phase"),
        ("missing_start_codon_share", qc.share(no_start, n), "partial models allowed"),
        ("missing_stop_codon_share", qc.share(no_stop, n), "partial models allowed"),
    ]
    qc.write_metrics(out, STEP, rows)


def main(argv=None):
    ap = qc.base_parser(__doc__.splitlines()[0])
    ap.add_argument("--genome", required=True)
    ap.add_argument("--proteins")
    a = ap.parse_args(argv)
    run(a.gff, a.out, a.genome, a.proteins, a.config)


if __name__ == "__main__":
    main()
