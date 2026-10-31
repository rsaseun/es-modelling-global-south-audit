"""Table 5. Models and quantification systems: volume, diffusion and impact.

Inputs : data/processed/methods_year_fixed.csv (articles per model/method query and year; InVEST = exact phrase)
         data/processed/methods_summary.csv    (whole-set mean citations, FWCI and % open access per query)
         data/processed/year_overall.txt       (annual corpus size, denominator of the shares)
Output : outputs/tables/Table5_models_methods.{csv,md,json}

Run from the repository root:  python scripts/table05_models_methods.py
"""
import pandas as pd

from _tables import DATA, write_table

CAPTION = "Models and quantification systems: volume, diffusion and impact."
HEAD = ["Model / method family", "Articles", "Share 2015 (%)", "Share 2025 (%)", "Mean citations", "Mean FWCI", "Open access (%)"]
NOTE = ("Shares are percentages of each year’s corpus. “—” = not computed for the exact-match InVEST query. "
        "ABM = agent-based model; SolVES = Social Values for Ecosystem Services.")
LABEL = {
    "InVEST": "InVEST suite (exact match)", 'SWAT OR "Soil and Water Assessment Tool"': "SWAT",
    'ARIES OR "Co$ting Nature" OR "Costing Nature" OR SolVES': "ARIES / Co$ting Nature / SolVES",
    'RUSLE OR USLE OR "universal soil loss"': "(R)USLE",
    '"equivalent factor*" OR "value coefficient*" OR "benefit transfer" OR "unit value*" OR "ecosystem service value*"': "Value-coefficient / benefit transfer (ESV)",
    '"CA-Markov" OR Markov OR "cellular automat*"': "CA–Markov / cellular automata",
    '"PLUS model" OR FLUS OR "CLUE-S" OR "CLUE model" OR "Dyna-CLUE" OR "land use simulation" OR "LUCC simulation"': "PLUS / FLUS / CLUE-S simulation",
    '"machine learning" OR "random forest" OR "deep learning" OR "neural network*" OR XGBoost OR "support vector"': "Machine and deep learning",
    '"Google Earth Engine"': "Google Earth Engine",
    'geodetector OR "geographical detector" OR "geographically weighted regression" OR MGWR': "Geodetector / (M)GWR",
    'SSP* OR RCP* OR CMIP* OR "shared socioeconomic pathway*" OR "representative concentration pathway*"': "SSP–RCP / CMIP scenarios",
    'MaxEnt OR "species distribution model*" OR "ecological niche model*"': "MaxEnt / species distribution models",
    'CASA OR "net primary productiv*" OR "light use efficiency"': "CASA / NPP light-use efficiency",
    '"participatory mapping" OR PPGIS OR "participatory GIS" OR stakeholder* OR "local knowledge"': "Participatory / stakeholder mapping",
    '"Bayesian network*" OR "system dynamics" OR "agent-based"': "Bayesian networks / system dynamics / ABM",
    '"uncertainty analysis" OR "sensitivity analysis" OR uncertaint* OR validation OR "field data" OR "in situ"': "Uncertainty, validation and field data",
}


def main():
    m = pd.read_csv(DATA / "methods_year_fixed.csv").rename(columns={"level0": "q", "level1": "year"})
    m["year"] = m.year.astype(int)
    size = pd.read_csv(DATA / "year_overall.txt").set_index("year")["count"]
    summ = pd.read_csv(DATA / "methods_summary.csv", keep_default_na=False).set_index("query")
    recs = []
    for q, g in m.groupby("q"):
        n = int(g["count"].sum())
        sh = lambda y: g.loc[g.year == y, "count"].sum() / size[y] * 100
        if q == "InVEST":  # exact-phrase InVEST: impact computed for the exact query only
            s = summ.loc["InVEST (exact phrase)"]
            assert int(s["count"]) == n
            cit, fwci, oa = "—", f"{float(s.mean_fwci):.2f}", "—"
        else:
            s = summ.loc[q]
            assert int(s["count"]) == n
            cit, fwci, oa = f"{float(s.mean_citations):.1f}", f"{float(s.mean_fwci):.2f}", f"{float(s.pct_open_access):.1f}"
        recs.append((n, LABEL[q], [LABEL[q], f"{n:,}", f"{sh(2015):.1f}", f"{sh(2025):.1f}", cit, fwci, oa]))
    rows = [r for *_, r in sorted(recs, key=lambda x: (-x[0], x[1]))]
    return write_table(5, "models_methods", CAPTION, HEAD, rows, NOTE)


if __name__ == "__main__":
    main()
