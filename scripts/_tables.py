"""Shared helpers for the table scripts.

Every table script builds its table as a list of string rows (formatted exactly
as printed in the article) and passes it to ``write_table``, which writes:

* outputs/tables/TableN_<name>.csv  (UTF-8, header + rows)
* outputs/tables/TableN_<name>.md   (caption, Markdown table, table note)
* outputs/tables/TableN_<name>.json (caption, head, rows, note; used by tests)
"""
import csv
import json
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data" / "processed"
TAB_OUT = REPO / "outputs" / "tables"
TAB_OUT.mkdir(parents=True, exist_ok=True)
N_CORPUS = 7972  # screened corpus (Table 2, stage 6)


def thousands(v):
    """Integer with a thousands separator, as printed in the article (e.g. 2,452)."""
    return f"{int(round(v)):,}"


def half_up(v, nd=1):
    """Round a stored (already 2-decimal) value half-up, as a spreadsheet would: 49.55 -> 49.6, not 49.5."""
    from decimal import Decimal, ROUND_HALF_UP
    return str(Decimal(str(v)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def pct1(v):
    """Percentage with one decimal; exact 100 is printed without decimals."""
    return "100" if round(v, 1) == 100 else f"{v:.1f}"


def write_table(no, stem, caption, head, rows, note=""):
    rows = [[str(c) for c in r] for r in rows]
    assert all(len(r) == len(head) for r in rows), "ragged table"
    base = TAB_OUT / f"Table{no}_{stem}"
    with open(base.with_suffix(".csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(head)
        w.writerows(rows)
    md = [f"**Table {no}.** {caption}", "", "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    md += ["| " + " | ".join(c.replace("|", "\\|") for c in r) + " |" for r in rows]
    if note:
        md += ["", note]
    base.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    base.with_suffix(".json").write_text(json.dumps(
        {"id": f"Table {no}", "caption": caption, "head": head, "rows": rows, "note": note},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print("written", base.with_suffix(".csv").relative_to(REPO))
    return pd.DataFrame(rows, columns=head)
