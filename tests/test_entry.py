#!/usr/bin/env python3
"""Tests for the news-image-20261120 entry, stdlib only.

Seams under test (public interfaces only):
  1. `python3 generate.py` writes a valid entry.png beside itself.
  2. `node main.ts` copies entry.png into MAKEFUN_OUTPUT_DIR/entry.png.

Expected values come from the competition spec, not from the code:
PNG 1024x1024, at most 1048576 bytes, byte-identical across runs.
"""
import hashlib
import os
import struct
import subprocess
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRY = os.path.join(REPO, "entry.png")
GENERATE = os.path.join(REPO, "generate.py")
MAIN_TS = os.path.join(REPO, "main.ts")


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def png_size(path):
    """Return (width, height) of a PNG by reading its IHDR chunk."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG file"
    assert head[12:16] == b"IHDR", "first chunk is not IHDR"
    width, height = struct.unpack(">II", head[16:24])
    return width, height


class TestGenerate(unittest.TestCase):
    def test_generate_writes_valid_png(self):
        """generate.py writes a whole 1024x1024 PNG of at most 1 MiB."""
        if os.path.exists(ENTRY):
            os.remove(ENTRY)
        proc = subprocess.run(
            [sys.executable, GENERATE], cwd=REPO,
            capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(os.path.exists(ENTRY), "entry.png was not written")
        size = os.path.getsize(ENTRY)
        self.assertLessEqual(size, 1048576, "entry.png over 1 MiB")
        self.assertEqual(png_size(ENTRY), (1024, 1024))

    def test_generate_is_deterministic(self):
        """Two runs of generate.py write byte-identical files."""
        first = subprocess.run(
            [sys.executable, GENERATE], cwd=REPO,
            capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        digest_a = sha256(ENTRY)
        second = subprocess.run(
            [sys.executable, GENERATE], cwd=REPO,
            capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(sha256(ENTRY), digest_a)


class TestMainTs(unittest.TestCase):
    def test_main_copies_entry_twice_identically(self):
        """main.ts writes entry.png into the output dir, same bytes twice."""
        import shutil
        import tempfile

        self.assertTrue(os.path.exists(ENTRY), "run generate.py first")
        expected = sha256(ENTRY)
        tmp = tempfile.mkdtemp()
        try:
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=tmp)
            for _ in range(2):
                proc = subprocess.run(
                    ["node", MAIN_TS], cwd=REPO, env=env,
                    capture_output=True, text=True, timeout=60,
                )
                self.assertEqual(proc.returncode, 0, proc.stderr)
                copied = os.path.join(tmp, "entry.png")
                self.assertTrue(os.path.exists(copied))
                self.assertEqual(sha256(copied), expected)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
