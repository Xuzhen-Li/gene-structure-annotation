# A2 — PROTEIN_DB for BRAKER / GALBA

`PROTEIN_DB` is the clade-matched protein FASTA passed to BRAKER (`--prot_seq`) or GALBA.  
Launcher: [`A2_run_draft.sh`](A2_run_draft.sh) · cards: [`../docs/tools/braker3.md`](../docs/tools/braker3.md) · [`../docs/tools/galba.md`](../docs/tools/galba.md).

**Print-first:** build/index offline; set `RUN=1` on draft only after `PROTEIN_DB` points at a real file.

---

## What to put in PROTEIN_DB

| Situation | Prefer |
|-----------|--------|
| Default S1 (RNA + proteins) | OrthoDB **clade** proteins for *your* lineage (e.g. Viridiplantae / eudicots / Poales) **or** a high-quality same-clade protein set |
| S2 / GALBA | **Close** relative proteins (same genus/family curated set) — not only a giant distant OrthoDB dump |
| Dual evidence | Same FASTA is fine; do not mix Metazoa proteins into a plant run |

Do **not** leave a copy-pasted Vitis/eudicots path when the genome is rice (Poales) or an animal.

---

## Layout (example)

```bash
set -a && source config/local.env && set +a
: "${WORK_DIR:?}"
DB_ROOT="${DB_ROOT:-$HOME/annot_dbs}"
mkdir -p "$DB_ROOT/proteins" "$WORK_DIR/proteins_db"

# Option 1 — OrthoDB / clade FASTA you already downloaded (path is yours):
#   e.g. OrthoDB Viridiplantae or eudicots protein FASTA from the OrthoDB / BRAKER docs
PROTEIN_FASTA="${PROTEIN_FASTA:-$DB_ROOT/proteins/OrthoDB_clade.faa}"

# Option 2 — concatenate a few trusted near-species proteomes (document sources in METHODS):
# cat speciesA.faa speciesB.faa > "$DB_ROOT/proteins/near_clade.faa"
# PROTEIN_FASTA="$DB_ROOT/proteins/near_clade.faa"

# BRAKER/GALBA take a protein FASTA; DIAMOND DB is optional (handy for your own homology QC):
export PROTEIN_DB="$PROTEIN_FASTA"
```

Record in METHODS: source name, release/date, approximate protein count, and that the set matches **your** clade.

---

## Optional: DIAMOND makedb (local homology / filters)

Not required by `A2_run_draft.sh`, but useful for sanity blastp / ProtHint-adjacent workflows:

```bash
: "${PROTEIN_DB:?}"
: "${THREADS:=16}"
OUT_DMND="${PROTEIN_DB%.faa}"
OUT_DMND="${OUT_DMND%.fasta}"
OUT_DMND="${OUT_DMND%.fa}"
diamond makedb --in "$PROTEIN_DB" -d "$OUT_DMND" --threads "$THREADS"
# DIAMOND looks for ${OUT_DMND}.dmnd
ls -lh "${OUT_DMND}.dmnd"
```

Swiss-Prot DIAMOND for **functional** annotation lives in the sibling repo ([`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation) `docs/INSTALL_FUNCTIONAL.md`) — different DB, different purpose.

---

## Wire into local.env

```bash
PROTEIN_DB="/path/to/YOUR_OrthoDB_or_clade.faa"
```

Then:

```bash
# review printed braker.pl / galba.pl
bash pipeline/A2_run_draft.sh
# when ready on the cluster: RUN=1 or paste the printed command into your job
```

## Pitfalls

- Metazoa OrthoDB on a plant genome (or the reverse)
- Feeding **all isoforms** of a messy annotation as “evidence” without documenting it
- Pointing `PROTEIN_DB` at a DIAMOND `.dmnd` path — BRAKER wants the **FASTA**
- Claiming GALBA with only distant OrthoDB when a close proteome exists (see peer notes in [`../docs/PEER_PIPELINES.md`](../docs/PEER_PIPELINES.md))
