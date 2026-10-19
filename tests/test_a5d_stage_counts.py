"""A5d: GFF3 (key=value) and GTF (key "value") give the same gene / mono / multi counts."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import toydata  # noqa: E402

A5D = str(toydata.PIPE / "A5d_stage_counts.sh")


class StageCountsTest(unittest.TestCase):
    def _counts(self, path, tmp):
        out = Path(tmp) / "stage.tsv"
        r = toydata.run(["bash", A5D, str(path)], env={"STAGE_QC_TSV": str(out)})
        self.assertEqual(r.returncode, 0, r.stderr)
        row = out.read_text().splitlines()[1].split("\t")
        return row

    def test_gff3_counts(self):
        # Old bug: "ID=g1" was returned as the ID (the GTF branch matched first) → 7 "genes" for 4.
        with tempfile.TemporaryDirectory() as d:
            gff = toydata.build(Path(d))["gff"]
            label, genes, mono, multi, ratio = self._counts(gff, d)
        self.assertEqual(label, "toy.gff3")
        self.assertEqual((genes, mono, multi), ("4", "3", "1"))
        self.assertEqual(ratio, "3.000")

    def test_gtf_counts(self):
        with tempfile.TemporaryDirectory() as d:
            gtf = Path(d) / "a.gtf"
            gtf.write_text(
                'chr1\tx\ttranscript\t1\t900\t.\t+\t.\tgene_id "G1"; transcript_id "T1";\n'
                'chr1\tx\texon\t1\t100\t.\t+\t.\tgene_id "G1"; transcript_id "T1";\n'
                'chr1\tx\texon\t800\t900\t.\t+\t.\tgene_id "G1"; transcript_id "T1";\n'
                'chr1\tx\texon\t1000\t1100\t.\t+\t.\tgene_id "G2"; transcript_id "T2";\n')
            _, genes, mono, multi, _ = self._counts(gtf, d)
        self.assertEqual((genes, mono, multi), ("2", "1", "1"))

    def test_default_output_under_work_dir(self):
        with tempfile.TemporaryDirectory() as d:
            gff = toydata.build(Path(d))["gff"]
            r = toydata.run(["bash", A5D, str(gff)], env={"WORK_DIR": d})
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((Path(d) / "qc" / "stage_qc.tsv").is_file())


if __name__ == "__main__":
    unittest.main()
