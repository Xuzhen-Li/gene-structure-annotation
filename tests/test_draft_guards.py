"""A2/A4 guards, BRAKER species name and --gff3, liftoff branch, MERGED_GFF not preset, lineage names."""
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import toydata  # noqa: E402

A2 = str(toydata.PIPE / "A2_run_draft.sh")
A4 = str(toydata.PIPE / "A4_merge_sets.sh")


class GuardTest(unittest.TestCase):
    def test_a2_rejects_placeholder(self):
        # Old bug: mkdir /path/to/... → "Permission denied" before any message.
        r = toydata.run(["bash", A2], env={"WORK_DIR": "/path/to/work", "GENOME_SOFT": "/path/to/g.fa",
                                           "DRAFT_GFF": "/path/to/work/draft/primary.gff3"})
        self.assertEqual(r.returncode, 1)
        self.assertIn("/path/to", r.stderr)
        self.assertNotIn("Permission denied", r.stderr)

    def test_a4_rejects_placeholder(self):
        r = toydata.run(["bash", A4], env={"WORK_DIR": "/path/to/work", "DRAFT_GFF": "/path/to/a.gff3",
                                           "DRAFT_GFF_B": "/path/to/b.gff3"})
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("Permission denied", r.stderr)

    def test_a4_rejects_placeholder_second_draft(self):
        with tempfile.TemporaryDirectory() as d:
            r = toydata.run(["bash", A4], env={"WORK_DIR": d, "DRAFT_GFF": f"{d}/a.gff3",
                                               "DRAFT_GFF_B": "/path/to/b.gff3"})
        self.assertEqual(r.returncode, 1)
        self.assertIn("DRAFT_GFF_B", r.stderr)


class BrakerTest(unittest.TestCase):
    def test_species_name_and_gff3(self):
        with tempfile.TemporaryDirectory() as d:
            r = toydata.run(["bash", A2], env={"WORK_DIR": d, "GENOME_SOFT": f"{d}/g.fa",
                                               "DRAFT_GFF": f"{d}/draft/primary.gff3", "PROTEIN_DB": f"{d}/p.faa",
                                               "RNA_BAM": f"{d}/r.bam", "GENOME_PREFIX": "Toy"})
        self.assertEqual(r.returncode, 0, r.stderr)
        # Old bug: --species=generic for every run (parallel runs share one AUGUSTUS model dir).
        self.assertNotIn("--species=generic", r.stdout)
        self.assertIn("--species=Toy_braker ", r.stdout.replace("\\\n", " "))
        self.assertNotRegex(r.stdout, r"--species=\S*\d{8}")   # stable name → reruns reuse the trained model
        self.assertIn("--gff3", r.stdout)
        self.assertIn("--keep-genes", r.stdout)


class LiftoffTest(unittest.TestCase):
    def test_liftoff_engine(self):
        # Old bug: DRAFT_ENGINE=liftoff (03_solanum_s11 env.snippet) → "unknown DRAFT_ENGINE", exit 1.
        with tempfile.TemporaryDirectory() as d:
            r = toydata.run(["bash", A2], env={"WORK_DIR": d, "DRAFT_ENGINE": "liftoff",
                                               "DRAFT_GFF": f"{d}/draft/liftoff.gff3", "GENOME_FA": f"{d}/g.fa",
                                               "REF_FA": f"{d}/ref.fa", "REF_GFF": f"{d}/ref.gff3"})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("liftoff -g", r.stdout)
        self.assertIn("A2c_liftoff.md", r.stdout)

    def test_snippet_engine_is_supported(self):
        snippet = (toydata.REPO / "examples/plant_sim/03_solanum_s11/env.snippet").read_text()
        engine = re.search(r'DRAFT_ENGINE="(\w+)"', snippet).group(1)
        self.assertIn(f"  {engine})", Path(A2).read_text())


class ConfigTest(unittest.TestCase):
    def test_merged_gff_not_preset(self):
        env = (toydata.REPO / "config/example.env").read_text()
        self.assertIsNone(re.search(r"^MERGED_GFF=", env, re.M))

    def test_no_nonexistent_busco_lineage(self):
        # BUSCO odb12 names the eudicot set eudicotyledons_odb12; eudicots_odb12 does not exist.
        hits = [str(p.relative_to(toydata.REPO)) for p in toydata.REPO.rglob("*")
                if p.is_file() and ".git" not in p.parts and "tests" not in p.parts and p.suffix in {".md", ".env", ".py", ".sh", ".yaml", ".snippet"}
                and "eudicots_odb12" in p.read_text(errors="ignore")]
        self.assertEqual(hits, [])

    def test_lineages_page_lists_datasets_command(self):
        self.assertIn("busco --list-datasets", (toydata.REPO / "docs/LINEAGES.md").read_text())


if __name__ == "__main__":
    unittest.main()
