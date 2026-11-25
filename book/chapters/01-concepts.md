# Chapter 1. Concepts and principles

## 1.1 What structural annotation produces

Structural annotation finds genes on an assembled genome and writes their coordinates as GFF3, together with the predicted proteins (README, Overview). A gene model is a hierarchy: a gene contains one or more transcripts (mRNA), and each transcript is made of exons, coding sequence (CDS) and untranslated regions (UTR). The names of these parts come from the Sequence Ontology, a controlled vocabulary for the parts of a genomic annotation that makes data exchange and automated reasoning possible ([doi:10.1186/gb-2005-6-5-r44](https://doi.org/10.1186/gb-2005-6-5-r44)). Function (GO, KEGG, names) is a separate layer handled in the sibling repository gene-function-annotation (README, Overview).

## 1.2 Why plant genomes are hard

Plant genomes are large, rich in transposable elements and often polyploid, and annotation software is mostly developed on model organisms without broad benchmarks ([doi:10.1002/aps3.11533](https://doi.org/10.1002/aps3.11533)). Errors spread: a survey of 30 recently annotated genomes found 605 confirmed chimeric gene models, where adjacent genes were fused into one, most of them in invertebrates and plants ([doi:10.1186/s12864-025-11765-w](https://doi.org/10.1186/s12864-025-11765-w)). Annotation choices also change later analyses: four annotation sources for the same genomes gave markedly different orthology inferences ([doi:10.1093/bioinformatics/btaf365](https://doi.org/10.1093/bioinformatics/btaf365)).

## 1.3 Kinds of evidence

- **Transcript evidence.** Short RNA-seq reads are aligned and assembled into transcripts; long reads can give full-length isoforms. The RGASP benchmark showed that most tools find exons well but assembling complete isoforms remains a major challenge ([doi:10.1038/nmeth.2714](https://doi.org/10.1038/nmeth.2714)).
- **Protein evidence.** Proteins from related species are aligned to the genome with spliced alignment. The authors of miniprot report that it is tens of times faster than older aligners with comparable accuracy ([doi:10.1093/bioinformatics/btad014](https://doi.org/10.1093/bioinformatics/btad014)).
- **Ab initio prediction.** Statistical gene finders such as AUGUSTUS and the GeneMark family learn gene structure from the genome itself. The independent G3PO benchmark found ab initio structure prediction very challenging on draft assemblies ([doi:10.1186/s12864-020-6707-9](https://doi.org/10.1186/s12864-020-6707-9)).
- **Deep learning.** Helixer and Tiberius combine neural networks with a hidden Markov model. Helixer offers pretrained models for fungi, plants, vertebrates and invertebrates that need no RNA-seq ([doi:10.1038/s41592-025-02939-1](https://doi.org/10.1038/s41592-025-02939-1)); Tiberius was trained and tested on mammals ([doi:10.1093/bioinformatics/btae685](https://doi.org/10.1093/bioinformatics/btae685)).
- **Transfer from a related annotation.** Liftoff maps genes between assemblies of the same or closely related species ([doi:10.1093/bioinformatics/btaa1016](https://doi.org/10.1093/bioinformatics/btaa1016)); LiftOn adds protein alignments to reach more distant species ([doi:10.1101/gr.279620.124](https://doi.org/10.1101/gr.279620.124)).

## 1.4 Soft-masking repeats

Repeats and transposable elements produce false gene calls if they are left unmarked. Soft-masking writes repeat bases in lower case so that predictors can down-weight them without removing sequence. In this repository the mask uses a trusted TE library built in vitis-te; the step soft-masks only and never hard-masks for BRAKER or GALBA, and the soft-masked fraction measures similarity to that library, not the TE percentage of the genome (`examples/plant_sim/01_vitis_s1_s7/plan.md` and `env.snippet`).

## 1.5 Combining evidence

No single kind of evidence is enough. A plant benchmark of BRAKER and MAKER on five genomes found that transcripts from RNA alignments alone are not sufficient and recommends combining evidence-based and ab initio prediction ([doi:10.1002/aps3.11533](https://doi.org/10.1002/aps3.11533)). EVidenceModeler builds a weighted consensus of all evidence, and its authors report quality approaching manual curation on rice and human ([doi:10.1186/gb-2008-9-1-r7](https://doi.org/10.1186/gb-2008-9-1-r7)). BRAKER3 uses RNA-seq and a protein database together and outperformed BRAKER1, BRAKER2, MAKER2, Funannotate and FINDER on 11 genomes ([doi:10.1101/gr.278090.123](https://doi.org/10.1101/gr.278090.123)).

## 1.6 Measuring quality

Completeness tools (BUSCO, compleasm) count conserved single-copy genes; compleasm reports a 14-fold speed-up over BUSCO on human assemblies ([doi:10.1093/bioinformatics/btad595](https://doi.org/10.1093/bioinformatics/btad595)). OMArk also checks consistency with related species and reports contamination ([doi:10.1038/s41587-024-02147-w](https://doi.org/10.1038/s41587-024-02147-w)). PSAURON scores each protein for how likely it is to be a real coding sequence ([doi:10.1093/nargab/lqae189](https://doi.org/10.1093/nargab/lqae189)). The repository acceptance levels (L0, L1, L2) are defined in [`docs/EVALUATION.md`](../../docs/EVALUATION.md).

## 1.7 Names

Gene identifiers and names follow community rules; for grapevine the International Grapevine Genome Project set up a nomenclature system ([doi:10.1186/1471-2164-15-1077](https://doi.org/10.1186/1471-2164-15-1077)).
