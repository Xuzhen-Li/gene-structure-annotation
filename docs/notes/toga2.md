# TOGA2

- https://github.com/hillerlab/TOGA2 (use this; TOGA1 unmaintained)  
- Paper: bioRxiv TOGA2 (vertebrate annotation + orthology at scale).  
- Needs reference annotation + query genome + whole-genome alignment (chains / related pipelines).  
- Outputs gene models, orthology / loss / paralog handling, optional UTRs; `orthogroups` mode for CAFE5-style families.  
- Wrappers: Harvard `AnnotationTOGA` Snakemake.

**Adopt:** animal / vertebrate transfer lane beside Liftoff/LiftOn; not default for plants without a suitable WGA+reference pair.
