# Peer structural pipelines (biology-wide)

Further reading only — not a claim that this repo copies any third-party project wholesale.  
Canonical spine: [`PLAYBOOK.md`](PLAYBOOK.md) · [`steps/MAIN.md`](steps/MAIN.md).  
Functional FA after proteins: [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation).

## Already integrated / previously noted

| Peer | Lane | Our hook |
|------|------|----------|
| BRAKER3 / BRAKER4 | Default S1 ETP | `docs/tools/braker4.md`, S1 |
| GALBA | Protein-only S2 | `docs/tools/galba.md` |
| GeMoMa / Liftoff / LiftOn | Homology / transfer | S1–S4, S11 |
| nf-annotate · nf-core/genomeannotator | Nextflow stacks | notes in FA repo historically |
| funannotate (v1) | Fungi-first eukaryote | `docs/notes` / FA notes |
| EVM / PASA (S14) | Consensus | `docs/steps/dclab/` |
| GSAman | Last-mile | `docs/tools/gsaman.md` |

## New haul (2026-09-12)

### GALBA2 — protein-only, large genomes

- https://github.com/Gaius-Augustus/GALBA2  
- Snakemake rewrite of GALBA on the BRAKER4 container stack; miniprot → miniprothint → AUGUSTUS.  
- **When:** no usable RNA; **close** related proteins (not giant OrthoDB dump). Scales better than BRAKER-EP on large/repeat-rich genomes.  
- **Our mapping:** optional S2 path beside classic `galba.pl`; keep BRAKER4 EP when only distant OrthoDB proteins exist.  
- Note: [`notes/galba2.md`](notes/galba2.md)

### TOGA2 — vertebrate / WGA transfer + orthology

- https://github.com/hillerlab/TOGA2 (TOGA1 deprecated)  
- Exon-aware annotation transfer from reference via whole-genome alignments; orthology / loss calls; scales to thousands of vertebrate assemblies (bioRxiv TOGA2).  
- Companion wrappers: https://github.com/harvardinformatics/AnnotationTOGA  
- **When:** mammals/birds/fish/etc. with a good reference + chain/HAL alignment; not a substitute for de novo when no WGA exists.  
- **Our mapping:** animal-side peer to Liftoff/LiftOn (S4/S11); combine with BRAKER/RNA when evidence exists (Harvard GenomeAnnotation pattern).  
- Note: [`notes/toga2.md`](notes/toga2.md)

### funannotate2 (+ addons) — fungi / general eukaryotes

- https://github.com/nextgenusfs/funannotate2 · docs: https://funannotate2.readthedocs.io/  
- clean → train → predict → annotate; Docker with HelixerLite etc.  
- Addons: https://github.com/nextgenusfs/funannotate2-addons (eggNOG, InterProScan, antiSMASH, SignalP).  
- **When:** fungal genomes (primary), other eukaryotes as alternate stack.  
- **Our mapping:** structure peer for fungi (parallel to S1/S14); FA pieces → hand proteins to gene-function-annotation **or** funannotate2-addons (eggNOG/IPS align with our F1).  
- Note: [`notes/funannotate2.md`](notes/funannotate2.md)

### Harvard Informatics Annotation* wrappers

- https://github.com/harvardinformatics/GenomeAnnotation (BRAKER, Liftoff, TOGA, MAKER, RNA-seq assembly tutorials)  
- Genome Research 2025 comparative annotation essay (tree-of-life liftoff / TOGA / BRAKER patterns).  
- **Our mapping:** teaching parallels; does not replace our S-branch table.

## Still thin / watchlist (not yet fleshed)

| Idea | Why interesting |
|------|-----------------|
| MetaEuk | Eukaryotic proteins on metagenomic contigs |
| FINDER | RNA+homology combiner (BRAKER3 paper compares) |
| Earl Grey / EDTA-class TE | Soft-mask peers beyond EDTA |
| Mycotools | Fungal comparative DB / GFF ops (not a predictor) |

## How to use this list

1. Pick **one** evidence branch in `SCENARIOS.md`.  
2. Only swap in a peer when evidence matches (GALBA2 ≠ distant OrthoDB; TOGA2 needs WGA).  
3. Rejoin at AGAT → proteins → BUSCO → qualify.  
4. Do not widen every run into “run all peers”.
