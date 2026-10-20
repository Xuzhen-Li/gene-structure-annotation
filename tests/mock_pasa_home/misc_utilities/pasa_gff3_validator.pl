#!/usr/bin/env python3
"""MOCK pasa_gff3_validator.pl (tests only): fail if the GFF3 has no gene/mRNA/CDS rows."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _mockpasa import die, log  # noqa: E402

log("pasa_gff3_validator.pl", sys.argv[1:])
if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
    die("usage: pasa_gff3_validator.pl annotations.gff3")
types = {l.split("\t")[2] for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")}
if not {"gene", "mRNA", "CDS"} <= types:
    die("no protein-coding gene/mRNA/CDS rows")
