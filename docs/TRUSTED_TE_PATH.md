# Trusted TE path — copy-paste checklist (A0)

**Goal:** soft-mask with a **trusted curatedlib** only → `GENOME_SOFT` for BRAKER / GALBA / …  
**Never** soft-mask with working lib, raw EDTA TElib, `cat`+CD-HIT mega-FASTA, or TEsorter `all.cls.lib`.

Full scheme: [`TE_LIBRARY.md`](TE_LIBRARY.md) · soft-mask commands: [`../pipeline/A0_softmask.md`](../pipeline/A0_softmask.md) · optional CDS purge: [`../pipeline/A0b_protexcluder.md`](../pipeline/A0b_protexcluder.md).

---

## Pick ONE path

### (A) Own build via TE_LIBRARY layers

Tick in order (see [`TE_LIBRARY.md`](TE_LIBRARY.md) lab order):

- [ ] **01 discovery** — per-assembly / haplotype EDTA (provenance frozen; no casual `--overwrite`)
- [ ] **02 consensus** — TEtrimmer → CD-HIT ~95% → **working** lib (+ optional 80-80 family catalog)
- [ ] **03 classify** — TEsorter labels on working (does **not** replace the FASTA)
- [ ] **04 curation gate** — CDS BLAST + class filters → emit **trusted** FASTA
- [ ] **05 release product** — one trusted file you will actually soft-mask with
- [ ] Record **filename + version + sha256** (and that working ≠ curatedlib)

```bash
# Example product checks (paths are yours — never commit private cluster paths)
ls -lh "$TRUSTED_TE_LIB"
sha256sum "$TRUSTED_TE_LIB" | tee "$WORK_DIR/mask/TRUSTED_TE_LIB.sha256"
export CLEAN_TE_LIB="$TRUSTED_TE_LIB"
```

METHODS must cite that sha256 (real hex), not a placeholder.

### (B) Near-species borrow (+ METHODS provenance)

When you **do not** build a panel TE library yourself:

- [ ] Source is a **named trusted curatedlib** from a near species / same panel (not raw EDTA dump)
- [ ] You have permission / public citation for that file
- [ ] METHODS fields filled (below)
- [ ] Still soft-mask with RepeatMasker `-xsmall` only — never hard-mask for BRAKER/GALBA

```text
METHODS — borrowed TE lib
  source_species / panel: FILL
  file: FILL_trusted_vX.fa
  version / date: FILL
  sha256: FILL
  why borrow OK: FILL (e.g. same genus panel trusted v1.1)
  note: working/raw EDTA not used for A0
```

### (C) Soft-mask command

Pointer only — run from [`../pipeline/A0_softmask.md`](../pipeline/A0_softmask.md):

```bash
# CLEAN_TE_LIB = trusted curatedlib (from A or B)
RepeatMasker -lib "$CLEAN_TE_LIB" -xsmall -pa "$THREADS" \
  -dir "$WORK_DIR/mask" "$GENOME_FA"
cp "$WORK_DIR/mask/$(basename "$GENOME_FA").masked" "$GENOME_SOFT"
# verify softmasked_fraction (homology to THIS lib ≠ genome TE%) — see A0_softmask.md
```

---

## Hard stop — never for A0

| Forbidden as `-lib` / `--curatedlib` | Why |
|-------------------------------------|-----|
| Raw EDTA `*.TElib.fa` / working discovery tree | Untrusted consensi + gene fragments |
| Entire **working** lib | Unknowns get 100% trust |
| `cat` haplotype TElibs + CD-HIT | Dedup ≠ curation |
| TEsorter `all.cls.lib` | Classifier output ≠ library |
| Hard-mask to `N` | Destroys sequence BRAKER needs |

---

## After A0

Export in `config/local.env`:

```bash
TRUSTED_TE_LIB="/path/to/species_TElib_trusted_vX.fa"
CLEAN_TE_LIB="$TRUSTED_TE_LIB"
GENOME_SOFT="/path/to/species.hap.softmasked.fa"
```

Then draft (S1/S2/S11/…) on `GENOME_SOFT`. TE gene inflation later → overlay **S10** (remask with trusted → re-enter draft).
