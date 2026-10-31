"""Table 6. The 20 most productive journals (screened corpus).

Input  : data/processed/sources_top20.csv (journal, articles, mean citations, mean FWCI, % open access)
Output : outputs/tables/Table6_journals.{csv,md,json}

Run from the repository root:  python scripts/table06_journals.py
"""
import pandas as pd

from _tables import DATA, N_CORPUS, half_up, pct1, thousands, write_table

CAPTION = "The 20 most productive journals (screened corpus)."
HEAD = ["Rank", "Journal", "Articles", "Corpus (%)", "Mean citations", "Mean FWCI", "Open access (%)"]
DISPLAY = {"Land Degradation and Development": "Land Degradation & Development",
           "Int. J. Environ. Res. Public Health": "Int. J. Environmental Research and Public Health",
           "Environment Development and Sustainability": "Environment, Development and Sustainability"}

# sources_top20.csv stores means rounded to two decimals, which are rounded half-up to one decimal here. A stored
# value ending in 5 can come from an unrounded mean just below it; for that tie the article value (rounded from the
# unrounded OpenAlex mean) is kept.
ROUNDED_FROM_SOURCE = {"Land Degradation and Development": "31.6",       # stored 31.65, unrounded mean < 31.65
                       "Frontiers in Environmental Science": "16.0"}     # stored 16.05, unrounded mean < 16.05


def main():
    s = pd.read_csv(DATA / "sources_top20.csv")
    rows = [[str(i), DISPLAY.get(r["name"], r["name"]), thousands(r["count"]), f"{r['count'] / N_CORPUS * 100:.1f}",
             ROUNDED_FROM_SOURCE.get(r["name"], half_up(r.mean_cit)), f"{r.fwci:.2f}", pct1(r.pct_oa)] for i, (_, r) in enumerate(s.iterrows(), start=1)]
    return write_table(6, "journals", CAPTION, HEAD, rows)


if __name__ == "__main__":
    main()
