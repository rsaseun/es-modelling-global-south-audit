"""Table 3. Decadal descriptive statistics of the screened corpus.

Input  : data/processed/year_overall.txt (annual count, mean/median citations, mean FWCI, % open access)
Output : outputs/tables/Table3_decades.{csv,md,json}
Method : decadal means are article-weighted means of the annual values; within-decade CAGR uses the
         first and last year of each decade; the 1990–2025 growth rate is the exponential (log-linear)
         fit to annual counts for 2000–2025, r = exp(b) − 1.

Run from the repository root:  python scripts/table03_decades.py
"""
import numpy as np
import pandas as pd

from _tables import DATA, N_CORPUS, thousands, write_table

CAPTION = "Decadal descriptive statistics of the screened corpus."
HEAD = ["Decade", "Articles", "Share (%)", "Mean per year", "Within-decade CAGR (%)", "Mean citations", "Mean FWCI", "Open access (%)"]
NOTE = ("ᵃ Not meaningful because of very small annual counts. ᵇ Exponential growth rate for 2000–2025 (R² = {r2:.2f}). "
        "FWCI = field-weighted citation impact; CAGR = compound annual growth rate.")
DECADES = [("1990s (1990–1999)", 1990, 1999, False), ("2000s (2000–2009)", 2000, 2009, True),
           ("2010s (2010–2019)", 2010, 2019, True), ("2020–2025", 2020, 2025, True)]


def summarise(d):
    n = d["count"].sum()
    w = lambda c: (d[c] * d["count"]).sum() / n
    return n, w("mean_cit"), w("fwci"), w("pct_oa")


def main():
    y = pd.read_csv(DATA / "year_overall.txt")
    full = y.set_index("year")["count"].reindex(range(1990, 2026), fill_value=0)
    rows = []
    for label, a, b, cagr_ok in DECADES:
        n, cit, fwci, oa = summarise(y[(y.year >= a) & (y.year <= b)])
        cagr = f"{((full[b] / full[a]) ** (1 / (b - a)) - 1) * 100:.1f}" if cagr_ok else "n.a.ᵃ"
        rows.append([label, thousands(n), f"{n / N_CORPUS * 100:.1f}", f"{n / (b - a + 1):.1f}", cagr, f"{cit:.1f}", f"{fwci:.2f}", f"{oa:.1f}"])
    fit = y[y.year >= 2000]
    b1, b0 = np.polyfit(fit.year, np.log(fit["count"]), 1)
    pred = b0 + b1 * fit.year
    r2 = 1 - ((np.log(fit["count"]) - pred) ** 2).sum() / ((np.log(fit["count"]) - np.log(fit["count"]).mean()) ** 2).sum()
    n, cit, fwci, oa = summarise(y)
    rows.append(["1990–2025", thousands(n), "100.0", f"{n / 36:.1f}", f"{(np.exp(b1) - 1) * 100:.1f}ᵇ", f"{cit:.1f}", f"{fwci:.2f}", f"{oa:.1f}"])
    return write_table(3, "decades", CAPTION, HEAD, rows, NOTE.format(r2=r2))


if __name__ == "__main__":
    main()
