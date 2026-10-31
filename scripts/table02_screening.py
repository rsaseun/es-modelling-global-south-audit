"""Table 2. Screening stages, criteria and record counts (OpenAlex, retrieved October 2026).

Inputs : data/processed/screening_log.csv   (records identified and excluded at each stage)
         data/processed/relevance_audit.csv (random relevance audit of the final corpus)
Output : outputs/tables/Table2_screening.{csv,md,json}

Run from the repository root:  python scripts/table02_screening.py
"""
import pandas as pd

from _tables import DATA, N_CORPUS, thousands, write_table

CAPTION = "Screening stages, criteria and record counts (OpenAlex, retrieved October 2026)."
HEAD = ["Stage", "Criterion", "Excluded", "Remaining", "Share retained (%)"]


def share(remaining, identified):
    v = remaining / identified * 100
    # two decimals where one decimal would round a value below 100 up to 100.0
    return f"{v:.2f}" if (round(v, 1) == 100 and remaining < identified) else f"{v:.1f}"


def main():
    log = pd.read_csv(DATA / "screening_log.csv", dtype=str, keep_default_na=False)
    identified = int(log.loc[0, "identified"])
    remaining, rows = identified, []
    for _, r in log.iterrows():
        if r.stage == "0":
            rows.append([r.stage, r.criterion, "—", thousands(identified), share(identified, identified)])
            continue
        remaining -= int(r.excluded)
        rows.append([r.stage, r.criterion, thousands(int(r.excluded)), thousands(remaining), share(remaining, identified)])
    assert remaining == N_CORPUS, f"screening chain ends at {remaining}, expected {N_CORPUS}"
    a = pd.read_csv(DATA / "relevance_audit.csv").iloc[0]
    p = lambda k: round(a[k] / a.sample_size * 100)
    rows.append(["Audit", f"Random relevance audit of final corpus (n = {a.sample_size}): strictly relevant {a.strictly_relevant} "
                 f"({p('strictly_relevant')}%), marginal {a.marginal} ({p('marginal')}%), off-topic {a.off_topic} ({p('off_topic')}%)",
                 "—", thousands(remaining), "—"])
    return write_table(2, "screening", CAPTION, HEAD, rows)


if __name__ == "__main__":
    main()
