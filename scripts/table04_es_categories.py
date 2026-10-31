"""Table 4. Ecosystem-service categories: volume, decadal distribution, growth and impact.

Input  : data/processed/services_year.txt  (category | articles | mean citations | mean FWCI | year:count,...)
Output : outputs/tables/Table4_ES_categories.{csv,md,json}
Method : CAGR is smoothed between the 2015–2017 and 2023–2025 three-year means (8-year span).

Run from the repository root:  python scripts/table04_es_categories.py
"""
import numpy as np

from _tables import DATA, N_CORPUS, half_up, thousands, write_table

CAPTION = "Ecosystem-service categories: volume, decadal distribution, growth and impact."
HEAD = ["ES category", "Articles", "Corpus (%)", "2000s", "2010s", "2020–25", "CAGRᵃ (%)", "Mean citations", "Mean FWCI"]
NOTE = ("ᵃ Smoothed CAGR between 2015–2017 and 2023–2025 three-year means. Decadal columns exclude the 1990s "
        "(≤5 articles per category). Categories overlap; percentages do not sum to 100.")
LABEL = {"Crop/food production": "Crop / food production", "Water yield/provision": "Water yield / provision",
         "Habitat quality/biodiversity": "Habitat quality / biodiversity", "Nutrient cycling/retention": "Nutrient cycling / retention",
         "Soil conservation/erosion": "Soil conservation / erosion", "Carbon storage/sequestration": "Carbon storage / sequestration",
         "Urban heat/cooling": "Urban heat mitigation / cooling", "Marine & coastal": "Marine and coastal",
         "Flood/hazard regulation": "Flood / hazard regulation", "Pollination": "Pollination",
         "Cultural/recreation": "Cultural / recreation", "Air purification": "Air purification"}

# The processed file stores means rounded to two decimals, which are rounded half-up to one decimal here.
# One stored value (Habitat quality, 44.85) was itself rounded up from an unrounded OpenAlex mean below 44.85,
# so the article prints 44.8; that cell keeps the article value.
ROUNDED_FROM_SOURCE = {("Habitat quality/biodiversity", "mean_citations"): "44.8"}  # stored 44.85, unrounded < 44.85


def main():
    recs = []
    for line in open(DATA / "services_year.txt", encoding="utf-8"):
        name, n, cit, fwci, ys = line.rstrip("\n").split("|")
        yc = {int(k): int(v) for k, v in (p.split(":") for p in ys.split(","))}
        dec = lambda a, b: sum(v for k, v in yc.items() if a <= k <= b)
        m = lambda a, b: np.mean([yc.get(k, 0) for k in range(a, b + 1)])
        cagr = ((m(2023, 2025) / m(2015, 2017)) ** (1 / 8) - 1) * 100
        recs.append((int(n), [LABEL[name], thousands(int(n)), f"{int(n) / N_CORPUS * 100:.1f}", thousands(dec(2000, 2009)),
                              thousands(dec(2010, 2019)), thousands(dec(2020, 2025)), f"{cagr:.1f}", ROUNDED_FROM_SOURCE.get((name, "mean_citations"), half_up(cit)), f"{float(fwci):.2f}"]))
    rows = [r for _, r in sorted(recs, key=lambda x: -x[0])]
    return write_table(4, "ES_categories", CAPTION, HEAD, rows, NOTE)


if __name__ == "__main__":
    main()
