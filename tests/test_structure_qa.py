"""Tests for pipeline/structure_qa (standard library only).

Run:  python3 -m unittest discover -s tests -v
BUSCO, OMArk and gffcompare are replaced by small fake programs on PATH when
the real tools are absent, so the tests run on any machine.
"""
from __future__ import annotations

import gzip
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
QA = REPO / "pipeline" / "structure_qa"
SIM = REPO / "examples" / "structure_qa_sim"
sys.path.insert(0, str(QA))

import qa_common as qc  # noqa: E402
import qa02_busco  # noqa: E402
import qa03_omark  # noqa: E402
import qa04_evidence_aed  # noqa: E402
import qa05_rnaseq_junctions  # noqa: E402
import qa07_internal_stops  # noqa: E402
import qa10_summary  # noqa: E402

MOCK = SIM / "mock_tool_outputs"


def read_tsv(path):
    with open(path, encoding="utf-8") as fh:
        lines = [ln.rstrip("\n").split("\t") for ln in fh if not ln.startswith("#")]
    head = lines[0]
    return [dict(zip(head, row)) for row in lines[1:]]


def metrics(out, step):
    return {r["metric"]: r for r in read_tsv(Path(out) / "metrics" / f"{step}.tsv")}


def write(path, text):
    Path(path).write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")
    return path


class TempDir(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="sqa_"))
        self._env = dict(os.environ)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._env)
        shutil.rmtree(self.tmp, ignore_errors=True)


GFF_TWO_ISOFORMS = """
##gff-version 3
c1\tt\tgene\t1\t100\t.\t+\t.\tID=geneA
c1\tt\tmRNA\t1\t100\t.\t+\t.\tID=isoform_short;Parent=geneA
c1\tt\tCDS\t1\t30\t.\t+\t0\tParent=isoform_short
c1\tt\tmRNA\t1\t100\t.\t+\t.\tID=zz_long;Parent=geneA
c1\tt\tCDS\t1\t30\t.\t+\t0\tParent=zz_long
c1\tt\tCDS\t41\t100\t.\t+\t0\tParent=zz_long
c1\tt\tgene\t200\t260\t.\t-\t.\tID=geneB.t1
c1\tt\tmRNA\t200\t260\t.\t-\t.\tID=geneB.t1.t1;Parent=geneB.t1
c1\tt\tCDS\t200\t260\t.\t-\t0\tParent=geneB.t1.t1
"""


class ModelTests(TempDir):
    def test_longest_isoform_uses_parent_not_id(self):
        gff = write(self.tmp / "a.gff3", GFF_TWO_ISOFORMS)
        reps = qc.longest_isoforms(qc.read_models(gff))
        self.assertEqual(set(reps), {"geneA", "geneB.t1"})
        self.assertEqual(reps["geneA"].id, "zz_long")  # longest CDS, despite its name
        self.assertEqual(reps["geneB.t1"].id, "geneB.t1.t1")

    def test_cds_before_mrna_line(self):
        gff = write(self.tmp / "b.gff3", """
            c1\tt\tCDS\t1\t30\t.\t+\t0\tParent=m1
            c1\tt\tmRNA\t1\t30\t.\t+\t.\tID=m1;Parent=g1
        """)
        t = qc.read_models(gff)["m1"]
        self.assertEqual(t.gene, "g1")
        self.assertEqual(t.cds_length(), 30)

    def test_gtf_reader(self):
        gtf = write(self.tmp / "e.gtf", """
            c1\tS\ttranscript\t1\t100\t.\t+\t.\tgene_id "G"; transcript_id "T";
            c1\tS\texon\t1\t30\t.\t+\t.\tgene_id "G"; transcript_id "T";
            c1\tS\texon\t61\t100\t.\t+\t.\tgene_id "G"; transcript_id "T";
        """)
        t = qc.read_models(gtf)["T"]
        self.assertEqual(t.introns(), [(31, 60)])

    def test_translate_minus_strand(self):
        genome = {"c1": qc.revcomp("ATGAAATAA")}
        t = qc.Transcript("t", "g", "c1", "-")
        t.cds = [(1, 9, 0)]
        self.assertEqual(qc.translate(t.cds_sequence(genome)), "MK*")


class StopCodonTests(TempDir):
    def test_protein_stops_dot_and_star(self):
        ps = qa07_internal_stops.protein_stops
        self.assertEqual(ps("MKV*"), (0, True))
        self.assertEqual(ps("MKV."), (0, True))   # gffread -y style
        self.assertEqual(ps("MK.V."), (1, True))
        self.assertEqual(ps("MK*V"), (1, False))
        self.assertEqual(ps("MKV"), (0, False))

    def test_sim_internal_stop(self):
        out = self.tmp / "o"
        qa07_internal_stops.run(SIM / "consensus.gff3", out, SIM / "genome.fa", SIM / "proteins.faa")
        m = metrics(out, "qa07_internal_stops")
        self.assertEqual(m["internal_stop_count"]["value"], "1")
        self.assertEqual(m["protein_fasta_internal_stop_count"]["value"], "1")
        self.assertEqual(m["protein_fasta_terminal_stop_share"]["value"], "1")
        self.assertEqual(m["missing_stop_codon_share"]["value"], "0")
        listed = read_tsv(out / "internal_stops.tsv")
        self.assertEqual({r["transcript_id"] for r in listed}, {"g05.t1"})


class AedTests(TempDir):
    def test_aed_values(self):
        pred = qc.Transcript("p", "g", "c1", "+")
        pred.exons = [(1, 100)]
        pred.cds = [(1, 100, 0)]
        ev = qc.Transcript("e", "e", "c1", "+")
        ev.exons = [(51, 150)]
        aed = qa04_evidence_aed.compute_aed({"p": pred}, [ev])
        self.assertAlmostEqual(aed["p"][0], 0.5)  # SN 0.5, SP 0.5
        ev_other_strand = qc.Transcript("e2", "e2", "c1", "-")
        ev_other_strand.exons = [(1, 100)]
        self.assertEqual(qa04_evidence_aed.compute_aed({"p": pred}, [ev_other_strand])["p"][0], 1.0)

    def test_aed_attribute_used(self):
        gff = write(self.tmp / "m.gff3", """
            c1\tm\tmRNA\t1\t30\t.\t+\t.\tID=m1;Parent=g1;_AED=0.27
            c1\tm\tCDS\t1\t30\t.\t+\t0\tParent=m1
        """)
        out = self.tmp / "o"
        qa04_evidence_aed.run(gff, out, {})
        self.assertEqual(metrics(out, "qa04_evidence_aed")["aed_median"]["value"], "0.27")

    def test_aed1_flagged_not_deleted(self):
        out = self.tmp / "o"
        qa04_evidence_aed.run(SIM / "consensus.gff3", out,
                              {"transcripts": str(SIM / "evidence_transcripts.gtf")})
        flagged = read_tsv(out / "aed1_flagged.tsv")
        self.assertEqual([r["transcript_id"] for r in flagged], ["g06.t1"])
        self.assertIn("do not delete", flagged[0]["note"])
        self.assertIn("g06.t1", (SIM / "consensus.gff3").read_text())


def tiny_bam(path, refs, reads):
    """reads: (ref_index, pos0, flag, [(op, len)]). Plain gzip is enough for the reader."""
    text = "".join(f"@SQ\tSN:{n}\tLN:{ln}\n" for n, ln in refs).encode()
    data = b"BAM\x01" + struct.pack("<i", len(text)) + text + struct.pack("<i", len(refs))
    for n, ln in refs:
        data += struct.pack("<i", len(n) + 1) + n.encode() + b"\x00" + struct.pack("<i", ln)
    codes = {"M": 0, "N": 3, "S": 4}
    for i, (ref, pos, flag, cig) in enumerate(reads):
        name = f"r{i}".encode() + b"\x00"
        c = b"".join(struct.pack("<I", ln << 4 | codes[op]) for op, ln in cig)
        body = struct.pack("<iiBBHHHiiii", ref, pos, len(name), 60, 0, len(cig), flag, 0, -1, -1, 0)
        body += name + c
        data += struct.pack("<i", len(body)) + body
    with gzip.open(path, "wb") as fh:
        fh.write(data)


class JunctionTests(TempDir):
    def test_cigar_junction_coordinates(self):
        j = list(qa05_rnaseq_junctions.junctions_from_cigar("c1", 101, [("M", 10), ("N", 50), ("M", 5)]))
        self.assertEqual(j, [("c1", 111, 160)])

    def test_python_bam_reader_skips_secondary(self):
        bam = self.tmp / "t.bam"
        tiny_bam(bam, [("c1", 1000)], [(0, 100, 0, [("M", 10), ("N", 50), ("M", 5)]),
                                       (0, 100, 0x100, [("M", 10), ("N", 70), ("M", 5)])])
        old = os.environ.get("PATH", "")
        os.environ["PATH"] = str(self.tmp)  # make sure samtools is not used
        try:
            counts = qa05_rnaseq_junctions.junctions_from_bam(bam)
        finally:
            os.environ["PATH"] = old
        self.assertEqual(dict(counts), {("c1", 111, 160): 1})

    def test_sim_bam_support(self):
        out = self.tmp / "o"
        qa05_rnaseq_junctions.run(SIM / "consensus.gff3", out, bam=SIM / "rnaseq.bam")
        m = metrics(out, "qa05_rnaseq_junctions")
        self.assertEqual(m["rnaseq_gene_junction_support_share"]["value"], "0.875")  # g06 unsupported

    def test_star_table(self):
        sj = write(self.tmp / "SJ.out.tab", "c1\t111\t160\t1\t1\t0\t3\t1\t20\n")
        counts = qa05_rnaseq_junctions.junctions_from_table(sj)
        self.assertEqual(counts[("c1", 111, 160)], 4)


class ParserTests(unittest.TestCase):
    def test_busco_parser(self):
        p = next((MOCK / "busco" / "prot_embryophyta_odb12").glob("short_summary*.txt"))
        v = qa02_busco.parse_short_summary(p)
        self.assertEqual((v["C"], v["D"], v["n"]), (94.1, 8.8, 2026))

    def test_omark_parser(self):
        v = qa03_omark.parse_sum(MOCK / "omark" / "omark_output" / "proteins.sum")
        self.assertEqual((v["consistent"], v["inconsistent"], v["contaminant"], v["unknown"]),
                         (82.6, 4.7, 0.0, 12.7))
        self.assertEqual(v["missing"], 3.5)

    def test_gffcompare_parser(self):
        v = qa04_evidence_aed.parse_gffcompare_stats(MOCK / "gffcompare" / "transcripts.stats")
        self.assertEqual(v["intron"], (100.0, 94.1))
        self.assertEqual(v["intron_chain"], (100.0, 87.5))


class SummaryTests(TempDir):
    def test_rules(self):
        cfg = qc.load_config()
        rules = qa10_summary.load_rules(cfg)
        ev = qa10_summary.evaluate
        self.assertEqual(ev("single_exon_share", "0.2", rules)[1], "PASS")
        self.assertEqual(ev("single_exon_share", "0.4", rules)[1], "WARN")
        self.assertEqual(ev("busco_gap_eudicotyledons_odb12", "6.5", rules)[1], "WARN")
        self.assertEqual(ev("busco_prot_embryophyta_odb12_S", "80", rules)[1], "INFO")
        self.assertEqual(ev("splice_gt_ag_share", "0.99", rules)[1], "PASS")
        self.assertEqual(ev("aed_le_0.5_share", "NA", rules)[1], "WARN")

    def test_config_labelled_rule_of_thumb(self):
        text = qc.DEFAULT_CONFIG.read_text(encoding="utf-8")
        self.assertIn("RULE OF THUMB", text)
        self.assertIn("eudicotyledons_odb12", text)
        self.assertIn("busco --list-datasets", text)

    def test_bad_rule(self):
        with self.assertRaises(ValueError):
            qa10_summary.parse_rule("about 5")


FAKE_TOOLS = {
    "busco": r'''
import sys, pathlib, shutil
a = sys.argv[1:]
o, op, lin = a[a.index("-o") + 1], a[a.index("--out_path") + 1], a[a.index("-l") + 1]
d = pathlib.Path(op) / o
d.mkdir(parents=True, exist_ok=True)
src = pathlib.Path(r"{mock}") / "busco" / o
for f in src.glob("short_summary*.txt"):
    shutil.copy(f, d / f.name)
''',
    "omamer": r'''
import sys, pathlib
a = sys.argv[1:]
pathlib.Path(a[a.index("--out") + 1]).write_text("fake omamer\n")
''',
    "omark": r'''
import sys, pathlib, shutil
a = sys.argv[1:]
o = pathlib.Path(a[a.index("-o") + 1]); o.mkdir(parents=True, exist_ok=True)
shutil.copy(pathlib.Path(r"{mock}") / "omark" / "omark_output" / "proteins.sum", o / "fake.sum")
''',
    "gffcompare": r'''
import sys, pathlib, shutil
a = sys.argv[1:]
o = pathlib.Path(a[a.index("-o") + 1])
shutil.copy(pathlib.Path(r"{mock}") / "gffcompare" / (o.name + ".stats"), str(o) + ".stats")
''',
}


class PipelineTests(TempDir):
    def run_pipeline(self, out, extra_env=None, args=()):
        env = dict(os.environ)
        env.update(extra_env or {})
        cmd = [sys.executable, str(QA / "run_structure_qa.py"),
               "--gff", str(SIM / "consensus.gff3"), "--genome", str(SIM / "genome.fa"),
               "--proteins", str(SIM / "proteins.faa"),
               "--evidence", f"transcripts={SIM / 'evidence_transcripts.gtf'}",
               "--evidence", f"proteins={SIM / 'evidence_proteins.gff3'}",
               "--bam", str(SIM / "rnaseq.bam"), "--te", str(SIM / "te.gff3"),
               "--out", str(out), *args]
        return subprocess.run(cmd, env=env, capture_output=True, text=True)

    def key_columns(self, path):
        return [(r["metric"], r["value"], r["threshold"], r["status"]) for r in read_tsv(path)]

    def test_example_matches_expected(self):
        out = self.tmp / "o"
        res = subprocess.run(["bash", str(SIM / "run_example.sh"), str(out)],
                             capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(self.key_columns(out / "qc_summary.tsv"),
                         self.key_columns(SIM / "expected_qc_summary.tsv"))

    def test_tools_absent_gives_warn_not_crash(self):
        out = self.tmp / "o"
        bindir = self.tmp / "empty_bin"
        bindir.mkdir()
        os.symlink(sys.executable, bindir / "python3")
        res = self.run_pipeline(out, {"PATH": str(bindir), "RUN": "1"})
        self.assertEqual(res.returncode, 0, res.stderr)
        rows = {r["metric"]: r for r in read_tsv(out / "qc_summary.tsv")}
        self.assertEqual(rows["busco_prot_embryophyta_odb12_C"]["status"], "WARN")
        self.assertIn("not computed", rows["busco_prot_embryophyta_odb12_C"]["note"])
        self.assertEqual(rows["omark_consistent_pct"]["value"], "NA")
        self.assertEqual(rows["single_exon_share"]["status"], "PASS")  # local checks still run

    def test_fake_tools_on_path_with_run1(self):
        bindir = self.tmp / "bin"
        bindir.mkdir()
        for name, code in FAKE_TOOLS.items():
            p = bindir / name
            p.write_text(f"#!{sys.executable}\n" + code.replace("{mock}", str(MOCK)))
            p.chmod(0o755)
        db = write(self.tmp / "LUCA.h5", "fake\n")
        cfg_text = qc.DEFAULT_CONFIG.read_text(encoding="utf-8").replace(
            "omamer_db =", f"omamer_db = {db}")
        cfg = write(self.tmp / "qa.ini", cfg_text)
        out = self.tmp / "o"
        env = {"PATH": f"{bindir}{os.pathsep}{os.environ.get('PATH', '')}", "RUN": "1"}
        res = self.run_pipeline(out, env, ("--config", str(cfg)))
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("[CMD] busco", res.stdout)
        rows = {r["metric"]: r for r in read_tsv(out / "qc_summary.tsv")}
        self.assertEqual(rows["busco_gap_eudicotyledons_odb12"]["value"], "6.5")
        self.assertEqual(rows["omark_contaminant_pct"]["status"], "PASS")
        self.assertEqual(rows["gffcompare_proteins_intron_precision"]["value"], "94.1")

    def test_dry_run_does_not_call_tools(self):
        bindir = self.tmp / "bin"
        bindir.mkdir()
        marker = self.tmp / "called"
        p = bindir / "busco"
        p.write_text(f"#!/bin/sh\ntouch {marker}\n")
        p.chmod(0o755)
        out = self.tmp / "o"
        env = {"PATH": f"{bindir}{os.pathsep}{os.environ.get('PATH', '')}", "RUN": "0"}
        res = self.run_pipeline(out, env)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("[DRY]", res.stdout)
        self.assertFalse(marker.exists())

    def test_strict_exit_code(self):
        out = self.tmp / "o"
        shutil.copytree(MOCK, out)
        res = self.run_pipeline(out, args=("--strict",))
        self.assertEqual(res.returncode, 1)

    def test_placeholder_path_rejected(self):
        res = subprocess.run([sys.executable, str(QA / "run_structure_qa.py"), "--gff",
                              "/path/to/merged.gff3", "--genome", str(SIM / "genome.fa"),
                              "--out", str(self.tmp / "o")], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("placeholder", res.stderr)


class ReviewFixTests(TempDir):
    """Fixes from the PR #2 QA review."""

    def test_no_evidence_no_attribute_gives_na(self):
        gff = write(self.tmp / "evm.gff3", """
            c1\tEVM\tgene\t1\t30\t.\t+\t.\tID=g1
            c1\tEVM\tmRNA\t1\t30\t.\t+\t.\tID=m1;Parent=g1
            c1\tEVM\tCDS\t1\t30\t.\t+\t0\tParent=m1
        """)
        out = self.tmp / "o"
        qa04_evidence_aed.run(gff, out, {})
        m = metrics(out, "qa04_evidence_aed")
        self.assertEqual(m["aed_le_0.5_share"]["value"], "NA")
        self.assertEqual(m["aed_eq_1_share"]["value"], "NA")
        self.assertIn("no evidence given", m["aed_eq_1_share"]["note"])
        self.assertEqual(read_tsv(out / "aed1_flagged.tsv"), [])

    def test_unstranded_evidence_matches_either_strand(self):
        pred = qc.Transcript("p", "g", "c1", "-")
        pred.exons = [(1, 100)]
        pred.cds = [(1, 100, 0)]
        ev = qc.Transcript("e", "e", "c1", ".")
        ev.exons = [(1, 100)]
        self.assertEqual(qa04_evidence_aed.compute_aed({"p": pred}, [ev])["p"][0], 0.0)

    def test_sim_unstranded_gtf_same_result(self):
        gtf = self.tmp / "ev_dot.gtf"
        rows = []
        for line in (SIM / "evidence_transcripts.gtf").read_text().splitlines():
            c = line.split("\t")
            c[6] = "."
            rows.append("\t".join(c))
        gtf.write_text("\n".join(rows) + "\n")
        out = self.tmp / "o"
        qa04_evidence_aed.run(SIM / "consensus.gff3", out, {"transcripts": str(gtf)})
        m = metrics(out, "qa04_evidence_aed")
        self.assertEqual(m["aed_le_0.5_share"]["value"], "0.9091")
        self.assertEqual(m["aed_eq_1_count"]["value"], "1")

    def test_corrupt_bam_warns_not_traceback(self):
        bad = self.tmp / "bad.bam"
        bad.write_bytes(b"this is not a bam file")
        out = self.tmp / "o"
        old = os.environ.get("PATH", "")
        os.environ["PATH"] = str(self.tmp)  # built-in reader
        try:
            qa05_rnaseq_junctions.run(SIM / "consensus.gff3", out, bam=bad)
        finally:
            os.environ["PATH"] = old
        m = metrics(out, "qa05_rnaseq_junctions")
        self.assertEqual(m["rnaseq_gene_junction_support_share"]["value"], "NA")
        self.assertIn("cannot read", m["rnaseq_gene_junction_support_share"]["note"])

    def test_missing_tool_prints_warning(self):
        bindir = self.tmp / "empty_bin"
        bindir.mkdir()
        os.symlink(sys.executable, bindir / "python3")
        res = PipelineTests.run_pipeline(self, self.tmp / "o", {"PATH": str(bindir)})
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("[WARN] busco not on PATH", res.stderr)
        self.assertIn("[WARN] omamer/omark not on PATH", res.stderr)
        self.assertIn("[WARN] gffcompare not on PATH", res.stderr)

    def _fake_busco(self, code):
        bindir = self.tmp / f"bin{code}"
        bindir.mkdir()
        p = bindir / "busco"
        p.write_text(f"#!/bin/sh\nexit {code}\n")
        p.chmod(0o755)
        return bindir

    def test_run0_and_failed_notes_differ(self):
        notes = {}
        for run, code in (("0", 0), ("1", 3)):
            bindir = self._fake_busco(code)
            out = self.tmp / f"o{run}"
            env = {"PATH": f"{bindir}{os.pathsep}{os.environ.get('PATH', '')}", "RUN": run}
            res = PipelineTests.run_pipeline(self, out, env)
            self.assertEqual(res.returncode, 0, res.stderr)
            rows = {r["metric"]: r for r in read_tsv(out / "qc_summary.tsv")}
            notes[run] = rows["busco_prot_embryophyta_odb12_C"]["note"]
        self.assertIn("RUN=1 not set", notes["0"])
        self.assertIn("failed (exit 3)", notes["1"])

    def test_expected_summary_has_no_absolute_paths(self):
        text = (SIM / "expected_qc_summary.tsv").read_text()
        self.assertNotIn("/tmp/", text)
        self.assertNotIn(str(REPO), text)

    def test_longest_isoform_tie_and_protein_rule(self):
        gff = write(self.tmp / "t.gff3", """
            c1\tt\tmRNA\t1\t9\t.\t+\t.\tID=b;Parent=G
            c1\tt\tCDS\t1\t9\t.\t+\t0\tParent=b
            c1\tt\tmRNA\t1\t9\t.\t+\t.\tID=a;Parent=G
            c1\tt\tCDS\t1\t9\t.\t+\t0\tParent=a
        """)
        prot = write(self.tmp / "p.faa", ">b\nMKV.\n>a\nMKV*\n")
        import qa01_longest_isoform as q1
        reps, _ = q1.pick_longest(qc.read_models(gff), qc.read_fasta(prot), None)
        self.assertEqual(reps["G"].id, "a")  # same length after stop removal -> first ID

    def test_longest_isoform_prefers_clean_orf(self):
        gff = write(self.tmp / "t2.gff3", """
            c1\tt\tmRNA\t1\t30\t.\t+\t.\tID=long_bad;Parent=G
            c1\tt\tCDS\t1\t30\t.\t+\t0\tParent=long_bad
            c1\tt\tmRNA\t1\t12\t.\t+\t.\tID=short_ok;Parent=G
            c1\tt\tCDS\t1\t12\t.\t+\t0\tParent=short_ok
            c1\tt\tmRNA\t1\t30\t.\t+\t.\tID=h1;Parent=H
            c1\tt\tCDS\t1\t30\t.\t+\t0\tParent=h1
        """)
        prot = write(self.tmp / "p2.faa",
                     ">long_bad\nMKVL.AGT.\n>short_ok\nMKV.\n>h1\nMK*VLAGT*\n")
        import qa01_longest_isoform as q1
        reps, _ = q1.pick_longest(qc.read_models(gff), qc.read_fasta(prot), None)
        self.assertEqual(reps["G"].id, "short_ok")  # clean ORF beats a longer one with a stop
        self.assertEqual(reps["H"].id, "h1")        # only isoform: kept even with a stop
        self.assertTrue(q1.has_internal_stop("MK.V."))
        self.assertFalse(q1.has_internal_stop("MKV*"))

    def test_default_lineages_are_odb12(self):
        cfg = qc.load_config()
        self.assertEqual(qc.setting_list(cfg, "busco_protein_lineages"),
                         ["embryophyta_odb12", "eudicotyledons_odb12"])
        for d in (MOCK / "busco").iterdir():
            self.assertTrue(d.name.endswith("_odb12"), d.name)


class RepoHygieneTests(unittest.TestCase):
    def test_banned_word_absent(self):
        banned = "G" + "BTS"
        for base in (QA, SIM, REPO / "config", REPO / "tests"):
            for f in base.rglob("*"):
                if f.is_file() and f.suffix in {".py", ".sh", ".md", ".ini", ".tsv", ".txt", ".gff3", ".gtf"}:
                    self.assertNotIn(banned, f.read_text(encoding="utf-8", errors="ignore"), str(f))


if __name__ == "__main__":
    unittest.main()
