"""Check that every regenerated figure is pixel-identical to the figure published in the article.

The reference is a SHA-256 hash of the decoded RGB pixels of each published 600-dpi PNG
(tests/figure_checksums.json). Identity requires the pinned package versions in
requirements.txt and the Liberation Sans font (see README).

Run from the repository root after `python scripts/make_all.py`:
    python tests/test_figures.py      (or: pytest tests/)
"""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
REPO = Path(__file__).resolve().parents[1]
REF = json.loads((REPO / "tests" / "figure_checksums.json").read_text())


def check(name):
    a = np.asarray(Image.open(REPO / "outputs" / "figures" / name).convert("RGB"))
    exp = REF[name]
    assert list(a.shape) == exp["shape"], f"{name}: size {a.shape} differs from {exp['shape']}"
    assert hashlib.sha256(a.tobytes()).hexdigest() == exp["sha256_pixels"], f"{name}: pixels differ from the article figure"


def test_all_figures():
    for name in REF:
        check(name)


if __name__ == "__main__":
    bad = 0
    for name, e in REF.items():
        try:
            check(name); print(f"Fig. {e['figure']:>2} {name:<36} identical to the article")
        except (AssertionError, FileNotFoundError) as err:
            bad += 1; print(f"Fig. {e['figure']:>2} {name:<36} MISMATCH: {err}")
    raise SystemExit(1 if bad else 0)
