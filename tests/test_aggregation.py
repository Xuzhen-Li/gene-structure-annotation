"""Tests for the multi-source aggregation steps A4a-A4e (standard library only).

Run from the repo root:  python3 -m unittest discover -s tests -v

External tools (EVidenceModeler, tsebra.py, mikado, PASA) are replaced by the mocks in
tests/mock_bin and tests/mock_pasa_home when they are not installed, or always when
GSA_FORCE_MOCKS=1. Assertions only check structure, so a real install also passes.
"""
from __future__ import annotations

import filecmp
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PIPE = REPO / "pipeline"
TOY = REPO / "examples" / "aggregation_toy"
WEIGHTS = REPO / "config" / "evm_weights_aggregate.txt"
MOCK_BIN = Path(__file__).resolve().parent / "mock_bin"
MOCK_PASA = Path(__file__).resolve().parent / "mock_pasa_home"
FORCE = os.environ.get("GSA_FORCE_MOCKS") == "1"

sys.path.insert(0, str(PIPE))
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("a4c", PIPE / "A4c_evm_inputs.py")
a4c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(a4c)

CODON = {}
_b = "TCAG"
_aa = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
for i, a in enumerate(_b):
    for j, b in enumerate(_b):
        for k, c in enumerate(_b):
            CODON[a + b + c] = _aa[16 * i + 4 * j + k]


def revcomp(s):
    return s.translate(str.maketrans("ACGT", "TGCA"))[::-1]


def read_fasta(path):
    seqs, name = {}, None
    for line in Path(path).read_text().splitlines():
        if line.startswith(">"):
            name = line[1:].split()[0]
            seqs[name] = []
        elif name:
            seqs[name].append(line.strip())
    return {k: "".join(v) for k, v in seqs.items()}


def gff_rows(path):
    return [l.split("\t") for l in Path(path).read_text().splitlines()
            if l.strip() and not l.startswith("#")]


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="gsa_a4_"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.log = self.tmp / "mock.log"
        self.bin = self.tmp / "bin"
        self.bin.mkdir()
        self.mocked = []
        for tool in ("EVidenceModeler", "tsebra.py", "mikado"):
            if FORCE or shutil.which(tool) is None:
                (self.bin / tool).symlink_to(MOCK_BIN / tool)
                self.mocked.append(tool)
        real_pasa = os.environ.get("PASA_HOME")
        self.pasa_home = real_pasa if (real_pasa and not FORCE) else str(MOCK_PASA)
        self.env = {k: v for k, v in os.environ.items()
                    if k not in ("EVM_HOME", "TSEBRA_HOME", "RUN", "AGG_DIR")}
        self.env.update({
            "PATH": f"{self.bin}{os.pathsep}{os.environ.get('PATH', '')}",
            "WORK_DIR": str(self.tmp / "work"),
            "GENOME_FA": str(TOY / "genome.fa"),
            "MOCK_LOG": str(self.log),
            "THREADS": "2",
        })

    def a4c(self, *args):
        return subprocess.run([sys.executable, str(PIPE / "A4c_evm_inputs.py"), *map(str, args)],
                              capture_output=True, text=True, cwd=self.tmp)

    def step(self, script, run=True, **env):
        e = dict(self.env, **{k: str(v) for k, v in env.items()})
        if run:
            e["RUN"] = "1"
        return subprocess.run(["bash", str(PIPE / script)], capture_output=True, text=True,
                              env=e, cwd=self.tmp)

    def ok(self, proc):
        self.assertEqual(proc.returncode, 0, f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
        return proc

    def evm_inputs(self, out, *extra):
        return self.ok(self.a4c("-o", out, "-w", WEIGHTS, "--genome", TOY / "genome.fa", *extra))

    def mock_calls(self, tool):
        if not self.log.exists():
            return []
        return [l.split("\t")[1:] for l in self.log.read_text().splitlines() if l.split("\t")[0] == tool]


class ToyData(unittest.TestCase):
    def test_committed_toy_matches_generator(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run([sys.executable, str(TOY / "make_toy.py"), d], check=True)
            for p in Path(d).rglob("*"):
                if p.is_file():
                    rel = p.relative_to(d)
                    self.assertTrue(filecmp.cmp(p, TOY / rel, shallow=False), f"{rel} differs; re-run make_toy.py")

    def test_toy_is_small(self):
        total = sum(p.stat().st_size for p in TOY.rglob("*") if p.is_file())
        self.assertLess(total, 100_000)

    def test_braker_models_are_complete_orfs(self):
        genome = read_fasta(TOY / "genome.fa")["chr1"]
        models, _ = a4c.collect_models(TOY / "braker.gtf", {"CDS", "stop_codon"})
        self.assertEqual(len(models), 3)
        for tid, m in models.items():
            seq = "".join(genome[s - 1:e] for s, e in m["segs"])
            if m["strand"] == "-":
                seq = revcomp(seq)
            prot = "".join(CODON[seq[i:i + 3]] for i in range(0, len(seq), 3))
            self.assertTrue(prot.startswith("M"), tid)
            self.assertTrue(prot.endswith("*"), tid)
            self.assertNotIn("*", prot[:-1], tid)


class EvmInputs(Base):
    def test_full_conversion(self):
        out = self.tmp / "evm_inputs"
        self.evm_inputs(out, "--braker", TOY / "braker.gtf", "--gemoma", TOY / "gemoma.gff3",
                        "--stringtie", TOY / "stringtie.gtf", "--pasa", TOY / "pasa_assemblies.gff3",
                        "--miniprot", TOY / "miniprot.gff")
        gp = gff_rows(out / "gene_predictions.gff3")
        ta = gff_rows(out / "transcript_alignments.gff3")
        pa = gff_rows(out / "protein_alignments.gff3")
        self.assertEqual({r[1] for r in gp}, {"BRAKER", "GeMoMa"})
        self.assertEqual({r[1] for r in ta}, {"StringTie", "PASA"})
        self.assertEqual({r[1] for r in pa}, {"miniprot"})
        self.assertEqual({r[2] for r in gp}, {"gene", "mRNA", "exon", "CDS"})
        self.assertEqual({r[2] for r in pa}, {"nucleotide_to_protein_match"})
        for p, kind in (("gene_predictions.gff3", "gene"), ("transcript_alignments.gff3", "alignment"),
                        ("protein_alignments.gff3", "alignment")):
            self.ok(self.a4c("--validate", out / p, "--kind", kind))
        # stop codon merged into the terminal CDS: g1 ends at 2151, g2 starts at 4200
        cds = {(r[3], r[4]) for r in gp if r[1] == "BRAKER" and r[2] == "CDS"}
        self.assertIn(("1901", "2151"), cds)
        self.assertIn(("4200", "4400"), cds)
        # phases follow transcript order on both strands
        ph = {(r[3], r[4]): r[7] for r in gp if r[1] == "BRAKER" and r[2] == "CDS"}
        self.assertEqual([ph[("1101", "1300")], ph[("1501", "1700")], ph[("1901", "2151")]], ["0", "1", "2"])
        self.assertEqual([ph[("4601", "4900")], ph[("4200", "4400")]], ["0", "0"])
        # unstranded single-exon StringTie transcript dropped
        self.assertFalse(any("STRG.9" in r[8] for r in ta))
        self.assertIn("unstranded=1", (out / "summary.tsv").read_text())
        # Target coordinates run 5'->3' along the transcript, also on minus strand
        g2 = [r for r in ta if "STRG.2.1" in r[8]]
        self.assertEqual([(r[3], r[8].split("Target=")[1]) for r in g2],
                         [("4601", "STRG.2.1 1 400 +"), ("4001", "STRG.2.1 401 800 +")])
        # protein Target is in amino acids, score = identity %
        self.assertTrue(all(r[5] == "95.00" for r in pa))
        self.assertIn("Target=PROT_g1 1 67", "\n".join(r[8] for r in pa))

    def test_weights_only_present_sources_no_comments(self):
        out = self.tmp / "w"
        self.evm_inputs(out, "--braker", TOY / "braker.gtf", "--miniprot", TOY / "miniprot.gff")
        rows = [l.split("\t") for l in (out / "weights.txt").read_text().splitlines()]
        self.assertEqual(rows, [["ABINITIO_PREDICTION", "BRAKER", "1"], ["PROTEIN", "miniprot", "3"]])
        self.assertFalse((out / "transcript_alignments.gff3").exists())

    def test_stale_output_removed(self):
        out = self.tmp / "stale"
        self.evm_inputs(out, "--braker", TOY / "braker.gtf", "--stringtie", TOY / "stringtie.gtf")
        self.assertTrue((out / "transcript_alignments.gff3").exists())
        self.evm_inputs(out, "--braker", TOY / "braker.gtf")
        self.assertFalse((out / "transcript_alignments.gff3").exists())

    def test_augustus_gff3_with_isoforms(self):
        gff = self.tmp / "augustus.gff3"
        gff.write_text("\n".join([
            "##gff-version 3",
            "chr1\tAUGUSTUS\tgene\t1101\t2151\t.\t+\t.\tID=g1",
            "chr1\tAUGUSTUS\tmRNA\t1101\t2151\t.\t+\t.\tID=g1.t1;Parent=g1",
            "chr1\tAUGUSTUS\tCDS\t1101\t1300\t.\t+\t0\tID=g1.t1.cds;Parent=g1.t1",
            "chr1\tAUGUSTUS\tCDS\t1501\t1700\t.\t+\t1\tID=g1.t1.cds;Parent=g1.t1",
            "chr1\tAUGUSTUS\tCDS\t1901\t2151\t.\t+\t2\tID=g1.t1.cds;Parent=g1.t1",
            "chr1\tAUGUSTUS\tmRNA\t1101\t2151\t.\t+\t.\tID=g1.t2;Parent=g1",
            "chr1\tAUGUSTUS\tCDS\t1101\t1300\t.\t+\t0\tID=g1.t2.cds;Parent=g1.t2",
            "chr1\tAUGUSTUS\tCDS\t1901\t2152\t.\t+\t1\tID=g1.t2.cds;Parent=g1.t2",
        ]) + "\n")
        out = self.tmp / "aug"
        self.evm_inputs(out, "--augustus", gff)
        gp = gff_rows(out / "gene_predictions.gff3")
        self.assertEqual(sum(r[2] == "gene" for r in gp), 1)
        self.assertEqual(sum(r[2] == "mRNA" for r in gp), 2)
        exon_ids = [r[8].split(";")[0] for r in gp if r[2] == "exon"]
        self.assertEqual(len(exon_ids), len(set(exon_ids)), "shared exons must be duplicated with unique IDs")
        self.assertEqual({r[1] for r in gp}, {"AUGUSTUS"})

    def test_braker_and_tsebra_are_exclusive(self):
        p = self.a4c("-o", self.tmp / "x", "-w", WEIGHTS, "--braker", TOY / "braker.gtf",
                     "--tsebra", TOY / "braker.gtf")
        self.assertEqual(p.returncode, 1)
        self.assertIn("alternatives", p.stderr)

    def test_needs_gene_predictions(self):
        p = self.a4c("-o", self.tmp / "x", "-w", WEIGHTS, "--stringtie", TOY / "stringtie.gtf")
        self.assertEqual(p.returncode, 1)

    def test_missing_weight_fails(self):
        w = self.tmp / "w.txt"
        w.write_text("ABINITIO_PREDICTION\tBRAKER\t1\n")
        p = self.a4c("-o", self.tmp / "x", "-w", w, "--braker", TOY / "braker.gtf",
                     "--gemoma", TOY / "gemoma.gff3")
        self.assertEqual(p.returncode, 1)
        self.assertIn("GeMoMa", p.stderr)

    def test_unknown_seqid_fails(self):
        bad = self.tmp / "bad.gtf"
        bad.write_text((TOY / "braker.gtf").read_text().replace("chr1", "chrX"))
        p = self.a4c("-o", self.tmp / "x", "-w", WEIGHTS, "--genome", TOY / "genome.fa", "--braker", bad)
        self.assertEqual(p.returncode, 1)
        self.assertIn("chrX", p.stderr)

    def test_validators_catch_errors(self):
        gene = [
            "c\ts\tgene\t1\t100\t.\t+\t.\tID=g",
            "c\ts\tmRNA\t1\t100\t.\t+\t.\tID=m;Parent=g",
            "c\ts\texon\t1\t50\t.\t+\t.\tID=e;Parent=m",
            "c\ts\texon\t60\t100\t.\t+\t.\tID=e;Parent=m",
            "c\ts\tCDS\t40\t70\t.\t+\t0\tID=c;Parent=m",
        ]
        errs = "\n".join(a4c.validate_gene_gff3(gene))
        self.assertIn("duplicate ID e", errs)
        self.assertIn("not contained", errs)
        aln = ["c\ts\tEST_match\t1\t50\t100\t+\t.\tID=a;Target=t 1 50 +",
               "c\ts\tEST_match\t40\t90\t100\t+\t.\tID=a;Target=t 51 101 +",
               "c\ts\tEST_match\t200\t250\t100\t+\t.\tID=b"]
        errs = "\n".join(a4c.validate_alignment_gff3(aln))
        self.assertIn("overlapping", errs)
        self.assertIn("Target", errs)


class WeightsFile(unittest.TestCase):
    def test_template(self):
        rows = a4c.read_weights(WEIGHTS)
        w = {s: float(x) for _, s, x in rows}
        cls = {s: c for c, s, _ in rows}
        # every A4c source has exactly one row with the class A4c writes
        for opt, (c, s, _) in a4c.INPUTS.items():
            self.assertEqual(cls.get(s), c, opt)
        self.assertEqual(len(rows), len(a4c.INPUTS))
        # starting points: ab initio 1, protein 2-5, transcript 8-10, PASA 10
        for s in ("BRAKER", "TSEBRA", "AUGUSTUS"):
            self.assertEqual(w[s], 1)
        for s in ("GeMoMa", "miniprot"):
            self.assertTrue(2 <= w[s] <= 5, s)
        for s in ("StringTie", "Mikado"):
            self.assertTrue(8 <= w[s] <= 10, s)
        self.assertEqual(w["PASA"], 10)
        text = WEIGHTS.read_text()
        self.assertIn("Tune them per species", text)
        self.assertIn("doi:10.1186/gb-2008-9-1-r7", text)
        # Mikado sits on the transcript side, not with the ab initio predictors
        self.assertEqual(cls["Mikado"], "TRANSCRIPT")


class TsebraStep(Base):
    def test_skips_for_braker3(self):
        p = self.ok(self.step("A4a_tsebra_optional.sh", BRAKER_VERSION="3"))
        self.assertIn("built into BRAKER3", p.stdout)
        self.assertEqual(self.mock_calls("tsebra.py"), [])

    def test_requires_braker_version(self):
        p = self.step("A4a_tsebra_optional.sh")
        self.assertEqual(p.returncode, 1)

    def test_dry_run_prints_only(self):
        p = self.ok(self.step("A4a_tsebra_optional.sh", run=False, BRAKER_VERSION="1+2",
                              BRAKER1_DIR=TOY / "tsebra/braker1", BRAKER2_DIR=TOY / "tsebra/braker2",
                              TSEBRA_CFG=TOY / "pasa/annotCompare.config"))
        self.assertIn("[DRY]", p.stdout)
        self.assertFalse((self.tmp / "work").exists())

    def test_braker1_plus_2_then_evm_inputs(self):
        cfg = self.tmp / "default.cfg"
        cfg.write_text("P 0.1\nE 10\nC 5\nM 1\nintron_support 1.0\nstasto_support 2\n")
        self.ok(self.step("A4a_tsebra_optional.sh", BRAKER_VERSION="1+2",
                          BRAKER1_DIR=TOY / "tsebra/braker1", BRAKER2_DIR=TOY / "tsebra/braker2",
                          TSEBRA_CFG=cfg))
        out = self.tmp / "work/aggregate/tsebra/tsebra.gtf"
        self.assertTrue(out.is_file())
        if "tsebra.py" in self.mocked:
            self.assertEqual(len(self.mock_calls("tsebra.py")), 1)
        self.evm_inputs(self.tmp / "ev", "--tsebra", out)
        self.assertIn("ABINITIO_PREDICTION\tTSEBRA\t1", (self.tmp / "ev/weights.txt").read_text())


class MikadoStep(Base):
    def test_mikado_loci_go_to_transcript_side(self):
        self.ok(self.step("A4b_mikado_optional.sh", MIKADO_LIST=TOY / "mikado_list.tsv"))
        loci = self.tmp / "work/aggregate/mikado/mikado.loci.gff3"
        self.assertTrue(loci.is_file())
        if "mikado" in self.mocked:
            subs = [c[0] for c in self.mock_calls("mikado")]
            self.assertEqual(subs, ["configure", "prepare", "serialise", "pick"])
        out = self.tmp / "ev"
        self.evm_inputs(out, "--braker", TOY / "braker.gtf", "--mikado", loci)
        ta = gff_rows(out / "transcript_alignments.gff3")
        self.assertEqual({r[1] for r in ta}, {"Mikado"})
        self.assertEqual({r[2] for r in ta}, {"EST_match"})
        self.assertFalse(any(r[1] == "Mikado" for r in gff_rows(out / "gene_predictions.gff3")))
        self.assertIn("TRANSCRIPT\tMikado\t8", (out / "weights.txt").read_text())


class EvmAndPasa(Base):
    def _evm(self):
        inp = self.tmp / "work/aggregate/evm_inputs"
        self.evm_inputs(inp, "--braker", TOY / "braker.gtf", "--gemoma", TOY / "gemoma.gff3",
                        "--stringtie", TOY / "stringtie.gtf", "--pasa", TOY / "pasa_assemblies.gff3",
                        "--miniprot", TOY / "miniprot.gff")
        return self.ok(self.step("A4d_evm_run.sh"))

    def test_evm_dry_run(self):
        p = self.ok(self.step("A4d_evm_run.sh", run=False))
        self.assertIn("--gene_predictions", p.stdout)
        self.assertIn("[DRY]", p.stdout)
        self.assertEqual(self.mock_calls("EVidenceModeler"), [])

    def test_evm_missing_inputs(self):
        p = self.step("A4d_evm_run.sh")
        self.assertEqual(p.returncode, 1)
        self.assertIn("run A4c first", p.stderr)

    def test_evm_run(self):
        self._evm()
        gff = self.tmp / "work/aggregate/evm/evm.EVM.gff3"
        self.assertTrue(gff.is_file())
        self.assertEqual(a4c.validate_gene_gff3(gff.read_text().splitlines()), [])
        self.assertEqual(sum(r[2] == "gene" for r in gff_rows(gff)), 3)
        self.assertTrue((self.tmp / "work/aggregate/evm/weights.used.txt").is_file())
        if "EVidenceModeler" in self.mocked:
            call = self.mock_calls("EVidenceModeler")[0]
            for flag in ("--protein_alignments", "--transcript_alignments", "--weights", "--CPU"):
                self.assertIn(flag, call)
            self.assertTrue(all(Path(call[call.index(f) + 1]).is_absolute()
                                for f in ("--genome", "--weights", "--gene_predictions")))

    def _pasa_env(self, **extra):
        env = dict(PASA_HOME=self.pasa_home, PASA_ALIGN_CONFIG=TOY / "pasa/alignAssembly.config",
                   PASA_ANNOT_CONFIG=TOY / "pasa/annotCompare.config",
                   PASA_TRANSCRIPTS=TOY / "pasa/transcripts.fasta.clean")
        env.update(extra)
        return env

    def test_pasa_two_rounds(self):
        self._evm()
        p = self.ok(self.step("A4e_pasa_update.sh", **self._pasa_env()))
        d = self.tmp / "work/aggregate/pasa_update"
        for f in ("round1.gff3", "round2.gff3", "pasa_updated.gff3"):
            self.assertTrue((d / f).is_file(), f)
        self.assertEqual((d / "round2.gff3").read_text(), (d / "pasa_updated.gff3").read_text())
        self.assertIn("round 2", p.stdout)
        if self.pasa_home == str(MOCK_PASA):
            loads = self.mock_calls("Load_Current_Gene_Annotations.dbi")
            self.assertEqual(len(loads), 2)
            self.assertTrue(loads[0][loads[0].index("-P") + 1].endswith("evm.EVM.gff3"))
            self.assertTrue(loads[1][loads[1].index("-P") + 1].endswith("round1.gff3"))
            self.assertEqual(len(self.mock_calls("Launch_PASA_pipeline.pl")), 2)
            # mock "UTR" extension accumulates over the two rounds
            span = [(r[3], r[4]) for r in gff_rows(d / "pasa_updated.gff3") if r[2] == "gene"]
            self.assertIn(("1041", "2211"), span)

    def test_pasa_dry_and_rounds_setting(self):
        p = self.ok(self.step("A4e_pasa_update.sh", run=False, **self._pasa_env(PASA_ROUNDS="3")))
        self.assertIn("round 3", p.stdout)
        p = self.step("A4e_pasa_update.sh", **self._pasa_env(PASA_ROUNDS="0"))
        self.assertEqual(p.returncode, 1)


class Scripts(unittest.TestCase):
    def test_bash_syntax(self):
        for sh in sorted(PIPE.glob("A4*.sh")):
            subprocess.run(["bash", "-n", str(sh)], check=True)


if __name__ == "__main__":
    unittest.main()
