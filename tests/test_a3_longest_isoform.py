"""A3: one protein per gene by GFF Parent, and an existing MERGED_GFF wins over DRAFT_GFF."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import toydata  # noqa: E402

sys.path.insert(0, str(toydata.PIPE))
import longest_isoform as li  # noqa: E402


class LongestIsoformTest(unittest.TestCase):
    def test_ncbi_isoforms_collapse_to_parent_gene(self):
        # Old bug: rna-XM_0001.1 and rna-XM_0002.1 were stripped to two different "genes".
        with tempfile.TemporaryDirectory() as d:
            gff = toydata.build(Path(d))["gff"]
            tx_gene = li.transcript_to_gene(gff)
        prots = [("rna-XM_0001.1", "M" + "G" * 70 + "*"), ("rna-XM_0002.1", "G" * 40 + "*"),
                 ("g1.t1", "M" + "A" * 60 + "*")]
        best, unmapped = li.pick_longest(tx_gene, prots)
        self.assertEqual(sorted(best), ["g1", "gene-L2"])
        self.assertEqual(best["gene-L2"][1], "rna-XM_0001.1")
        self.assertEqual(best["gene-L2"][0], 71)        # stop not counted
        self.assertEqual(unmapped, [])

    def test_prefers_isoform_without_internal_stop(self):
        tx_gene = {"a.t1": "a", "a.t2": "a", "b.t1": "b"}
        prots = [("a.t1", "M" + "A" * 80 + "*" + "A" * 20),   # longer but internal stop (gffread -y -S)
                 ("a.t2", "M" + "A" * 60),
                 ("b.t1", "M" + "A" * 30 + "*" + "A" * 30)]   # only isoform: kept anyway
        best, _ = li.pick_longest(tx_gene, prots)
        self.assertEqual(best["a"][1], "a.t2")
        self.assertEqual(best["b"][1], "b.t1")

    def test_tie_is_stable(self):
        best, _ = li.pick_longest({"x.2": "x", "x.1": "x"}, [("x.2", "MAAA"), ("x.1", "MAAA")])
        self.assertEqual(best["x"][1], "x.1")

    def test_gtf_input(self):
        with tempfile.TemporaryDirectory() as d:
            gtf = Path(d) / "a.gtf"
            gtf.write_text('chr1\tx\ttranscript\t1\t90\t.\t+\t.\tgene_id "G1"; transcript_id "T1";\n'
                           'chr1\tx\tCDS\t1\t90\t.\t+\t0\tgene_id "G1"; transcript_id "T2";\n')
            self.assertEqual(li.transcript_to_gene(gtf), {"T1": "G1", "T2": "G1"})


class A3GffChoiceTest(unittest.TestCase):
    def _run(self, merged_exists: bool):
        with tempfile.TemporaryDirectory() as d:
            t = Path(d)
            data = toydata.build(t)
            merged = t / "merged.gff3"
            if merged_exists:
                merged.write_text(data["gff"].read_text())
            log = t / "fake.log"
            # stub gffread: log args, write one protein per transcript
            toydata.fake_tool(t / "bin", "gffread",
                              'out=""; while [[ $# -gt 0 ]]; do [[ $1 == -y ]] && out=$2; shift; done; '
                              'printf ">g1.t1\\nMAAA*\\n" > "$out"')
            r = toydata.run(["bash", str(toydata.PIPE / "A3_proteins_from_gff.sh")], env={
                "PATH": f"{t / 'bin'}:/usr/bin:/bin", "FAKE_LOG": str(log), "RUN": "1",
                "WORK_DIR": str(t), "GENOME_FA": str(data["fa"]), "DRAFT_GFF": str(data["gff"]),
                "MERGED_GFF": str(merged), "PROTEINS_FA": str(t / "p.faa")})
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            return log.read_text(), data, merged

    def test_prefers_existing_merged(self):
        log, _, merged = self._run(True)
        self.assertIn(f"gffread {merged} ", log)

    def test_falls_back_to_draft(self):
        log, data, _ = self._run(False)
        self.assertIn(f"gffread {data['gff']} ", log)


@unittest.skipUnless(toydata.have("gffread"), "gffread not on PATH")
class A3EndToEndTest(unittest.TestCase):
    def test_one_protein_per_gene(self):
        with tempfile.TemporaryDirectory() as d:
            t = Path(d)
            data = toydata.build(t)
            r = toydata.run(["bash", str(toydata.PIPE / "A3_proteins_from_gff.sh")], env={
                "RUN": "1", "WORK_DIR": str(t), "GENOME_FA": str(data["fa"]),
                "DRAFT_GFF": str(data["gff"]), "PROTEINS_FA": str(t / "p.faa")})
            self.assertEqual(r.returncode, 0, r.stderr)
            heads = [l.split()[0][1:] for l in (t / "p.faa").read_text().splitlines() if l.startswith(">")]
            self.assertEqual(heads, ["g1", "g3", "g4", "gene-L2"])


if __name__ == "__main__":
    unittest.main()
