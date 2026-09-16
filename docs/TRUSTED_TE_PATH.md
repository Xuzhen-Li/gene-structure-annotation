# Trusted TE path — copy-paste checklist (A0)

**Goal:** soft-mask with a **trusted curatedlib** only → `GENOME_SOFT` for BRAKER / GALBA / …  
**Never** soft-mask with working lib, raw EDTA TElib, `cat`+CD-HIT mega-FASTA, or TEsorter `all.cls.lib`.

Full scheme: [`TE_LIBRARY.md`](TE_LIBRARY.md) · soft-mask: [`../pipeline/A0_softmask.md`](../pipeline/A0_softmask.md) · optional A0b: [`../pipeline/A0b_protexcluder.md`](../pipeline/A0b_protexcluder.md).

---

## Hard gate (both paths)

**No real `sha256` hex → forbid A0.**  
Placeholders `YOUR_SHA256`, `<paste>`, `FILL`, or a blank field are **not** provenance. Do not export `CLEAN_TE_LIB` / run RepeatMasker / claim Gate soft-mask until:

```bash
sha256sum "$TRUSTED_TE_LIB"
# METHODS gets the 64-char hex from THIS file — not a template token
```

---

## ① Near-species borrow (preferred when you are not building a panel lib)

Use a **named trusted curatedlib** from a near species / same panel. Not raw EDTA.

### Borrow checklist

- [ ] **Species / panel** of the donor lib: ________________
- [ ] **Source URL** (or public repo + release/tag; not a private cluster absolute path in METHODS): ________________
- [ ] **Filename** (exact): ________________
- [ ] **Version / date**: ________________
- [ ] **sha256** (64-char hex from `sha256sum` on the file you will soft-mask with): ________________
- [ ] Permission / citation OK for that file
- [ ] Still soft-mask with RepeatMasker `-xsmall` (or EDTA `--curatedlib` only for a TE track — see one-liner). Never hard-mask for BRAKER/GALBA

### Wire env

```bash
# After download — paths are yours; never commit private cluster paths
TRUSTED_TE_LIB="/path/to/donor_TElib_trusted_vX.fa"
sha256sum "$TRUSTED_TE_LIB" | tee "$WORK_DIR/mask/TRUSTED_TE_LIB.sha256"
# STOP if you only have YOUR_SHA256 / FILL / empty — forbid A0
export CLEAN_TE_LIB="$TRUSTED_TE_LIB"
```

### `--curatedlib` one-liner (EDTA TE-track optional; A0 soft-mask is usually RM)

```bash
# Optional: EDTA annotation pass with trusted curatedlib (new output dir; never --overwrite frozen discovery)
EDTA.pl --genome "$GENOME_FA" --species others --anno 1 \
  --curatedlib "$CLEAN_TE_LIB" --threads "$THREADS" \
  # ... other flags per docs/tools/edta.md — do NOT copy grape --u blindly
```

Gene-structure **A0** soft-mask (usual):

```bash
RepeatMasker -lib "$CLEAN_TE_LIB" -xsmall -pa "$THREADS" \
  -dir "$WORK_DIR/mask" "$GENOME_FA"
cp "$WORK_DIR/mask/$(basename "$GENOME_FA").masked" "$GENOME_SOFT"
```

### METHODS fill lines (borrow)

```text
TE soft-mask lib (borrowed trusted curatedlib):
  donor_species_or_panel: FILL
  source_URL_or_release: FILL
  filename: FILL_trusted_vX.fa
  version_or_date: FILL
  sha256: FILL_64hex
  why_borrow_OK: FILL (e.g. same-genus panel trusted v1.1)
  A0: RepeatMasker -xsmall with that file only; working/raw EDTA not used.
```

If any of `source_URL`, `filename`, `version_or_date`, or `sha256` is missing → **forbid A0** / do not claim G2 soft-mask pass.

---

## ② Own build via TE_LIBRARY layers (when you curate the panel yourself)

Tick in order (details: [`TE_LIBRARY.md`](TE_LIBRARY.md)):

- [ ] **01 discovery** — per-assembly / haplotype EDTA (provenance frozen; no casual `--overwrite`)
- [ ] **02 consensus** — TEtrimmer → CD-HIT ~95% → **working** lib (+ optional 80-80 family catalog)
- [ ] **03 classify** — TEsorter labels on working (does **not** replace the FASTA)
- [ ] **04 curation gate** — CDS BLAST + class filters → emit **trusted** FASTA
- [ ] **05 release product** — one trusted file for soft-mask
- [ ] **sha256** of that trusted product (real hex) → METHODS

```bash
ls -lh "$TRUSTED_TE_LIB"
sha256sum "$TRUSTED_TE_LIB" | tee "$WORK_DIR/mask/TRUSTED_TE_LIB.sha256"
export CLEAN_TE_LIB="$TRUSTED_TE_LIB"
# Then same RepeatMasker / optional EDTA --curatedlib one-liners as in ①
```

### METHODS fill lines (own build)

```text
TE library: EDTA → TEtrimmer → CD-HIT~95% working → TEsorter → CDS-gated trusted curatedlib.
  trusted_filename: FILL  version: FILL  sha256: FILL_64hex
Soft-mask: RepeatMasker -xsmall with trusted only; working ≠ curatedlib.
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
| Lib without recorded **sha256** | No provenance → forbid A0 |

---

## After A0

```bash
TRUSTED_TE_LIB="/path/to/species_TElib_trusted_vX.fa"
CLEAN_TE_LIB="$TRUSTED_TE_LIB"
GENOME_SOFT="/path/to/species.hap.softmasked.fa"
```

Verify `softmasked_fraction` ([`A0_softmask.md`](../pipeline/A0_softmask.md)) — homology to **this** trusted lib ≠ genome TE%.  
TE gene inflation later → overlay **S10** (remask with trusted → re-enter draft).
