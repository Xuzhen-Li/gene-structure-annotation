# GeMoMa — homology projection from an annotated genome

**Role:** Second (or primary) draft from a high-quality grape reference GFF+FA.

## Get it
- https://github.com/Jstacs/GeMoMa (Java; version CLI differs — read *your* jar’s help)

## Idea
Take gene models from `REF_FA` + `REF_GFF` (e.g. PN40024) and project them onto `GENOME_SOFT`.

## Pattern (version-dependent)
```bash
# Pseudocode — replace with GeMoMaPipeline CLI for your jar version:
java -jar GeMoMa-*.jar CLI GeMoMaPipeline \
  t="$REF_GFF" a="$REF_FA" g="$GENOME_SOFT" \
  outdir="$WORK_DIR/draft/gemoma" threads="$THREADS"
# Collect final GFF → DRAFT_GFF or DRAFT_GFF_B
```

## When to prefer GeMoMa vs Liftoff
| GeMoMa | Liftoff |
|--------|---------|
| Deeper homology scoring / intron length models | Faster lift, great for S4/S11 |
| Good second set for EVM | Good when structures already trusted |

## Pitfalls
- Wrong GeMoMa major version CLI (always `--help`).  
- Using a poor or outdated reference GFF as truth.
