# Mikado — pick best transcripts at overlapping loci

**Role:** Combiner alternative to EVM (RAGNAROK). Inputs: Helixer, StringTie, miniprot, TransDecoder, optional Liftoff/BRAKER GFFs + scoring YAML.

## Get it
https://github.com/EI-CoreBioinformatics/mikado  

Follow Mikado tutorial for `configure` → `prepare` → `serialise` → `pick`. For a batteries-included run, use upstream [RAGNAROK](https://github.com/ryandkuster/ragnarok).

## Plant tip
Use a scoring file that **penalizes Helixer microexons** (see RAGNAROK `plant_microexon_filter.yaml` note).
