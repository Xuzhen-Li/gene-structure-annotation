#!/usr/bin/env python3
"""flow.py — Step-1 flow tool for gene-structure-annotation.

User answers → automatic branch pick → narrated stage plan
(inputs, software purpose, process, outputs).

Honesty: this version PLANS and optionally PRINTS helper commands.
It does not silently run BRAKER/EVM on the cluster. Later steps can
wire dry-run → execute where safe.

Usage:
  python3 pipeline/flow_tool/flow.py --answers pipeline/flow_tool/answers.yaml
  python3 pipeline/flow_tool/flow.py --answers answers.yaml --emit-commands -o plan.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


REPO = Path(__file__).resolve().parents[2]


def load_answers(path: Path) -> dict:
    text = path.read_text()
    if yaml is not None:
        data = yaml.safe_load(text)
    else:
        # Minimal YAML subset: key: value (bool/str)
        data = {}
        for line in text.splitlines():
            s = line.split("#", 1)[0].strip()
            if not s or ":" not in s:
                continue
            k, v = s.split(":", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if v.lower() in ("true", "yes"):
                v = True
            elif v.lower() in ("false", "no"):
                v = False
            data[k] = v
    if not isinstance(data, dict):
        raise SystemExit(f"answers file must be a mapping: {path}")
    return data


def choose_branch(a: dict) -> dict:
    """Return primary draft + overlays from ROADMAP chooser."""
    goal = str(a.get("goal", "qualified")).lower()
    overlays = []
    if a.get("multi_hap"):
        overlays.append("S4")
    if goal in ("paper_t2t", "paper", "t2t", "l2"):
        overlays.append("S5")
    if a.get("plant_tandem_focus"):
        overlays.append("S7")

    if a.get("close_curated_ref"):
        primary = "S11"
        reason = "Close curated reference → liftover first (Ji NRG 2026)."
    elif a.get("want_evm_pasa"):
        primary = "S14"
        reason = "User requested classic PASA→EVM→polish stack."
    elif a.get("deep_isoseq"):
        primary = "S3"
        reason = "Deep Iso-seq / evidence CDS → IsoQuant/SQANTI (± EviAnn)."
    elif a.get("has_rna") and a.get("has_proteins"):
        primary = "S1"
        reason = "RNA + proteins, no close ref → BRAKER4/3 + StringTie compare."
    elif a.get("has_proteins") and not a.get("has_rna"):
        primary = "S2"
        reason = "Proteins only → GALBA/GALBA2/GeMoMa."
    elif a.get("want_gpu_abinitio_compare") and not a.get("has_rna"):
        primary = "S13"
        reason = "Thin evidence + GPU ab initio compare (not a silent S1 replace)."
    elif not a.get("has_rna") and not a.get("has_proteins"):
        primary = "S6"
        reason = "Thin evidence → provisional homology-first."
    else:
        primary = "S1"
        reason = "Default fallback: S1 when unsure with any RNA/proteins signal."

    if a.get("want_gpu_abinitio_compare") and primary != "S13":
        overlays.append("S13_compare")

    grade = {"provisional": "L0", "qualified": "L1", "paper_t2t": "L2", "paper": "L2", "t2t": "L2", "l2": "L2"}.get(
        goal, "L1"
    )
    if primary in ("S6",) or (primary == "S11" and grade != "L2"):
        # raw liftover stays provisional until QC unless user forces L2 path with gap-fill
        if primary == "S6":
            grade = "L0"

    return {
        "primary": primary,
        "overlays": overlays,
        "reason": reason,
        "grade_target": grade,
    }


def stages_for(choice: dict, a: dict) -> list[dict]:
    """Ordered narrated stages. Each: id, title, inputs, software, process, outputs, helper."""
    primary = choice["primary"]
    stages = []

    def add(sid, title, inputs, software, process, outputs, helper=""):
        stages.append(
            {
                "id": sid,
                "title": title,
                "inputs": inputs,
                "software": software,
                "process": process,
                "outputs": outputs,
                "helper": helper,
            }
        )

    add(
        "Asm0",
        "Assembly / haplotype decision",
        "Raw HiFi / Hi-C / ONT (or an already-finished genome FASTA).",
        "Assembler stack you already trust (hifiasm, etc.) — see pipeline/Asm0_assembly.md.",
        "Build or accept GENOME_FA; write down ploidy / hap choice.",
        "GENOME_FA with stable headers.",
        "pipeline/Asm0_assembly.md",
    )
    add(
        "Asm1",
        "Assembly QC gate",
        "GENOME_FA",
        "BUSCO (genome mode), seqkit/QUAST-style stats.",
        "Decide ASSEMBLY_OK for your clade; set lineage name explicitly.",
        "Asm1 notes; ASSEMBLY_OK=yes|no.",
        "pipeline/Asm1_assembly_qc.md",
    )
    add(
        "A0",
        "Soft-mask with trusted TE library",
        "GENOME_FA + trusted curatedlib (not raw EDTA / not full working lib).",
        "RepeatMasker -xsmall; TE scheme in docs/TE_LIBRARY.md; optional ProtExcluder (A0b).",
        "Soft-mask only; never hard-mask for BRAKER/GALBA.",
        "GENOME_SOFT (+ lib version/sha in METHODS).",
        "pipeline/A0_softmask.md · docs/TE_LIBRARY.md",
    )

    if a.get("has_rna") and primary in ("S1", "S3", "S14", "S5"):
        add(
            "A1b",
            "RNA alignment",
            "RNA FASTQ + GENOME_FA/SOFT",
            "HISAT2 or STAR (short); minimap2 for long reads if Iso-seq.",
            "Produce stranded BAM suitable for BRAKER / StringTie / PASA.",
            "RNA_BAM (+ index).",
            "pipeline/A1b_rna_align.md",
        )

    if primary == "S11":
        add(
            "S11",
            "Liftover-first draft",
            "REF_FA + REF_GFF + target GENOME_SOFT",
            "Liftoff / LiftOn / CAT (± TOGA2 if WGA).",
            "Transfer models; mark provisional until QC; plan gap-fill with S1/S2.",
            "Lifted DRAFT_GFF (status=provisional until G7).",
            "pipeline/A2c_liftoff.md",
        )
    elif primary == "S2":
        add(
            "S2",
            "Protein-only draft",
            "GENOME_SOFT + PROTEIN_DB",
            "GALBA / GALBA2 / GeMoMa.",
            "Homology-driven gene calling without claiming complete UTRs.",
            "DRAFT_GFF",
            "pipeline/A2_run_draft.sh (engine=galba)",
        )
    elif primary == "S3":
        add(
            "S3",
            "Iso-seq / evidence CDS draft",
            "GENOME_SOFT + long-read BAM/fastq (± proteins)",
            "IsoQuant → SQANTI3 (± EviAnn); BRAKER orphans optional.",
            "Build evidence backbone; filter with SQANTI; attach orphans carefully.",
            "DRAFT_GFF (evidence-first)",
            "docs/SCENARIOS.md S3",
        )
    elif primary == "S13":
        add(
            "S13",
            "GPU ab initio draft (compare lane)",
            "GENOME_SOFT (GPU)",
            "Helixer / Tiberius / ANNEVO (± SegmentNT watchlist).",
            "Ab initio models for comparison — not a silent replace when RNA exists.",
            "DRAFT_GFF (AI)",
            "docs/ROADMAP.md S13",
        )
    elif primary == "S14":
        add(
            "S14",
            "EVM consensus stack",
            "GENOME_SOFT + RNA + proteins",
            "PASA → Augustus/GeneMark → EVM → polish (steps/dclab/).",
            "Classic evidence combiner path; heavy but transparent weights.",
            "DRAFT_GFF / EVM GFF",
            "docs/steps/dclab/",
        )
    elif primary == "S6":
        add(
            "S6",
            "Thin-evidence provisional draft",
            "GENOME_SOFT ± sparse proteins",
            "Homology-first / liftoff-light tools.",
            "Produce usable but provisional models; METHODS must say L0.",
            "DRAFT_GFF (provisional)",
            "docs/SCENARIOS.md S6",
        )
    else:  # S1 default
        add(
            "S1",
            "BRAKER draft + transcript compare",
            "GENOME_SOFT + PROTEIN_DB + RNA_BAM",
            "BRAKER4/3 (± GeMoMa); StringTie→TransDecoder as compare set.",
            "Train/predict with RNA+proteins; keep StringTie as compare, not silent replace.",
            "DRAFT_GFF (+ compare track)",
            "pipeline/A2_run_draft.sh · A2b_second_predictor.md",
        )

    if "S13_compare" in choice["overlays"]:
        add(
            "S13c",
            "Overlay: AI ab initio compare",
            "Same GENOME_SOFT",
            "Helixer / Tiberius / ANNEVO",
            "Run beside primary draft; reconcile conflicts in merge / priority — do not overwrite S1 quietly.",
            "Compare GFF track",
            "docs/ROADMAP.md overlays",
        )

    add(
        "A4",
        "Merge drafts (if dual track)",
        "DRAFT_GFF ± DRAFT_GFF_B / compare",
        "EVM or TSEBRA (weights in config on structure repo).",
        "Combine with logged weights; prefer evidence-supported models.",
        "MERGED_GFF",
        "pipeline/A4_merge_sets.sh",
    )
    add(
        "A5",
        "AGAT structure counts",
        "MERGED_GFF or primary GFF",
        "AGAT",
        "Gene/mRNA/CDS counts for METHODS and sanity vs related species.",
        "AGAT_OUT counts",
        "pipeline/A5_agat_stats.sh",
    )
    add(
        "A3",
        "Proteins from GFF",
        "Release-candidate GFF + genome",
        "gffread / AGAT extract",
        "One representative protein per gene (state isoform rule).",
        "PROTEINS_FA",
        "pipeline/A3_proteins_from_gff.sh",
    )
    add(
        "01",
        "Protein BUSCO + PSAURON",
        "PROTEINS_FA",
        "BUSCO (protein), PSAURON; optional OMArk (required if S5/L2).",
        "Report C/D/F/M + lineage; triage low-quality loci.",
        "BUSCO summary + PSAURON_TSV (+ OMArk if L2)",
        "pipeline/01_qc_busco_psauron.sh · A5b_omark_compleasm.sh",
    )
    add(
        "02",
        "Priority loci list",
        "PSAURON_TSV (± family boost TSV)",
        "pipeline/02_priority_loci.py (± 02b_merge_priority_r2.py)",
        "Rank worst models; expand for tandems/BUSCO fragments on L2.",
        "PRIORITY_TSV",
        "pipeline/02_priority_loci.py",
    )
    add(
        "04",
        "GSAman / manual curation",
        "Priority windows + evidence tracks",
        "GSAman (browser curation)",
        "Fix or defer each priority locus; depth scales with S5/S7.",
        "CURATED_GFF",
        "pipeline/04_gsaman_curation.md",
    )
    if a.get("multi_hap") or "S4" in choice["overlays"]:
        add(
            "05",
            "Multi-hap SynGAP polish",
            "Dual-haplotype GFFs",
            "SynGAP",
            "Transfer/polish across haplotypes.",
            "Polished GFF",
            "pipeline/05_syngap_polish.md",
        )
    add(
        "06",
        "Qualify + package release",
        "Curated GFF + proteins + qc/",
        "gffread validate; copy to release/<TAG>/; fill METHODS",
        "Tick docs/EVALUATION.md gates for target grade; freeze tag.",
        "release/<TAG>/ GFF + proteins + METHODS + qc snapshot",
        "pipeline/06_release_gff.md · docs/EVALUATION.md",
    )
    add(
        "A6",
        "Hand-off to functional annotation",
        "Released PROTEINS_FA",
        "Sibling gene-function-annotation flow tool (F1 default).",
        "Do not invent GO here; point FA at this RELEASE_TAG.",
        "FA functional_master.tsv (next repo)",
        "pipeline/A6_functional_optional.md",
    )
    return stages


def render_markdown(a: dict, choice: dict, stages: list[dict], emit_commands: bool) -> str:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# Structure flow plan — {a.get('species_label', 'run')}",
        "",
        f"Generated: {now}  ",
        f"Tool: `pipeline/flow_tool/flow.py` (plan + explain; print-first execution).",
        "",
        "## Chooser decision",
        "",
        f"- **Primary draft:** `{choice['primary']}`",
        f"- **Overlays:** {', '.join(choice['overlays']) if choice['overlays'] else '(none)'}",
        f"- **Target grade:** `{choice['grade_target']}` (see docs/EVALUATION.md)",
        f"- **Reason:** {choice['reason']}",
        "",
        "### Answers snapshot",
        "",
    ]
    for k in (
        "close_curated_ref",
        "has_rna",
        "has_proteins",
        "deep_isoseq",
        "want_gpu_abinitio_compare",
        "want_evm_pasa",
        "goal",
        "multi_hap",
        "plant_tandem_focus",
    ):
        if k in a:
            lines.append(f"- `{k}`: `{a[k]}`")
    if a.get("notes"):
        lines.append(f"- notes: {a['notes']}")
    lines += ["", "---", "", "## Narrated stages", ""]

    for i, st in enumerate(stages, 1):
        lines += [
            f"### {i}. {st['id']} — {st['title']}",
            "",
            f"**Input:** {st['inputs']}",
            "",
            f"**Software & purpose:** {st['software']}",
            "",
            f"**Process:** {st['process']}",
            "",
            f"**Output:** {st['outputs']}",
            "",
        ]
        if st.get("helper"):
            lines.append(f"**Helper / doc:** `{st['helper']}`")
            lines.append("")
        if emit_commands and st.get("helper", "").endswith(".sh"):
            lines.append("```bash")
            lines.append(f"# Print-first helper (review before running on cluster):")
            lines.append(f"bash {st['helper']}")
            lines.append("```")
            lines.append("")

    lines += [
        "---",
        "",
        "## After this plan",
        "",
        "1. Copy `config/example.env` → `config/local.env` and fill paths.",
        "2. Walk stages in order; tick `docs/EVALUATION.md` for your target grade.",
        "3. Hand proteins to `gene-function-annotation` (`pipeline/flow_tool/flow.py` there).",
        "",
        "This tool does **not** claim one-click BRAKER on your HPC yet — helpers often print commands.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Auto-choose structure branch and narrate the full flow.")
    p.add_argument("--answers", type=Path, required=True, help="YAML answers file")
    p.add_argument("-o", "--output", type=Path, help="Write Markdown plan here")
    p.add_argument("--emit-commands", action="store_true", help="Include bash helper stubs")
    args = p.parse_args(argv)

    a = load_answers(args.answers)
    choice = choose_branch(a)
    stages = stages_for(choice, a)
    md = render_markdown(a, choice, stages, args.emit_commands)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(md)
        print(f"Wrote {args.output}", file=sys.stderr)
    print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
