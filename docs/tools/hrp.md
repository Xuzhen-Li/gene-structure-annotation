# HRP — NB-LRR / NLR helpers

**Role:** F8 optional full-length resistance-gene refinement after InterProScan filter.

**Software:** [AndolfoG/HRP](https://github.com/AndolfoG/HRP)

## In this playbook

1. Run F1.3 InterProScan → `bash pipeline/F8_run.sh` for domain-based candidates.  
2. Optionally run HRP on `$PROTEINS_FA` per upstream README → `$FUNCTION_DIR/nlr/hrp/`.  
3. Cite HRP software + your IPS version in METHODS.

Scenario **F8**.
