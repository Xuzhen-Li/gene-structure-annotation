"""A5e: complete proteins must survive; internal stops and missing terminal stops are reported separately."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import toydata  # noqa: E402

sys.path.insert(0, str(toydata.PIPE))
import protein_stop_check as psc  # noqa: E402


class ClassifyTest(unittest.TestCase):
    def test_complete_protein_is_kept(self):
        # Old bug: a protein ending in a stop was treated as "no stop" and removed.
        self.assertEqual(psc.classify("M" + "A" * 60 + "*", 50), set())

    def test_gffread_dot_stop_is_a_stop(self):
        # gffread -y without -S writes '.' for stops; still a terminal stop, not "missing".
        self.assertEqual(psc.classify("M" + "A" * 60 + ".", 50), set())

    def test_internal_stop(self):
        self.assertEqual(psc.classify("M" + "A" * 30 + "*" + "A" * 30 + "*", 50), {"internal_stop"})

    def test_missing_terminal_stop(self):
        self.assertEqual(psc.classify("M" + "A" * 60, 50), {"no_terminal_stop"})

    def test_short_excludes_stops(self):
        self.assertEqual(psc.classify("M" + "A" * 48 + "*", 50), {"short"})

    def test_translate_keeps_terminal_stop(self):
        # gffread -y drops the final stop from its protein output; the check therefore works on CDS.
        self.assertEqual(psc.translate("ATGGCCTAA"), "MA*")
        self.assertEqual(psc.translate("ATGTGAGCCTAG"), "M*A*")
        self.assertEqual(psc.translate("ATGNNNGC"), "MX")

    def test_script_checks_cds(self):
        text = (toydata.PIPE / "A5e_filter_proteins.sh").read_text()
        self.assertRegex(text, r"gffread .*-x ")
        self.assertIn("--cds", text)


@unittest.skipUnless(toydata.have("gffread"), "gffread not on PATH")
class A5eEndToEndTest(unittest.TestCase):
    def test_filter_on_toy_models(self):
        with tempfile.TemporaryDirectory() as d:
            t = Path(d)
            data = toydata.build(t)
            r = toydata.run(["bash", str(toydata.PIPE / "A5e_filter_proteins.sh"), str(data["gff"]), "20"],
                            env={"GENOME_FA": str(data["fa"])})
            self.assertEqual(r.returncode, 0, r.stderr)
            stem = t / "toy"
            internal = Path(f"{stem}.internal_stop.txt").read_text().split()
            partial = Path(f"{stem}.no_terminal_stop.txt").read_text().split()
            self.assertEqual(internal, ["g3.t1"])
            self.assertEqual(partial, ["g4.t2"])
            kept = Path(f"{stem}.checked.gff3").read_text()
            for tid in ("g1.t1", "rna-XM_0001.1", "rna-XM_0002.1", "g4.t1"):
                self.assertIn(f"ID={tid};", kept)
            self.assertNotIn("g3.t1", kept)
            self.assertNotIn("ID=g3\n", kept)          # gene with no transcript left is removed
            self.assertIn("ID=g4\n", kept)              # gene keeps its good isoform
            self.assertNotIn("g4.t2", kept)

    def test_keep_partial(self):
        with tempfile.TemporaryDirectory() as d:
            t = Path(d)
            data = toydata.build(t)
            r = toydata.run(["bash", str(toydata.PIPE / "A5e_filter_proteins.sh"), str(data["gff"]), "20"],
                            env={"GENOME_FA": str(data["fa"]), "KEEP_PARTIAL": "1"})
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("ID=g4.t2;", (t / "toy.checked.gff3").read_text())


if __name__ == "__main__":
    unittest.main()
