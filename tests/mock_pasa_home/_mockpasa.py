"""Shared helpers for the PASA mocks (tests only)."""
import os
import sys

STATE = ".mock_pasa_loaded"


def log(tool, argv):
    path = os.environ.get("MOCK_LOG")
    if path:
        with open(path, "a") as fh:
            fh.write(tool + "\t" + "\t".join(argv) + "\n")


def opt(argv, name):
    for i, a in enumerate(argv):
        if a == name and i + 1 < len(argv):
            return argv[i + 1]
    return None


def die(msg):
    sys.stderr.write(f"[mock PASA] {msg}\n")
    sys.exit(1)


def db_name(config):
    for line in open(config):
        if line.startswith(("DATABASE=", "MYSQLDB=")):
            return os.path.basename(line.split("=", 1)[1].strip())
    die(f"{config}: no DATABASE= line")
