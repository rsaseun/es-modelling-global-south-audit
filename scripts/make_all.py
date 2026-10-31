"""Regenerate every figure (Figs. 1–14) and table (Tables 1–9) of the article.

Each script runs in its own process so that plotting state never leaks between figures.
Also writes outputs/tables/Tables_1-9.xlsx (one sheet per table) and
outputs/stats/all_stats.json (summary statistics quoted in the text).

Run from the repository root:  python scripts/make_all.py
"""
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def run(script):
    t = time.time()
    r = subprocess.run([sys.executable, str(HERE / script)], cwd=REPO, capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stdout + r.stderr)
        raise SystemExit(f"FAILED: {script}")
    print(f"  {script:<40} {time.time() - t:5.1f} s")


def workbook():
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    wb = Workbook(); wb.remove(wb.active)
    for js in sorted((REPO / "outputs" / "tables").glob("Table*_*.json"), key=lambda p: int(p.stem.split("_")[0][5:])):
        t = json.loads(js.read_text(encoding="utf-8"))
        ws = wb.create_sheet(js.stem[:31])
        ws.append([f"{t['id']}. {t['caption']}"]); ws["A1"].font = Font(bold=True)
        ws.append([]); ws.append(t["head"])
        for c in ws[3]: c.font = Font(bold=True)
        for row in t["rows"]: ws.append(row)
        if t["note"]: ws.append([]); ws.append([t["note"]])
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = 16 if col[0].column > 1 else 34
            for c in col: c.alignment = Alignment(wrap_text=True, vertical="top")
    out = REPO / "outputs" / "tables" / "Tables_1-9.xlsx"
    wb.save(out); print("  workbook", out.relative_to(REPO))


def main():
    print("Figures"); [run(p.name) for p in sorted(HERE.glob("fig[0-9][0-9]_*.py"))]
    print("Tables"); [run(p.name) for p in sorted(HERE.glob("table[0-9][0-9]_*.py"))]
    workbook()
    stats = {p.stem: json.loads(p.read_text()) for p in sorted((REPO / "outputs" / "stats").glob("fig*.json"))}
    (REPO / "outputs" / "stats" / "all_stats.json").write_text(json.dumps(stats, indent=1, default=str))
    print("done: outputs/figures, outputs/tables, outputs/stats")


if __name__ == "__main__":
    main()
