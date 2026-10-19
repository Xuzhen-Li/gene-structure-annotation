"""Tests for pipeline/preflight.py (standard library only).

Run:  python3 -m unittest discover -s tests -v
Tools are faked with small executables in a temporary PATH folder.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PREFLIGHT = REPO / "pipeline" / "preflight.py"
sys.path.insert(0, str(REPO / "pipeline"))
import preflight  # noqa: E402


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pf_"))
        self.bin = self.tmp / "bin"
        self.bin.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def fake_tool(self, *names):
        for n in names:
            p = self.bin / n
            p.write_text("#!/bin/sh\nexit 0\n")
            p.chmod(0o755)

    def touch(self, rel, text="x\n"):
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def env_file(self, body):
        p = self.tmp / "local.env"
        p.write_text(textwrap.dedent(body).replace("@T", str(self.tmp)))
        return p

    def run_pf(self, *args):
        env = {"PATH": str(self.bin), "HOME": str(self.tmp)}
        return subprocess.run([sys.executable, str(PREFLIGHT), *args], env=env,
                              capture_output=True, text=True, cwd=self.tmp)


class EnvParsingTests(Base):
    def test_expansion_quotes_comments(self):
        p = self.env_file("""
            WORK_DIR="@T/work"   # comment
            export DRAFT_GFF="$WORK_DIR/draft/a.gff3"
            OUT="${MISSING:-@T/default}"
            LIT='$WORK_DIR/x'
            HASH="a#b"
        """)
        env = preflight.load_env(p, base={})
        self.assertEqual(env["WORK_DIR"], f"{self.tmp}/work")
        self.assertEqual(env["DRAFT_GFF"], f"{self.tmp}/work/draft/a.gff3")
        self.assertEqual(env["OUT"], f"{self.tmp}/default")
        self.assertEqual(env["LIT"], "$WORK_DIR/x")
        self.assertEqual(env["HASH"], "a#b")

    def test_placeholders(self):
        pr = preflight.placeholder_reason
        self.assertIn("/path/to", pr("/path/to/work"))
        self.assertIn("YOUR_", pr("YOUR_BUSCO_LINEAGE_odb12"))
        self.assertIn("$(...)", pr("$(pwd)/x"))
        self.assertIn("unset", pr("$NOPE/x"))
        self.assertEqual(pr(""), "empty")
        self.assertIsNone(pr("/data/genome.fa"))

    def test_env_file_read_without_export(self):
        # values only in the file (not exported in the shell) are still seen
        p = self.env_file("WORK_DIR=@T/work\n")
        res = self.run_pf("--env", str(p), "--step", next(iter(preflight.STEPS)))
        self.assertIn(f"WORK_DIR can be written: {self.tmp}/work", res.stdout)


class CliTests(Base):
    def test_list(self):
        res = self.run_pf("--list")
        self.assertEqual(res.returncode, 0)
        for name in preflight.STEPS:
            self.assertIn(name, res.stdout)

    def test_no_step_is_usage_error(self):
        self.assertEqual(self.run_pf().returncode, 2)

    def test_missing_env_file(self):
        res = self.run_pf("--env", str(self.tmp / "nope.env"), "--step", next(iter(preflight.STEPS)))
        self.assertEqual(res.returncode, 1)
        self.assertIn("env file not found", res.stdout)

    def test_example_env_stops(self):
        res = self.run_pf("--env", str(REPO / "config" / "example.env"), "--step",
                          next(iter(preflight.STEPS)))
        self.assertEqual(res.returncode, 1)
        self.assertIn("[STOP]", res.stdout)
        self.assertIn("Do not use RUN=1 yet", res.stdout)

    def test_command_substitution_stops(self):
        p = self.env_file('WORK_DIR="$(pwd)/work"\n')
        res = self.run_pf("--env", str(p), "--step", next(iter(preflight.STEPS)))
        self.assertEqual(res.returncode, 1)
        self.assertIn("not evaluated", res.stdout)


class PrintQcWordingTests(unittest.TestCase):
    def test_print_qc_points_to_preflight(self):
        text = (REPO / "pipeline" / "print_qc_commands.py").read_text(encoding="utf-8")
        self.assertIn("preflight.py", text)
        self.assertNotIn("not a RUN=1 plan", text)
        self.assertNotIn("RUN=1 yet", text)


class StructureStepTests(Base):
    def base_env(self, extra=""):
        self.touch("genome.fa", ">c1\nACGT\n")
        return self.env_file("""
            WORK_DIR="@T/work"
            GENOME_FA="@T/genome.fa"
            DRAFT_GFF="$WORK_DIR/draft/primary.gff3"
            MERGED_GFF="$WORK_DIR/draft/merged.gff3"
            PROTEINS_FA="$WORK_DIR/proteins.faa"
        """ + textwrap.dedent(extra))

    def test_nonexistent_inputs_stop(self):
        p = self.base_env()
        self.fake_tool("gffread")
        res = self.run_pf("--env", str(p), "--step", "proteins")
        self.assertEqual(res.returncode, 1)
        self.assertIn("DRAFT_GFF not found", res.stdout)
        self.assertIn("made by step 'draft'", res.stdout)

    def test_proteins_pass_and_product_not_required(self):
        p = self.base_env()
        self.touch("work/draft/primary.gff3")
        self.fake_tool("gffread")
        res = self.run_pf("--env", str(p), "--step", "proteins")
        self.assertEqual(res.returncode, 0, res.stdout)
        self.assertIn("PROTEINS_FA can be written", res.stdout)  # output need not exist
        self.assertIn("RUN=1 bash pipeline/A3_proteins_from_gff.sh", res.stdout)

    def test_missing_tool_stops(self):
        p = self.base_env()
        self.touch("work/draft/primary.gff3")
        res = self.run_pf("--env", str(p), "--step", "proteins")
        self.assertEqual(res.returncode, 1)
        self.assertIn("tool gffread not found", res.stdout)

    def test_optional_tool_only_warns(self):
        p = self.base_env()
        self.touch("work/draft/primary.gff3")
        res = self.run_pf("--env", str(p), "--step", "agat")
        self.assertEqual(res.returncode, 0, res.stdout)
        self.assertIn("[WARN] tool AGAT not found", res.stdout)

    def test_busco_lineage_names(self):
        self.touch("work/proteins.faa")
        self.fake_tool("busco")
        for lineage, code in (("eudicots_odb12", 1), ("eukaryota_odb10", 1),
                              ("YOUR_BUSCO_LINEAGE_odb12", 1), ("eudicotyledons_odb12", 0),
                              ("embryophyta_odb10", 0)):
            p = self.base_env(f'BUSCO_LINEAGE="{lineage}"\n')
            res = self.run_pf("--env", str(p), "--step", "busco")
            self.assertEqual(res.returncode, code, f"{lineage}: {res.stdout}")
        self.assertIn("busco --list-datasets", res.stdout)

    def test_draft_braker_container(self):
        self.touch("genome.soft.fa")
        self.touch("prot.faa")
        self.touch("braker.sif")
        p = self.base_env("""
            GENOME_SOFT="@T/genome.soft.fa"
            PROTEIN_DB="@T/prot.faa"
            DRAFT_ENGINE="braker3"
            RNA_BAM=""
        """)
        res = self.run_pf("--env", str(p), "--step", "draft")
        self.assertEqual(res.returncode, 1)
        self.assertIn("tool BRAKER not found", res.stdout)
        self.fake_tool("apptainer")
        with open(p, "a") as fh:
            fh.write(f'BRAKER_SIF="{self.tmp}/braker.sif"\n')
        res = self.run_pf("--env", str(p), "--step", "draft")
        self.assertEqual(res.returncode, 0, res.stdout)
        self.assertIn("container", res.stdout)

    def test_draft_rna_bam_set_but_missing(self):
        self.touch("genome.soft.fa")
        self.touch("prot.faa")
        self.fake_tool("braker.pl")
        p = self.base_env("""
            GENOME_SOFT="@T/genome.soft.fa"
            PROTEIN_DB="@T/prot.faa"
            RNA_BAM="@T/missing.bam"
        """)
        res = self.run_pf("--env", str(p), "--step", "draft")
        self.assertEqual(res.returncode, 1)
        self.assertIn("RNA_BAM is set but not found", res.stdout)

    def test_draft_liftoff_and_unknown_engine(self):
        self.touch("genome.soft.fa")
        self.touch("ref.fa")
        self.touch("ref.gff3")
        self.fake_tool("liftoff")
        p = self.base_env("""
            GENOME_SOFT="@T/genome.soft.fa"
            REF_FA="@T/ref.fa"
            REF_GFF="@T/ref.gff3"
            DRAFT_ENGINE="liftoff"
        """)
        res = self.run_pf("--env", str(p), "--step", "draft")
        self.assertEqual(res.returncode, 0, res.stdout)
        self.assertIn("A2c_liftoff.md", res.stdout)
        with open(p, "a") as fh:
            fh.write('DRAFT_ENGINE="maker9"\n')
        self.assertEqual(self.run_pf("--env", str(p), "--step", "draft").returncode, 1)

    def test_merge_single_draft_is_skip(self):
        p = self.base_env()
        self.touch("work/draft/primary.gff3")
        res = self.run_pf("--env", str(p), "--step", "merge")
        self.assertEqual(res.returncode, 0, res.stdout)
        self.assertIn("A4skip", res.stdout)

    def test_softmask_needs_assembly_ok(self):
        self.touch("te.fa")
        self.fake_tool("RepeatMasker")
        p = self.base_env('TRUSTED_TE_LIB="@T/te.fa"\nGENOME_SOFT="@T/work/soft.fa"\nASSEMBLY_OK="no"\n')
        res = self.run_pf("--env", str(p), "--step", "softmask")
        self.assertEqual(res.returncode, 1)
        self.assertIn("ASSEMBLY_OK is not 'yes'", res.stdout)

    def test_two_steps_one_stop(self):
        p = self.base_env()
        self.touch("work/draft/primary.gff3")
        res = self.run_pf("--env", str(p), "--step", "agat", "--step", "proteins")
        self.assertEqual(res.returncode, 1)
        self.assertIn("RESULT agat: PASS", res.stdout)
        self.assertIn("RESULT proteins: STOP", res.stdout)

    def test_release_folder(self):
        p = self.base_env('RELEASE_TAG="sp.v1"\n')
        self.assertEqual(self.run_pf("--env", str(p), "--step", "release").returncode, 1)
        (self.tmp / "work" / "release" / "sp.v1").mkdir(parents=True)
        res = self.run_pf("--env", str(p), "--step", "release")
        self.assertEqual(res.returncode, 0, res.stdout)
        self.assertIn("check_release_pack.py", res.stdout)


if __name__ == "__main__":
    unittest.main()
