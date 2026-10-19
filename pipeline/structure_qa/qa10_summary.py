#!/usr/bin/env python3
"""QA step 10: join all step metrics into one QC summary table.

In:  <out>/metrics/*.tsv (from qa01-qa09); thresholds in config/structure_qa.ini
Out: <out>/qc_summary.tsv with columns
     metric  value  threshold  status  basis  step  note
status: PASS / WARN for metrics with a threshold (a missing value is WARN),
        INFO for metrics reported without a threshold.
Every threshold is a rule of thumb; compare with a close relative before acting.
"""
from __future__ import annotations

import fnmatch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa_common as qc  # noqa: E402

HEADER = ["metric", "value", "threshold", "status", "basis", "step", "note"]


def parse_rule(text: str):
    parts = text.split()
    if not parts:
        raise ValueError("empty threshold")
    op = parts[0]
    if op in (">=", "<=", ">", "<", "==") and len(parts) == 2:
        return op, (float(parts[1]),)
    if op == "range" and len(parts) == 3:
        return op, (float(parts[1]), float(parts[2]))
    if op == "info" and len(parts) == 1:
        return op, ()
    raise ValueError(f"bad threshold {text!r}: use >= x, <= x, > x, < x, == x, range lo hi, info")


def rule_text(op, args) -> str:
    if op == "range":
        return f"{args[0]:g}-{args[1]:g}"
    if op == "info":
        return "-"
    return f"{op} {args[0]:g}"


def check(op, args, value: float) -> bool:
    if op == ">=":
        return value >= args[0]
    if op == "<=":
        return value <= args[0]
    if op == ">":
        return value > args[0]
    if op == "<":
        return value < args[0]
    if op == "==":
        return value == args[0]
    if op == "range":
        return args[0] <= value <= args[1]
    raise ValueError(op)


def load_rules(cfg):
    rules = []
    if cfg.has_section("thresholds"):
        for pattern, text in cfg.items("thresholds"):
            rules.append((pattern, *parse_rule(text)))
    return rules


def find_rule(rules, metric):
    for pattern, op, args in rules:
        if fnmatch.fnmatchcase(metric, pattern):
            return op, args
    return None


def evaluate(metric, value_text, rules):
    rule = find_rule(rules, metric)
    if rule is None or rule[0] == "info":
        return "-", "INFO", ""
    op, args = rule
    thr = rule_text(op, args)
    try:
        value = float(value_text)
    except ValueError:
        return thr, "WARN", "rule of thumb"
    return thr, ("PASS" if check(op, args, value) else "WARN"), "rule of thumb"


def run(out, config=None, strict=False):
    cfg = qc.load_config(config)
    rules = load_rules(cfg)
    out = Path(out)
    mfiles = sorted((out / "metrics").glob("*.tsv"))
    if not mfiles:
        sys.exit(f"[ERR] no metrics in {out / 'metrics'}; run qa01-qa09 first")
    rows = []
    for mf in mfiles:
        with open(mf, encoding="utf-8") as fh:
            next(fh)
            for line in fh:
                metric, value, note = (line.rstrip("\n").split("\t") + ["", ""])[:3]
                thr, status, basis = evaluate(metric, value, rules)
                if value == qc.NA and status == "WARN":
                    note = f"not computed: {note}" if note else "not computed"
                rows.append([metric, value, thr, status, basis, mf.stem, note])
    path = out / "qc_summary.tsv"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("# All thresholds are rules of thumb; compare with a close relative genome.\n")
        fh.write("\t".join(HEADER) + "\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")
    n_warn = sum(r[3] == "WARN" for r in rows)
    n_pass = sum(r[3] == "PASS" for r in rows)
    print(f"[OK] {path}  PASS={n_pass} WARN={n_warn} INFO={len(rows) - n_pass - n_warn}")
    return 1 if (strict and n_warn) else 0


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("--config")
    ap.add_argument("--strict", action="store_true", help="exit 1 when any metric is WARN")
    a = ap.parse_args(argv)
    sys.exit(run(a.out, a.config, a.strict))


if __name__ == "__main__":
    main()
