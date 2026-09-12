# 04 — GSAman curation (detailed)

Paper context: Chen, Chen & Xia (2026), *The Innovation* — last-mile gene structure.

## Order of work
1. Sort `priority.tsv` (worst PSAURON and boosted families first).  
2. Open locus ± flanking genes (tandems need neighbors).  
3. Classify error: fragmentation / fusion / exon-splice / tandem-collapse.  
4. Edit structure; save; export GFF periodically → `CURATED_GFF`.  
5. Append `curate/changelog.tsv`: `gene_id`, `class`, `date`, `note`.

## Round discipline
- Round 1: priority list only.  
- Re-run proteins + BUSCO + PSAURON.  
- Round 2 (S5): expanded BUSCO-fragment + tandem list.  
- Apply **S12** stop rules — do not infinite-polish.

## SynGAP (S4)
After Liftoff to other haplotypes, curate only SynGAP conflicts + priority families on each hap ([`05_syngap_polish.md`](05_syngap_polish.md)).

## Done when
`CURATED_GFF` exports cleanly and release checklist in [`../docs/PLAYBOOK.md`](../docs/PLAYBOOK.md) is ready.
