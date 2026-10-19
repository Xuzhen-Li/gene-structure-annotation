"""A6b: unique child IDs, non-mRNA transcripts kept, unknown parents fail loudly, ID map written."""
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import toydata  # noqa: E402

A6B = str(toydata.PIPE / "A6b_rename_gff.py")


def ids(gff_text):
    out = []
    for line in gff_text.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        col9 = line.split("\t")[8]
        out += [p.split("=", 1)[1] for p in col9.split(";") if p.startswith("ID=")]
    return out


class RenameTest(unittest.TestCase):
    def test_toy_models(self):
        with tempfile.TemporaryDirectory() as d:
            t = Path(d)
            gff = toydata.build(t)["gff"]
            mapf = t / "map.tsv"
            r = toydata.run([sys.executable, A6B, "Toy", "1", "chr", str(gff), "--map", str(mapf)])
            self.assertEqual(r.returncode, 0, r.stderr)
            out = r.stdout
            # Old bug: both exons of g1 got ID=...t01:exon (duplicate IDs).
            dup = {i: n for i, n in Counter(ids(out)).items() if n > 1 and not i.endswith(".cds")}
            self.assertEqual(dup, {})
            self.assertIn("ID=Toy_chr01g000001.t01.exon1;", out)
            self.assertIn("ID=Toy_chr01g000001.t01.exon2;", out)
            # CDS segments share one ID (one multi-line CDS feature)
            self.assertEqual(out.count("ID=Toy_chr01g000001.t01.cds;"), 2)
            # Old bug: the tRNA child of gene-L2 was dropped silently.
            self.assertIn("\ttRNA\t", out)
            m = mapf.read_text()
            self.assertIn("gene-L2\tToy_chr01g000002\tgene", m)
            self.assertIn("trna-1\t", m)
            self.assertIn("rna-XM_0002.1\t", m)

    def test_minus_strand_exons_numbered_5_to_3(self):
        with tempfile.TemporaryDirectory() as d:
            gff = Path(d) / "m.gff3"
            gff.write_text("chr2\tx\tgene\t100\t500\t.\t-\t.\tID=a\n"
                           "chr2\tx\tmRNA\t100\t500\t.\t-\t.\tID=a.1;Parent=a\n"
                           "chr2\tx\texon\t100\t200\t.\t-\t.\tParent=a.1\n"
                           "chr2\tx\texon\t400\t500\t.\t-\t.\tParent=a.1\n")
            r = toydata.run([sys.executable, A6B, "T", "1", "chr", str(gff)])
            first_exon = [l for l in r.stdout.splitlines() if "\texon\t" in l][0]
            self.assertIn("\t400\t500\t", first_exon)
            self.assertIn("exon1", first_exon)

    def test_unknown_parent_fails(self):
        with tempfile.TemporaryDirectory() as d:
            gff = Path(d) / "o.gff3"
            gff.write_text("chr1\tx\tgene\t1\t90\t.\t+\t.\tID=a\n"
                           "chr1\tx\tmRNA\t1\t90\t.\t+\t.\tID=a.1;Parent=a\n"
                           "chr1\tx\texon\t1\t90\t.\t+\t.\tParent=missing.1\n")
            r = toydata.run([sys.executable, A6B, "T", "1", "chr", str(gff)])
            self.assertEqual(r.returncode, 2)
            self.assertIn("--keep-unparented", r.stderr)
            r = toydata.run([sys.executable, A6B, "T", "1", "chr", str(gff), "--keep-unparented"])
            self.assertEqual(r.returncode, 0)
            self.assertIn("Parent=missing.1", r.stdout)


if __name__ == "__main__":
    unittest.main()
