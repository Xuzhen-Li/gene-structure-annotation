#!/usr/bin/env python3
"""Preflight check before RUN=1 (standard library only; runs nothing).

For one pipeline step it checks that:
  - required input files / folders exist (pipeline products of LATER steps are not required),
  - no value is still a placeholder (/path/to, YOUR_*, $(...), unset $VAR),
  - output paths can be created,
  - required tools are on PATH (shutil.which), or the container image is present,
  - lineage names look valid (busco --list-datasets is the final word).
Prints [PASS] / [STOP] / [WARN] lines and a next-step hint.
Exit 0 = PASS, 1 = STOP, 2 = usage error.

Usage:
  python3 pipeline/preflight.py --list
  python3 pipeline/preflight.py --env config/local.env --step proteins
  python3 pipeline/preflight.py --step busco --step omark     # default env: config/local.env

The env file is read directly, so `source` without `set -a` cannot hide values.
print_qc_commands.py stays a command printer; this script is the check before RUN=1.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV = REPO_ROOT / "config" / "local.env"

# --------------------------------------------------------------------------
# env file
# --------------------------------------------------------------------------

_VAR_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}|\$([A-Za-z_][A-Za-z0-9_]*)")


def _strip_comment(value: str) -> str:
    out, quote = [], None
    for i, ch in enumerate(value):
        if quote:
            if ch == quote:
                quote = None
            out.append(ch)
        elif ch in "\"'":
            quote = ch
            out.append(ch)
        elif ch == "#" and (i == 0 or value[i - 1].isspace()):
            break
        else:
            out.append(ch)
    return "".join(out).strip()


def _unquote(v: str) -> tuple[str, bool]:
    """Return (value, single_quoted)."""
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1], v[0] == "'"
    return v, False


def load_env(path: Path | None, base: dict[str, str] | None = None) -> dict[str, str]:
    """Read KEY=VALUE lines like `set -a; source FILE` would, without running anything.

    ${VAR}, ${VAR:-default} and $VAR are expanded. $(...) is NOT run; it is left in the
    value so the check can report it.
    """
    env = dict(os.environ if base is None else base)
    if path is None:
        return env
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), _strip_comment(m.group(2))
        value, literal = _unquote(value)
        if not literal:
            def repl(mm: re.Match[str]) -> str:
                name = mm.group(1) or mm.group(3)
                if name in env and env[name] != "":
                    return env[name]
                if mm.group(2) is not None:
                    return mm.group(2)
                return mm.group(0)
            value = _VAR_RE.sub(repl, value)
        env[key] = value
    return env


def placeholder_reason(value: str) -> str | None:
    if value is None or value.strip() == "":
        return "empty"
    if "/path/to" in value or value.startswith("/path/"):
        return "still a /path/to placeholder"
    if "YOUR_" in value or "your_" in value.lower():
        return "still a YOUR_* placeholder"
    if "$(" in value or "`" in value:
        return "contains $(...); it is not evaluated here, write the real absolute path"
    if re.search(r"\$\{?[A-Za-z_]", value):
        return "contains an unset variable ($...)"
    if "\u2026" in value or value.strip() == "...":
        return "contains '...'"
    return None


# --------------------------------------------------------------------------
# step model
# --------------------------------------------------------------------------


@dataclass
class Tool:
    label: str
    any_of: list[str] = field(default_factory=list)      # names looked up on PATH
    path_keys: list[tuple[str, str]] = field(default_factory=list)  # (KEY, relative file)
    container_key: str = ""                               # KEY of a .sif image
    optional: bool = False


@dataclass
class Step:
    name: str
    script: str
    files: list[str] = field(default_factory=list)          # must exist as files
    dirs: list[str] = field(default_factory=list)           # must exist as folders
    outputs: list[str] = field(default_factory=list)        # set, not placeholder; may not exist yet
    optional_files: list[str] = field(default_factory=list)  # checked only when set
    optional_dirs: list[str] = field(default_factory=list)
    any_file: list[list[str]] = field(default_factory=list)  # at least one of these keys exists
    tools: list[Tool] = field(default_factory=list)
    extra: list = field(default_factory=list)              # callables(env, report)
    run: str = ""                                           # command to print on PASS


class Report:
    def __init__(self):
        self.lines: list[tuple[str, str]] = []

    def ok(self, msg):
        self.lines.append(("PASS", msg))

    def stop(self, msg):
        self.lines.append(("STOP", msg))

    def warn(self, msg):
        self.lines.append(("WARN", msg))

    @property
    def n_stop(self):
        return sum(k == "STOP" for k, _ in self.lines)


def _producer_hint(key: str) -> str:
    step = PRODUCED_BY.get(key)
    if not step:
        return ""
    return f" (made by step '{step}': preflight --step {step}, then RUN=1 bash pipeline/{STEPS[step].script})"


def _value(env, key, report, required=True):
    val = env.get(key, "")
    why = placeholder_reason(val)
    if why:
        if required:
            report.stop(f"{key}: {why} -> edit config/local.env")
        return None
    return val


def check_step(step: Step, env: dict[str, str]) -> Report:
    r = Report()
    for key in step.files:
        val = _value(env, key, r)
        if val is None:
            continue
        p = Path(val)
        if p.is_file():
            r.ok(f"{key} exists: {val}")
        elif p.is_dir():
            r.stop(f"{key} is a folder, expected a file: {val}")
        else:
            r.stop(f"{key} not found: {val}{_producer_hint(key)}")
    for key in step.dirs:
        val = _value(env, key, r)
        if val is None:
            continue
        if Path(val).is_dir():
            r.ok(f"{key} folder exists: {val}")
        else:
            r.stop(f"{key} folder not found: {val}")
    for key in step.optional_files + step.optional_dirs:
        val = env.get(key, "")
        if val.strip() in ("", "none"):
            r.ok(f"{key} not set (optional)")
            continue
        why = placeholder_reason(val)
        want_dir = key in step.optional_dirs
        if why:
            r.stop(f"{key}: {why} -> set a real path or leave it empty")
        elif (Path(val).is_dir() if want_dir else Path(val).is_file()):
            r.ok(f"{key} exists: {val}")
        else:
            r.stop(f"{key} is set but not found: {val}")
    for keys in step.any_file:
        found = None
        for key in keys:
            val = env.get(key, "")
            if not placeholder_reason(val) and Path(val).is_file():
                found = (key, val)
                break
        if found:
            r.ok(f"input {found[0]} exists: {found[1]}")
        else:
            hints = "".join(_producer_hint(k) for k in keys[:1])
            r.stop(f"none of {', '.join(keys)} points to an existing file{hints}")
    for key in step.outputs:
        val = _value(env, key, r)
        if val is None:
            continue
        p = Path(val)
        parent = next((q for q in [p, *p.parents] if q.exists()), None)
        if parent is None or not os.access(parent, os.W_OK):
            r.stop(f"{key}: cannot create {val} (no writable parent folder)")
        else:
            r.ok(f"{key} can be written: {val}")
    for tool in step.tools:
        _check_tool(tool, env, r)
    for fn in step.extra:
        fn(env, r)
    return r


def _check_tool(tool: Tool, env, r: Report):
    for name in tool.any_of:
        hit = shutil.which(name)
        if hit:
            r.ok(f"tool {tool.label}: {hit}")
            return
    for key, rel in tool.path_keys:
        base = env.get(key, "")
        if base and not placeholder_reason(base):
            p = Path(base) / rel
            if p.is_file() and os.access(p, os.X_OK):
                r.ok(f"tool {tool.label}: {p}")
                return
    if tool.container_key:
        sif = env.get(tool.container_key, "")
        runner = shutil.which("apptainer") or shutil.which("singularity")
        if sif and not placeholder_reason(sif) and Path(sif).is_file() and runner:
            r.ok(f"tool {tool.label}: container {sif} via {runner}")
            return
    where = " or ".join(
        [f"'{n}' on PATH" for n in tool.any_of]
        + [f"{k}/{rel}" for k, rel in tool.path_keys]
        + ([f"{tool.container_key} (.sif) + apptainer/singularity"] if tool.container_key else []))
    msg = f"tool {tool.label} not found: need {where}"
    if tool.optional:
        r.warn(msg + " (optional)")
    else:
        r.stop(msg + " -> load the module / activate the env")


# --------------------------------------------------------------------------
# lineage checks
# --------------------------------------------------------------------------

KNOWN_BAD_LINEAGES = {
    "eudicots_odb12": "no such dataset; odb12 name is eudicotyledons_odb12 (odb10: eudicots_odb10)",
}


def busco_lineage_check(key: str):
    def fn(env, r: Report):
        val = env.get(key, "")
        why = placeholder_reason(val)
        if why:
            r.stop(f"{key}: {why} -> pick a clade lineage (check: busco --list-datasets)")
        elif val in KNOWN_BAD_LINEAGES:
            r.stop(f"{key}={val}: {KNOWN_BAD_LINEAGES[val]}")
        elif val.lower().startswith("eukaryota"):
            r.stop(f"{key}={val}: too broad -> set a clade lineage (busco --list-datasets)")
        elif not re.fullmatch(r"[a-z0-9_]+_odb\d+", val):
            if Path(val).is_dir():
                r.ok(f"{key} is a local lineage folder: {val}")
            else:
                r.stop(f"{key}={val}: expected a BUSCO name like embryophyta_odb12")
        else:
            r.ok(f"{key}={val} (confirm it is listed by: busco --list-datasets)")
    return fn


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Check inputs, paths and tools for one pipeline step before RUN=1.",
        epilog="Exit 0 = PASS, 1 = STOP, 2 = usage error. Steps: " + ", ".join(STEPS),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--env", type=Path, default=None,
                    help="env file (default config/local.env when it exists)")
    ap.add_argument("--step", action="append", choices=list(STEPS), metavar="STEP",
                    help="step to check (repeatable): " + ", ".join(STEPS))
    ap.add_argument("--list", action="store_true", help="list steps and exit")
    a = ap.parse_args(argv)
    if a.list:
        for s in STEPS.values():
            print(f"{s.name:14s} pipeline/{s.script}")
        return 0
    if not a.step:
        ap.print_usage(sys.stderr)
        print("preflight: give --step (see --list)", file=sys.stderr)
        return 2
    env_path = a.env
    if env_path is None and DEFAULT_ENV.is_file():
        env_path = DEFAULT_ENV
    if env_path is not None and not env_path.is_file():
        print(f"[STOP] env file not found: {env_path} -> cp config/example.env config/local.env")
        return 1
    env = load_env(env_path)
    src = str(env_path) if env_path else "environment only (no config/local.env)"
    total_stop = 0
    for name in a.step:
        step = STEPS[name]
        print(f"== preflight step={name}  script=pipeline/{step.script}  env={src}")
        rep = check_step(step, env)
        for kind, msg in rep.lines:
            print(f"[{kind}] {msg}")
        total_stop += rep.n_stop
        if rep.n_stop:
            print(f"RESULT {name}: STOP ({rep.n_stop} to fix). Do not use RUN=1 yet.")
            print(f"  Fix the items above, then re-run: python3 pipeline/preflight.py"
                  f"{' --env ' + str(env_path) if env_path else ''} --step {name}")
        else:
            print(f"RESULT {name}: PASS. Next:")
            env_arg = str(env_path) if env_path else "config/local.env"
            print(f"  set -a && source {env_arg} && set +a")
            print(f"  {step.run or 'RUN=1 bash pipeline/' + step.script}")
        print()
    return 1 if total_stop else 0


# --------------------------------------------------------------------------
# steps of this repo
# --------------------------------------------------------------------------


def _need_yes(key: str, hint: str):
    def fn(env, r: Report):
        if env.get(key, "").strip().lower() == "yes":
            r.ok(f"{key}=yes")
        else:
            r.stop(f"{key} is not 'yes' -> {hint}")
    return fn


def _draft_engine(env, r: Report):
    eng = env.get("DRAFT_ENGINE", "braker3").strip() or "braker3"
    table = {
        "braker3": Step("_", "", files=["PROTEIN_DB"], optional_files=["RNA_BAM"],
                        tools=[Tool("BRAKER", ["braker.pl"], container_key="BRAKER_SIF")]),
        "galba": Step("_", "", files=["PROTEIN_DB"],
                      tools=[Tool("GALBA", ["galba.pl"], container_key="GALBA_SIF")]),
        "gemoma": Step("_", "", files=["REF_FA", "REF_GFF"],
                       tools=[Tool("GeMoMa", ["GeMoMa", "java"])]),
        "eviann": Step("_", "", files=["ISOSEQ_BAM", "PROTEIN_DB"],
                       tools=[Tool("EviAnn", ["eviann.sh"])]),
        "liftoff": Step("_", "", files=["REF_FA", "REF_GFF"], tools=[Tool("Liftoff", ["liftoff"])]),
    }
    if eng not in table:
        r.stop(f"DRAFT_ENGINE={eng}: unknown -> use one of {', '.join(table)}")
        return
    r.ok(f"DRAFT_ENGINE={eng}")
    if eng == "liftoff":
        r.warn("A2_run_draft.sh has no liftoff branch; follow pipeline/A2c_liftoff.md instead")
    sub = check_step(table[eng], env)
    r.lines.extend(sub.lines)


def _merge_mode(env, r: Report):
    mode = env.get("MERGE_MODE", "evm").strip() or "evm"
    second = env.get("DRAFT_GFF_B", "").strip()
    if not second or second == env.get("DRAFT_GFF", ""):
        r.warn("DRAFT_GFF_B not set: single draft, A4 merge is skipped (A4skip); "
               "use MERGED_GFF = DRAFT_GFF")
        return
    table = {
        "evm": Step("_", "", tools=[Tool("EVidenceModeler", ["EVidenceModeler"],
                                         path_keys=[("EVM_TOOLS", "EvmUtils/partition_EVM_inputs.pl")])]),
        "tsebra": Step("_", "", tools=[Tool("TSEBRA", ["tsebra.py"]), Tool("gffread", ["gffread"])]),
        "mikado": Step("_", "", tools=[Tool("Mikado", ["mikado"])]),
        "evi_backbone": Step("_", ""),
    }
    if mode not in table:
        r.stop(f"MERGE_MODE={mode}: unknown -> use one of {', '.join(table)}")
        return
    r.ok(f"MERGE_MODE={mode}")
    sub = check_step(table[mode], env)
    r.lines.extend(sub.lines)
    sub = check_step(Step("_", "", files=["DRAFT_GFF_B"]), env)
    r.lines.extend(sub.lines)
    if mode == "evm":
        w = env.get("EVM_WEIGHTS", "")
        if w and not placeholder_reason(w) and Path(w).is_file():
            r.ok(f"EVM_WEIGHTS exists: {w}")
        else:
            r.stop(f"EVM_WEIGHTS not found: {w or '(empty)'} -> start from config/evm_weights_*.txt")


def _compleasm(env, r: Report):
    val = env.get("COMPLEASM_LINEAGE", "")
    if not shutil.which("compleasm"):
        return
    why = placeholder_reason(val)
    if why:
        r.stop(f"COMPLEASM_LINEAGE: {why} -> a Compleasm clade pack, e.g. eudicots | poales")
    elif "_odb" in val or val.lower().startswith("eukaryota"):
        r.stop(f"COMPLEASM_LINEAGE={val}: use a Compleasm pack name, not a BUSCO *_odb* name or eukaryota")
    else:
        r.ok(f"COMPLEASM_LINEAGE={val}")


def _qa_present(env, r: Report):
    p = REPO_ROOT / "pipeline" / "structure_qa" / "run_structure_qa.py"
    if p.is_file():
        r.ok(f"structure QA step present: {p.relative_to(REPO_ROOT)}")
    else:
        r.stop("pipeline/structure_qa/run_structure_qa.py is not in this checkout -> update main")


def _release_dir(env, r: Report):
    work, tag = env.get("WORK_DIR", ""), env.get("RELEASE_TAG", "")
    if placeholder_reason(work) or placeholder_reason(tag):
        r.stop("WORK_DIR / RELEASE_TAG not set -> edit config/local.env")
        return
    d = Path(work) / "release" / tag
    if d.is_dir():
        r.ok(f"release folder exists: {d}")
    else:
        r.stop(f"release folder not found: {d} -> see pipeline/06_release_gff.md")


STEPS: dict[str, Step] = {s.name: s for s in [
    Step("softmask", "A0_softmask.md", files=["GENOME_FA", "TRUSTED_TE_LIB"],
         outputs=["WORK_DIR", "GENOME_SOFT"],
         tools=[Tool("RepeatMasker", ["RepeatMasker"])],
         extra=[_need_yes("ASSEMBLY_OK", "accept the assembly first (pipeline/Asm1_assembly_qc.md)")],
         run="follow pipeline/A0_softmask.md (RepeatMasker -lib $TRUSTED_TE_LIB -xsmall)"),
    Step("draft", "A2_run_draft.sh", files=["GENOME_SOFT"], outputs=["WORK_DIR", "DRAFT_GFF"],
         extra=[_draft_engine]),
    Step("merge", "A4_merge_sets.sh", files=["DRAFT_GFF"], outputs=["WORK_DIR", "MERGED_GFF"],
         extra=[_merge_mode]),
    Step("proteins", "A3_proteins_from_gff.sh", files=["GENOME_FA", "DRAFT_GFF"],
         outputs=["WORK_DIR", "PROTEINS_FA"], tools=[Tool("gffread", ["gffread"])]),
    Step("agat", "A5_agat_stats.sh", any_file=[["MERGED_GFF", "DRAFT_GFF"]], outputs=["WORK_DIR"],
         tools=[Tool("AGAT", ["agat_sp_statistics.pl", "agat"], optional=True)]),
    Step("busco", "01_qc_busco_psauron.sh", files=["PROTEINS_FA"], outputs=["WORK_DIR"],
         tools=[Tool("BUSCO", ["busco"]), Tool("PSAURON", ["psauron"], optional=True)],
         extra=[busco_lineage_check("BUSCO_LINEAGE")]),
    Step("omark", "A5b_omark_compleasm.sh", files=["PROTEINS_FA", "OMAMER_DB"], outputs=["WORK_DIR"],
         tools=[Tool("OMAmer", ["omamer"]), Tool("OMArk", ["omark"]),
                Tool("Compleasm", ["compleasm"], optional=True)],
         extra=[_compleasm]),
    Step("structure_qa", "structure_qa/run_structure_qa.py", files=["GENOME_FA"],
         any_file=[["MERGED_GFF", "DRAFT_GFF"]], optional_files=["PROTEINS_FA", "RNA_BAM"],
         outputs=["WORK_DIR"],
         tools=[Tool("BUSCO", ["busco"], optional=True), Tool("OMArk", ["omark"], optional=True),
                Tool("gffcompare", ["gffcompare"], optional=True),
                Tool("samtools", ["samtools"], optional=True)],
         extra=[_qa_present],
         run='RUN=1 python3 pipeline/structure_qa/run_structure_qa.py --gff "$MERGED_GFF" '
             '--genome "$GENOME_FA" --out "$WORK_DIR/qc/structure_qa"'),
    Step("release", "check_release_pack.py", outputs=["WORK_DIR"], extra=[_release_dir],
         run='python3 pipeline/check_release_pack.py "$WORK_DIR/release/$RELEASE_TAG"'),
]}

PRODUCED_BY = {"GENOME_SOFT": "softmask", "DRAFT_GFF": "draft", "MERGED_GFF": "merge",
               "PROTEINS_FA": "proteins"}


if __name__ == "__main__":
    sys.exit(main())
