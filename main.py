#!/usr/bin/env python3
"""Entry program: copy the repo-held entry.png to the output directory.

Stdlib only, no network, deterministic. The grader runs this read-only;
only the output directory is writable.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
