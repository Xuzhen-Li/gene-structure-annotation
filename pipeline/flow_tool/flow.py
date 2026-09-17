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
    elif a.get("has_rna") and not a.get("has_proteins"):
        # Do NOT emit walkable S1: A2 braker3 requires PROTEIN_DB.
        primary = "BLOCKED_RNA_ONLY"
        reason = (
            "RNA without proteins: refuse broken S1 (BRAKER needs PROTEIN_DB). "
            "Set has_proteins=true + PROTEIN_DB, or choose S11/S13/S6 / deep_isoseq S3."
        )
    elif a.get("want_gpu_abinitio_compare") and not a.get("has_rna"):
        primary = "S13"
        reason = "Thin evidence + GPU ab initio compare (not a silent S1 replace)."
    elif not a.get("has_rna") and not a.get("has_proteins"):
        primary = "S6"
        reason = "Thin evidence → provisional homology-first."
    else:
        primary = "S1"
        reason = "Default fallback: S1 when unsure with any RNA/proteins signal."

    if a.get("want_gpu_abinitio_compare") and primary not in ("S13", "BLOCKED_RNA_ONLY"):
        overlays.append("S13_compare")

    grade = {"provisional": "L0", "qualified": "L1", "paper_t2t": "L2", "paper": "L2", "t2t": "L2", "l2": "L2"}.get(
        goal, "L1"
    )
    if primary in ("S6", "BLOCKED_RNA_ONLY"):
        grade = "L0"
    elif primary == "S13" and not a.get("has_rna") and not a.get("has_proteins"):
        # No RNA/proteins → treat like S6 provisional
        grade = "L0"
    elif primary == "S11" and grade != "L2":
        # raw liftover stays provisional until QC unless user forces L2 path with gap-fill
        pass

    # Thin evidence: never advertise evidence-based L1
    thin = (
        not a.get("has_rna")
        and not a.get("has_proteins")
        and not a.get("close_curated_ref")
    )
    if thin and grade != "L0":
        grade = "L0"
        reason = reason.rstrip(".") + "; no RNA/proteins/close-ref → force L0/provisional (not evidence-based L1)."

    return {
        "primary": primary,
        "overlays": overlays,
        "reason": reason,
        "grade_target": grade,
        "thin_evidence": thin,
    }


def stages_for(choice: dict, a: dict) -> list[dict]:
    """Ordered narrated stages. Each: id, title, inputs, software, process, outputs, helper."""
    primary = choice["primary"]
    stages = []

    def add(sid, title, inputs, software, process, outputs, helper="", note="", emit=""):
        # helper = one path only; note = extra docs; emit = optional full command for --emit-commands
        stages.append(
            {
                "id": sid,
                "title": title,
                "inputs": inputs,
                "software": software,
                "process": process,
                "outputs": outputs,
                "helper": helper,
                "note": note,
                "emit": emit,
            }
        )

    add(
        "Asm0",
        "Assembly / haplotype decision",
        "Raw HiFi / Hi-C / ONT (or an already-finished genome FASTA).",
        "Assembler stack you already trust (hifiasm, etc.) — see pipeline/Asm0_assembly.md.",
        "Build or accept GENOME_FA; write down ploidy / hap choice. If the FASTA was given to you, skip assembling — document source for G1. Finished-genome checklist: (1) source/version, (2) BUSCO lineage name for Asm1, (3) N50/ploidy note, (4) ASSEMBLY_OK gate, (5) stable headers.",
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
        "Soft-mask only (-xsmall); never hard-mask for BRAKER/GALBA. softmasked_fraction ≠ genome TE%; never use working/raw EDTA to inflate %. Trusted lib + sha256 in METHODS.",
        "GENOME_SOFT (+ lib version/sha in METHODS).",
        "pipeline/A0_softmask.md",
        "docs/TE_LIBRARY.md",
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
            "Transfer models; mark provisional until gap-fill+QC. Full S11 may reach L1; lift-only stop is S11-lite (L0).",
            "Lifted DRAFT_GFF (provisional).",
            "pipeline/A2c_liftoff.md",
            "No one-liner bash yet — follow the md (Liftoff/LiftOn). Do not hunt for a missing bash block.",
        )
        if choice.get("grade_target") in ("L1", "L2"):
            add(
                "S11gap",
                "S11 gap-fill (required for L1+)",
                "Lifted DRAFT_GFF + GENOME_SOFT + evidence (RNA and/or proteins)",
                "S1/S2 tools on unmapped/broken loci (BRAKER/GALBA/GeMoMa orphans) then optional merge",
                "Fill holes after lift; do not claim grade=L1 on lift-only. Stopping here without this stage = S11-lite (L0 provisional).",
                "Gap-filled DRAFT_GFF (candidate for trunk QC)",
                "pipeline/A2e_s11_gapfill.md",
                "Lift-only delivery must rename primary to S11-lite and keep grade=L0.",
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
    elif primary == "BLOCKED_RNA_ONLY":
        add(
            "WARN",
            "RNA-only — do not run protein-requiring S1",
            "RNA_BAM present; PROTEIN_DB / has_proteins missing",
            "N/A (chooser block)",
            "A2_run_draft.sh braker3 requires PROTEIN_DB. Fix answers (has_proteins + PROTEIN_DB), switch to S2/S11/S13/S6, or deep_isoseq→S3. METHODS: do not claim qualified S1.",
            "No DRAFT_GFF from this plan until evidence is fixed.",
            "pipeline/A1_choose_engine.md",
            "Honest L0: RNA-only without proteins is not a walkable BRAKER S1.",
        )
    else:  # S1 default
        add(
            "S1",
            "BRAKER draft + transcript compare",
            "GENOME_SOFT + PROTEIN_DB + RNA_BAM",
            "BRAKER4/3 (± GeMoMa); StringTie→TransDecoder as compare set.",
            "Train/predict with RNA+proteins; keep StringTie as compare, not silent replace. Note: StringTie compare ≠ a second gene set for EVM — do not force A4 for compare-only.",
            "DRAFT_GFF (+ compare track)",
            "pipeline/A2_run_draft.sh",
            "pipeline/A2b_second_predictor.md",
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

    # A4 only when dual-track merge is actually needed.
    # StringTie compare alone must NOT force A4 (not a second EVM gene set).
    eng_b = str(a.get("draft_engine_b", a.get("DRAFT_ENGINE_B", "")) or "").strip().lower()
    need_a4 = (
        primary in ("S14",)
        or bool(a.get("dual_draft_merge"))
        or bool(a.get("has_second_predictor"))
        or (eng_b not in ("", "none", "false", "0"))
        or bool(a.get("draft_gff_b") or a.get("DRAFT_GFF_B"))
    )
    if need_a4:
        add(
            "A4",
            "Merge drafts (dual track)",
            "DRAFT_GFF + DRAFT_GFF_B (or EVM evidence tracks)",
            "EVM or TSEBRA (weights in config on structure repo).",
            "Combine with logged weights; prefer evidence-supported models. Skip this stage if you only have StringTie compare beside a single BRAKER draft.",
            "MERGED_GFF",
            "pipeline/A4_merge_sets.sh",
            "StringTie compare ≠ second gene set for EVM.",
        )
    elif primary not in ("BLOCKED_RNA_ONLY",):
        add(
            "A4skip",
            "Merge skipped (single draft / compare-only)",
            "Primary DRAFT_GFF only",
            "N/A — set MERGED_GFF=$DRAFT_GFF or enable dual_draft_merge / has_second_predictor / DRAFT_ENGINE_B",
            f"Single primary draft ({primary}) does not require EVM/TSEBRA. "
            "Promote that GFF forward; run A4 only with a true second predictor / dual Liftoff set / S14 combiner. "
            "StringTie compare alone is not a second gene set.",
            "Use DRAFT_GFF as release-candidate input to AGAT/proteins",
            "",
            "pipeline/A4_merge_sets.sh (optional if dual track later)",
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
        "pipeline/01_qc_busco_psauron.sh",
        "pipeline/A5b_omark_compleasm.sh (optional / L2)",
    )
    s7 = bool(a.get("plant_tandem_focus") or "S7" in choice["overlays"])
    if not s7:
        add(
            "02",
            "Priority loci list (G7)",
            "PSAURON_TSV (± family boost TSV)",
            "pipeline/02_priority_loci.py (± 02b_merge_priority_r2.py)",
            "Rank worst models; expand for tandems/BUSCO fragments on L2.",
            "PRIORITY_TSV",
            "pipeline/02_priority_loci.py",
            "docs/EVALUATION.md G7 · docs/EVALUATION_CHECKLIST.md · docs/SCENARIOS.md",
            'python3 pipeline/02_priority_loci.py -i "$PSAURON_TSV" -o "$PRIORITY_TSV"',
        )
    if s7:
        add(
            "S7a",
            "S7 / G9 — build families.tsv",
            "Curated gene_id lists (OrthoGroups / QTL / known NLR windows). First pass: lab tables — NOT FA yet.",
            "Lab tables → families.tsv (gene_id\tfamily_or_window)",
            "FIRST PASS: build families.tsv from curated/known NLR·QTL gene_ids (or empty table + METHODS defer G9). "
            "Do NOT wait for FA — plant_sim 01 runs structure S7 before function. "
            "LATER LOOP: after FA F8, convert nlr_candidates.tsv via F8b_nlr_to_families.py and re-rank. "
            "Replaces generic stage-02 without --families.",
            "curate/families.tsv",
            "docs/SCENARIOS.md S7",
            "docs/EVALUATION.md G9",
        )
        add(
            "S7b",
            "S7 / G9 — re-rank priority with --families (G7)",
            "PSAURON_TSV + curate/families.tsv",
            "pipeline/02_priority_loci.py --families",
            "Build PRIORITY_TSV with family boosts; this is the G7 command for S7 runs.",
            "PRIORITY_TSV with family:… reasons",
            "pipeline/02_priority_loci.py",
            "docs/SCENARIOS.md S7",
            'python3 pipeline/02_priority_loci.py -i "$PSAURON_TSV" -o "$PRIORITY_TSV" --threshold 90 --families curate/families.tsv',
        )
        add(
            "S7c",
            "S7 / G9 — window curation (±100 kb tandems)",
            "Priority windows + evidence tracks",
            "GSAman on family/QTL windows only (rest may stay draft)",
            "Curate NLR/stilbene/QTL tandems; no unreviewed collapse, or list open items in METHODS (G9).",
            "CURATED_GFF (± curated_windows track / curated=yes attrs)",
            "pipeline/04_gsaman_curation.md",
            "docs/SCENARIOS.md S7 · G9",
        )
    if not (a.get("plant_tandem_focus") or "S7" in choice["overlays"]):
        add(
            "04",
            "GSAman / manual curation",
            "Priority windows + evidence tracks",
            "GSAman (browser curation)",
            "Fix or defer each priority locus (no S7 overlay on this plan — genome-wide or PSAURON-priority only).",
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
        "pipeline/06_release_gff.md",
        "docs/EVALUATION.md",
    )
    add(
        "A6",
        "Hand-off to function (FA never a product here)",
        "Released PROTEINS_FA",
        "Sibling gene-function-annotation flow tool (F1 default).",
        "Do not invent GO/KEGG/names here; point FA at this RELEASE_TAG only.",
        "FA functional_master.tsv (next repo — not this one)",
        "pipeline/A6_handoff_to_function.md",
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
        f"- **Overlays:** {', '.join(choice['overlays']) if choice['overlays'] else '(none)'}"
        + (" — S7 = plant tandem/disease windows (G9); not a second primary draft"
           if "S7" in choice.get("overlays", []) else ""),
        f"- **Target grade:** `{choice['grade_target']}` (see docs/EVALUATION.md)",
        f"- **Reason:** {choice['reason']}",
    ]
    if choice.get("thin_evidence"):
        lines += [
            "",
            "> **WARN:** answers have no RNA, no proteins, and no close curated ref — "
            "do **not** treat Target as evidence-based L1. Plan grade is **L0 / provisional** "
            "(see docs/EVALUATION.md).",
        ]
    lines += [
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
        h = (st.get("helper") or "").strip()
        note = (st.get("note") or "").strip()
        if h:
            lines.append(f"**Helper:** `{h}`")
            lines.append("")
        if note:
            lines.append(f"**Also see:** {note}")
            lines.append("")
        emit_cmd = (st.get("emit") or "").strip()
        if emit_commands and emit_cmd:
            lines.append("```bash")
            lines.append("# Print-first emit (review; may still need RUN=1 for .sh helpers):")
            lines.append(emit_cmd)
            lines.append("```")
            lines.append("")
        elif emit_commands and h.endswith(".sh"):
            hp = REPO / h
            if hp.is_file():
                body = hp.read_text(encoding="utf-8", errors="replace")
                dry = ("${RUN:-0}" in body) or ('RUN:-0' in body) or ('[[ "${RUN' in body)
                lines.append("```bash")
                if dry:
                    lines.append("# Print-first: DRY unless RUN=1 (see script header).")
                    lines.append(f"bash {h}          # dry")
                    lines.append(f"RUN=1 bash {h}    # execute on cluster after review")
                else:
                    lines.append("# Needs real inputs — 无 DRY/RUN 开关；假路径会直接失败。Review before paste.")
                    lines.append(f"bash {h}")
                lines.append("```")
                lines.append("")
            else:
                lines.append(f"> **emit skipped:** `{h}` not found under repo root.")
                lines.append("")

    lines += [
        "---",
        "",
        "## After this plan",
        "",
        "1. Copy `config/example.env` → `config/local.env` and fill paths.",
        "2. Walk stages in order; tick `docs/EVALUATION_CHECKLIST.md` "
        "(Chinese: `docs/zh/验收勾选表.md`; full rules: `docs/EVALUATION.md`).",
        "3. Optional QC command print: `python3 pipeline/print_qc_commands.py` "
        "(try `--env config/example.env`, or after `source config/local.env`).",
        "   Re-run with `--emit-commands` to embed stage helper stubs in this plan.",
        "   Already have GENOME_FA from someone else: treat Asm0/Asm1 as a checklist "
        "(document source + `ASSEMBLY_OK`), do not re-assemble.",
        "4. Hand proteins to `gene-function-annotation` (`pipeline/flow_tool/flow.py` there).",
        "",
        "This tool does **not** claim one-click BRAKER on your HPC yet — helpers often print commands.",
        "",
        "> 中文：读英文 plan 时看什么 → `docs/zh/读plan.md` · 术语 `docs/zh/99_术语表.md` · 起步 `docs/zh/03_怎么开始跑.md`。",
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
