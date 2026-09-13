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



## Mainstream / high-citation stacks

| Peer | Why it matters | Our hook |
|------|----------------|----------|
| **MAKER2** | BMC Bioinformatics 2011; decades of genome papers; AED QC | Alternate full stack; [`notes/maker2.md`](notes/maker2.md) |
| **AUGUSTUS · GeneMark · SNAP** | Classic ab initio engines inside BRAKER/MAKER | [`notes/classic_abinitio.md`](notes/classic_abinitio.md) |
| **EVM · PASA** | Haas consensus + transcript polish | **S14** `docs/steps/dclab/` |
| **NCBI EGAPx** | Institutional eukaryotic annotation | Optional S8-class peer (`pipeline/A2d_egapx_optional.md`) |
| **StringTie + aligners** | Standard RNA evidence path | S1 inputs |

Do not replace the default S1 spine with MAKER unless the lab already standardizes on it.

## AI-driven ab initio

| Peer | Venue / lab | Our hook |
|------|-------------|----------|
| **Helixer** | *Nat Methods* 2025; Usadel/Weber | **S13**; [`notes/helixer.md`](notes/helixer.md) |
| **Tiberius** | *Bioinformatics* 2024 (+ multi-clade); Stanke/Hoff | S13-class peer; [`notes/tiberius.md`](notes/tiberius.md) |
| **ANNEVO** | Kai Ye 叶凯 / XJTU `xjtu-omics`; genomic MoE LM | S13-class peer; [`notes/annevo.md`](notes/annevo.md) |
| **OrionGeno** | BGI Research; phylogeny-aware DL | S13-class; [`notes/oriongeno.md`](notes/oriongeno.md) |

**Rule:** AI drafts are evidence-light starts. Soft-mask first; still run protein BUSCO / PSAURON; when RNA+proteins exist, prefer **S1 BRAKER** and treat AI GFFs as comparison tracks (or EVM inputs with low–medium weight), not automatic truth.

## Kai Ye group (叶凯 / XJTU-omics)

| Tool | Role |
|------|------|
| **ANNEVO** | Primary gene-structure contribution for this playbook (ab initio LM). See [`notes/annevo.md`](notes/annevo.md). |
| Other XJTU-omics tools (assembly / SV / T2T helpers) | Out of scope here unless they emit GFF gene models; link from assembly notes if needed. |

License caution: ANNEVO is **non-commercial** — keep that explicit in METHODS and redistributed recipes.



## More peers (2026-09-13 haul)

### Evidence / transfer

| Peer | Notes | Hook |
|------|-------|------|
| **EviAnn** | *Nat Methods* 2026 evidence-only (no ab initio) | S3-class; [`notes/eviann.md`](notes/eviann.md) |
| **FINDER** | *BMC Bioinformatics* 2021; RNA→BRAKER2 automation | S1 alternate; [`notes/finder.md`](notes/finder.md) |
| **CAT** | Cactus HAL clade annotation (Fiddes et al.) | Multi-genome / T2T; [`notes/cat.md`](notes/cat.md) |
| **LiftOn** | Liftoff + miniprot protein-max | S4/S11; [`notes/lifton.md`](notes/lifton.md) |

### Soft-mask / TE

| Peer | Notes | Hook |
|------|-------|------|
| **Earl Grey** | *MBE* 2024 automated TE curation | A0 peer; [`notes/earlgrey.md`](notes/earlgrey.md) |

### Metagenome eukaryotes

| Peer | Notes | Hook |
|------|-------|------|
| **MetaEuk** | *Microbiome* 2020; Soeding lab | MAG/contig lane; [`notes/metaeuk.md`](notes/metaeuk.md) |

### Functional (sibling repo)

KO/GO peers for after proteins exist — see gene-function-annotation notes: DeepKOALA, BlastKOALA/GhostKOALA, DeepGOPlus. Default FA spine remains F1.


## Still thin / watchlist (not yet fleshed)

| Idea | Why interesting |
|------|-----------------|
| Mycotools | Fungal comparative DB / GFF ops (not a predictor) |
| More Ye-lab GFF emitters | Only if they publish gene-model tools beyond ANNEVO |
| ProteInfer / DeepFRI | Enzyme / GO DL — track in FA repo |
| NCBI RefSeq eukaryotic pipeline docs | Institutional compare |



## Deep hunt (2026-09-13b) — complexity layers

Gene annotation is not one tool: **mask → evidence transcripts → ab initio/AI → homology transfer → combiner → QC → (optional) FA**.

### Long-read / transcript evidence

| Peer | Venue | Hook |
|------|-------|------|
| **IsoQuant** | *Nat Biotechnol* 2023 | S3 LR discovery; [`notes/isoquant.md`](notes/isoquant.md) |
| **SQANTI3** | *Nat Methods* 2024 | LR QC/filter/rescue; [`notes/sqanti3.md`](notes/sqanti3.md) |
| **Mikado + Portcullis** | Earlham | Multi-assembler pick; S13; [`notes/mikado_portcullis.md`](notes/mikado_portcullis.md) |

### Protein homology aligners

| Peer | Hook |
|------|------|
| **miniprot · Spaln** (+ GenomeThreader/Exonerate legacy) | S1/S2/S14 evidence; [`notes/miniprot_spaln.md`](notes/miniprot_spaln.md) |

### Institutional / automated stacks

| Peer | Hook |
|------|------|
| **EGAPx / Gnomon** | NCBI public EGAP; GenBank 2026 path; S8; [`notes/egapx_gnomon.md`](notes/egapx_gnomon.md) |
| **MoGAAAP** | Liftoff+Helixer provisional + OMArk/BUSCO; [`notes/mogaaap.md`](notes/mogaaap.md) |

### QC beyond single BUSCO number

| Peer | Hook |
|------|------|
| **OMArk · compleasm** | Consistency + fast completeness; A5b; [`notes/omark_compleasm.md`](notes/omark_compleasm.md) |

### FA complexity (sibling)

After proteins: F1 core stays DIAMOND+eggNOG+InterProScan. DL/KO extras: ProteInfer, DeepFRI, DeepKOALA, IsoAnnot/FIT — see gene-function-annotation notes.




## Deep hunt fold-in (2026-09-13c) — executor haul

Verified extras beyond prior sections (skipping duplicates already listed).

### AI / Chinese full stacks
| Peer | Hook |
|------|------|
| **OrionGeno** (BGI) | S13-class AI ab initio; [`notes/oriongeno.md`](notes/oriongeno.md) |
| **GETA** | One-command CN pipeline; [`notes/geta.md`](notes/geta.md) |

### Protein evidence engines
| Peer | Hook |
|------|------|
| **ProtHint · miniprothint** | BRAKER-EP vs GALBA2 lanes; [`notes/prothint_miniprothint.md`](notes/prothint_miniprothint.md) |
| **CESAR2.0** | WGA exon realign (w/ TOGA); [`notes/cesar2.md`](notes/cesar2.md) |
| ProSplign · GenomeThreader · Exonerate | Institutional/legacy transfer (EGAPx/Ensembl/MAKER) |

### Transcriptomes (short + long)
| Peer | Hook |
|------|------|
| **LR peers** (bambu, FLAIR, FLAMES, TALON, PsiCLASS, Scallop2) | [`notes/lr_isoform_peers.md`](notes/lr_isoform_peers.md) |

### Combiners / QC packs / side-lanes
| Peer | Hook |
|------|------|
| **combinr · InGenAnnot** | EVM/TSEBRA peers; [`notes/combinr_ingenannot.md`](notes/combinr_ingenannot.md) |
| **PSAURON · GAQET2 · AnnoAudit** | QC packs; [`notes/psauron_gaqet_annoaudit.md`](notes/psauron_gaqet_annoaudit.md) |
| **tRNAscan-SE · Infernal/Rfam · TEsorter** | ncRNA + TE class; [`notes/ncrna_tesorter.md`](notes/ncrna_tesorter.md) |

### FA (sibling)
NetGO 3.0, dbCAN3, DeepLoc 2.0, SignalP 6.0 — gene-function-annotation notes.


## How to use this list

1. Pick **one** evidence branch in `SCENARIOS.md`.  
2. Only swap in a peer when evidence matches (GALBA2 ≠ distant OrthoDB; TOGA2 needs WGA).  
3. Rejoin at AGAT → proteins → BUSCO → qualify.  
4. Do not widen every run into “run all peers”.
