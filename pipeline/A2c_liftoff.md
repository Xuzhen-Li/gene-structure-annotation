# A2c — Liftoff (detailed)

Used in S1 (second set), S2, S4, S6, **S11** / **S11-lite**.  
Tool card: [`../docs/tools/liftoff.md`](../docs/tools/liftoff.md). Gap-fill after lift: [`A2e_s11_gapfill.md`](A2e_s11_gapfill.md).

**Print-first:** review the block; run on the cluster only when `REF_*` and `GENOME_FA` are real.

## Env + pasteable CLI

```bash
set -a && source config/local.env && set +a
: "${REF_FA:?reference genome FASTA}"
: "${REF_GFF:?reference annotation GFF3}"
: "${GENOME_FA:?target genome FASTA}"
: "${WORK_DIR:?}"
THREADS="${THREADS:-16}"
mkdir -p "$WORK_DIR/draft/liftoff_int"
OUT="${DRAFT_GFF:-$WORK_DIR/draft/liftoff.gff3}"

liftoff -g "$REF_GFF" \
  -o "$OUT" \
  -dir "$WORK_DIR/draft/liftoff_int" \
  -p "$THREADS" \
  -polish \
  -copies \
  "$GENOME_FA" "$REF_FA"

# S11 primary draft:
export DRAFT_GFF="$OUT"
# S1 dual-track second set instead:
# export DRAFT_GFF_B="$OUT"
```

## After Liftoff

```bash
bash pipeline/A5_agat_stats.sh "$OUT"
# Inspect low-quality lifts (attribute names vary by Liftoff version):
grep -E 'valid_ORF=False|partial_mapping|low_identity' "$OUT" | head -n 50 || true
```

---

## S11 vs S11-lite — stop here or continue

| Claim | What you did | METHODS |
|-------|--------------|---------|
| **S11-lite** | Liftoff (± AGAT stats) **only** — **no** gap-fill | `primary=S11-lite` · `grade=L0` · `status=provisional` — **not** L1/qualified |
| **S11** (full) | Liftoff **+** orphan/gap-fill ([`A2e_s11_gapfill.md`](A2e_s11_gapfill.md)) **+** trunk QC (A3 → 01 → … → 06) | `primary=S11` · may reach `grade=L1` + `status=qualified` when gates pass |

```text
STOP for S11-lite: after A5_agat_stats on liftoff GFF → provisional release language only.
CONTINUE for S11:   A2e gap-fill → merge (A4 if dual sets) → proteins → BUSCO/PSAURON → curation → release.
```

## Notes

- Prefer a **curated** close reference (e.g. polished PN40024 for grape) — not a half-done GFF.  
- `-copies` helps tandem arrays but can create extras — GSAman NLR / tandem windows (S7).  
- Half-done Liftoff or untrusted ref → do **not** hard-claim S11/L1; switch to S1 or stay provisional.
