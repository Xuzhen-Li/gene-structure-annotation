# A2e — S11 gap-fill (after Liftoff)

Operational steps to turn **S11-lite** (lift-only, provisional L0) into full **S11** (lift + gap-fill + trunk QC → may reach L1).

There is **no** one-click “fill all gaps” binary in this repo. Honest path: identify holes → run orphan prediction on soft-masked genome or windows → merge → rejoin trunk.

Related: [`A2c_liftoff.md`](A2c_liftoff.md) · [`A2_run_draft.sh`](A2_run_draft.sh) · [`A4_merge_sets.sh`](A4_merge_sets.sh) · [`A2_protein_db.md`](A2_protein_db.md) · chooser: [`../docs/ROADMAP.md`](../docs/ROADMAP.md).

**Print-first:** every block below is for review. Use `RUN=1` / job scripts only after `GENOME_SOFT`, `PROTEIN_DB`, and lift GFF exist.

---

## When to keep S11-lite

Stay on **S11-lite** (`grade=L0`, `status=provisional`) when:

- You only need a quick coordinate transfer for exploration
- Gap-fill compute / RNA / proteins are not ready
- Lift quality is already poor (wrong ref) — gap-fill will not invent a close reference; switch to **S1/S2** instead

Do **not** relabel S11-lite as S11/L1 without gap-fill + gates.

---

## 1. Identify unmapped / broken loci

After Liftoff (`DRAFT_GFF` = lift GFF):

```bash
set -a && source config/local.env && set +a
: "${DRAFT_GFF:?liftoff GFF}"
: "${REF_GFF:?}"
: "${WORK_DIR:?}"
mkdir -p "$WORK_DIR/draft/gapfill"

# AGAT summary
bash pipeline/A5_agat_stats.sh "$DRAFT_GFF"

# Low-quality / partial lifts (attribute names vary by Liftoff version)
grep -E 'valid_ORF=False|partial_mapping|low_identity|extra_copy' "$DRAFT_GFF" \
  | tee "$WORK_DIR/draft/gapfill/suspect_lifts.txt" | head -n 50 || true

# Genes in REF_GFF with no (or broken) lift — approach depends on Liftoff version / -u unmapped list:
# If Liftoff wrote an unmapped list under liftoff_int, copy it:
# cp "$WORK_DIR/draft/liftoff_int/"*unmapped* "$WORK_DIR/draft/gapfill/" 2>/dev/null || true
```

Build a working definition of **holes** for METHODS, for example:

- Reference genes absent from lift GFF
- Models with `valid_ORF=False` / partial mapping you refuse to trust
- Large genomic spans with RNA/protein evidence but no lifted gene

Exact bed/ID lists are project-specific — record how you defined them.

---

## 2. Orphan prediction (BRAKER or GALBA)

Run a **de novo / EP** draft on soft-masked sequence to propose models in holes. Two honest scopes:

| Scope | When | How |
|-------|------|-----|
| **Whole-genome orphan draft** | Simpler ops; accept more overlap cleanup | `DRAFT_ENGINE=braker3` or `galba` → [`A2_run_draft.sh`](A2_run_draft.sh) writing a **second** GFF |
| **Windowed orphan draft** | Huge genome / want to limit CPU | Extract soft-masked windows around holes → BRAKER/GALBA per window → lift coordinates back (manual / bedtools — not automated here) |

Whole-genome example (second set → merge):

```bash
: "${GENOME_SOFT:?}"
: "${PROTEIN_DB:?}"   # see A2_protein_db.md
export DRAFT_ENGINE="${DRAFT_ENGINE:-braker3}"
# Keep lift as primary; orphan draft as B:
export DRAFT_GFF_B="$WORK_DIR/draft/orphan_braker.gff3"
# Temporarily point DRAFT_GFF at the orphan output path for the printer:
DRAFT_GFF="$DRAFT_GFF_B" bash pipeline/A2_run_draft.sh
# Review printed braker.pl/galba.pl → run on cluster → copy result to DRAFT_GFF_B
```

If you have RNA, prefer BRAKER with `RNA_BAM` for orphans. Proteins-only → GALBA with **close** proteins ([`A2_protein_db.md`](A2_protein_db.md)).

Windowed runs: document window BED, tool versions, and coordinate lift in METHODS — this repo does not ship a window driver.

---

## 3. Merge back

Prefer **lift as backbone**; add non-overlapping orphan models.

```bash
# Primary = Liftoff, B = orphan draft
export DRAFT_GFF="$WORK_DIR/draft/liftoff.gff3"
export DRAFT_GFF_B="$WORK_DIR/draft/orphan_braker.gff3"
export MERGE_MODE="${MERGE_MODE:-evm}"   # or tsebra / evi_backbone when wired
bash pipeline/A4_merge_sets.sh
# Follow printed EVM/TSEBRA steps; write MERGED_GFF
```

If A4 skips (no real B), you are still on lift-only → **S11-lite**.

Alternative honest policy (document it): keep lift GFF; manually / script-add orphans that do not overlap lift CDS — then set `MERGED_GFF` to that curated file without claiming a fake automated merger.

---

## 4. Rejoin trunk (required for full S11 / L1)

```text
MERGED_GFF (or curated lift+orphans)
  → A5 AGAT
  → A3 proteins
  → 01 BUSCO + PSAURON
  → 02 priority → 04 GSAman (depth per goal)
  → 06 release + METHODS (primary=S11)
```

Eval: [`../docs/EVALUATION.md`](../docs/EVALUATION.md) · checklist: [`../docs/EVALUATION_CHECKLIST.md`](../docs/EVALUATION_CHECKLIST.md).

---

## METHODS bullets (copy)

```text
Primary draft: S11 (Liftoff vFILL from REF_GFF FILL onto target; polish/copies FILL).
Gap-fill: orphan BRAKER/GALBA vFILL on soft-masked genome (or windows FILL);
  holes defined as FILL; merge via FILL (EVM/TSEBRA/manual non-overlap).
Not S11-lite: gap-fill + trunk QC performed before qualified claim.
```
