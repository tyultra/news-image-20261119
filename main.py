#!/usr/bin/env python3
"""Entry point for the 19 November news-image entry (Python 3.13, stdlib only).

The front page was built by the agent in this repository (build/frontpage.html,
screenshotted to entry.png). The program simply copies that image to the
output directory the grader provides, so both runs write identical bytes:
a plain file copy carries no timestamps or run-specific data, and the size
check below fails loudly instead of ever writing a truncated image.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT_DIR, "entry.png"))
if os.path.getsize(os.path.join(OUT_DIR, "entry.png")) != os.path.getsize(SRC):
    raise RuntimeError("copied entry.png has the wrong size")
print("wrote", os.path.join(OUT_DIR, "entry.png"))
