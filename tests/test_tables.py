"""Check that every regenerated table is identical, cell by cell, to the table printed in the article.

Run from the repository root after `python scripts/make_all.py`:
    python tests/test_tables.py      (or: pytest tests/)
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXPECTED = json.loads((REPO / "tests" / "manuscript_tables.json").read_text(encoding="utf-8"))


def check(table_id):
    no = table_id.split()[1]
    out = next((REPO / "outputs" / "tables").glob(f"Table{no}_*.json"))
    got = json.loads(out.read_text(encoding="utf-8"))
    exp = EXPECTED[table_id]
    assert got["caption"] == exp["caption"], f"{table_id}: caption differs"
    assert got["head"] == exp["head"], f"{table_id}: header differs"
    assert len(got["rows"]) == len(exp["rows"]), f"{table_id}: row count differs"
    for i, (g, e) in enumerate(zip(got["rows"], exp["rows"])):
        assert g == e, f"{table_id}, row {i + 1}:\n  got      {g}\n  expected {e}"
    assert got["note"] == exp["note"], f"{table_id}: note differs\n  got      {got['note']}\n  expected {exp['note']}"


def test_all_tables():
    for tid in EXPECTED:
        check(tid)


if __name__ == "__main__":
    bad = 0
    for tid in EXPECTED:
        try:
            check(tid); print(f"{tid}: identical to the article")
        except AssertionError as e:
            bad += 1; print(f"{tid}: MISMATCH\n{e}")
    raise SystemExit(1 if bad else 0)
