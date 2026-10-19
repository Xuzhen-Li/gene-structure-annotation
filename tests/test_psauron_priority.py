"""PSAURON: CDS input (or -p for proteins), CSV output, 0-1 per-sequence cutoff in 02_priority_loci.py."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import toydata  # noqa: E402

PRIORITY = str(toydata.PIPE / "02_priority_loci.py")
CSV = ("description,psauron_is_protein,in-frame_score,frame_score_1\n"
       "g1.t1 gene=g1,True,0.95,0.01\n"
       "g2.t1,False,0.20,0.40\n"
       "g3.t1,True,0.55,0.02\n")


class PriorityTest(unittest.TestCase):
    def run_priority(self, text, *extra):
        with tempfile.TemporaryDirectory() as d:
            src, out = Path(d) / "ps.csv", Path(d) / "prio.tsv"
            src.write_text(text)
            r = toydata.run([sys.executable, PRIORITY, "-i", str(src), "-o", str(out), *extra])
            rows = out.read_text().splitlines()[1:] if out.exists() else []
            return r, rows

    def test_psauron_csv_low_scores_only(self):
        # Old bug: CSV split on tabs (nothing parsed) and cutoff 90 on a 0-1 scale flagged everything.
        r, rows = self.run_priority(CSV)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual([x.split("\t")[0] for x in rows], ["g2.t1"])

    def test_threshold_on_0_1_scale(self):
        _, rows = self.run_priority(CSV, "--threshold", "0.6")
        self.assertEqual([x.split("\t")[0] for x in rows], ["g2.t1", "g3.t1"])

    def test_percent_threshold_rejected(self):
        r, _ = self.run_priority(CSV, "--threshold", "90")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("0-1", r.stderr)

    def test_percent_scores_rejected(self):
        r, _ = self.run_priority("gene_id\tpsauron_score\ng1\t95\n")
        self.assertEqual(r.returncode, 2)

    def test_legacy_two_column_tsv(self):
        _, rows = self.run_priority("g1\t0.9\ng2\t0.1\n")
        self.assertEqual([x.split("\t")[0] for x in rows], ["g2"])


class QcScriptTest(unittest.TestCase):
    def _run(self, with_models: bool):
        with tempfile.TemporaryDirectory() as d:
            t = Path(d)
            data = toydata.build(t)
            log = t / "fake.log"
            bindir = t / "bin"
            toydata.fake_tool(bindir, "busco", "exit 0")
            toydata.fake_tool(bindir, "psauron", "exit 0")
            toydata.fake_tool(bindir, "gffread",
                              'out=""; while [[ $# -gt 0 ]]; do [[ $1 == -x ]] && out=$2; shift; done; : > "$out"')
            (t / "p.faa").write_text(">g1\nMAAA\n")
            env = {"PATH": f"{bindir}:/usr/bin:/bin", "FAKE_LOG": str(log), "RUN": "1", "WORK_DIR": str(t),
                   "PROTEINS_FA": str(t / "p.faa"), "BUSCO_LINEAGE": "viridiplantae_odb12"}
            if with_models:
                env.update(GENOME_FA=str(data["fa"]), DRAFT_GFF=str(data["gff"]))
            r = toydata.run(["bash", str(toydata.PIPE / "01_qc_busco_psauron.sh")], env=env)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            return [l for l in log.read_text().splitlines() if l.startswith("psauron ")][0], t

    def test_cds_input_when_models_available(self):
        line, t = self._run(True)
        self.assertIn("psauron_input.cds.fa", line)
        self.assertNotIn(" -p", line)
        self.assertIn("psauron.csv", line)

    def test_protein_mode_flag(self):
        # Old bug: proteins were scored without -p (PSAURON then reads them as nucleotide CDS).
        line, _ = self._run(False)
        self.assertTrue(line.endswith(" -p"), line)


if __name__ == "__main__":
    unittest.main()
