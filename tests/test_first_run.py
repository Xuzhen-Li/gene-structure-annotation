"""End-to-end test of scripts/first_run.sh on testdata/structure (standard library only)."""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOY = REPO / "testdata" / "structure"


class FirstRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="fr_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_first(self, path_env=None):
        env = dict(os.environ)
        env.pop("RUN", None)
        if path_env is not None:
            env["PATH"] = path_env
        return subprocess.run(["bash", str(REPO / "scripts" / "first_run.sh"), str(self.tmp / "out")],
                              capture_output=True, text=True, env=env)

    def test_first_run_matches_expected(self):
        res = self.run_first()
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("outputs match the expected listing", res.stdout)
        out = self.tmp / "out"
        for step in range(1, 9):
            self.assertIn(f"== {step} ", res.stdout)
        rel = out / "work" / "release" / "toy.v0.1"
        self.assertTrue((rel / "proteins.faa").is_file())
        self.assertIn("gff/gff3: OK", (out / "release_check.txt").read_text())

    def test_only_python_and_shell_tools_needed(self):
        bindir = self.tmp / "bin"
        bindir.mkdir()
        for tool in ("bash", "python3", "awk", "cp", "rm", "mkdir", "find", "sort", "comm",
                     "cut", "diff", "head", "grep", "env", "basename", "dirname", "tee", "cat"):
            hit = shutil.which(tool)
            if hit:
                os.symlink(hit, bindir / tool)
        res = self.run_first(str(bindir))
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_toy_is_small_and_deterministic(self):
        size = sum(p.stat().st_size for p in TOY.rglob("*") if p.is_file())
        self.assertLess(size, 5 * 1024 * 1024)
        names = ["genome.fa", "draft.gff3", "rnaseq.bam", "protein_db.faa", "te_lib.fa"]
        before = {n: hashlib.sha256((TOY / n).read_bytes()).hexdigest() for n in names}
        copy = self.tmp / "toycopy"
        subprocess.run([sys.executable, str(TOY / "make_toy.py"), "--out", str(copy)], check=True,
                       capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        after = {n: hashlib.sha256((copy / n).read_bytes()).hexdigest() for n in names}
        self.assertEqual(before, after)

    def test_envs_pinned(self):
        for f in (REPO / "envs").glob("*.yml"):
            for line in f.read_text().splitlines():
                s = line.strip()
                if s.startswith("- ") and not s.startswith("- conda-forge") and not s.startswith("- bioconda"):
                    self.assertRegex(s, r"^- [A-Za-z0-9_.-]+=\d", f"{f.name}: {s}")
        self.assertIn("teambraker/braker3:v", (REPO / "envs" / "structure.yml").read_text())


if __name__ == "__main__":
    unittest.main()
