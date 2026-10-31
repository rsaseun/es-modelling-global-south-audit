"""Shared paths, style, helpers and constants for every figure script.

All figures are drawn from OpenAlex aggregates stored in ``data/processed``
(see ``data/README.md``). The style block (palette, fonts, rcParams) is shared so
that every figure is rendered exactly as in the published article.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data" / "processed"
GEO = REPO / "data" / "geo" / "countries-50m.json"
FIG_OUT = REPO / "outputs" / "figures"
STATS_OUT = REPO / "outputs" / "stats"
FIG_OUT.mkdir(parents=True, exist_ok=True)
STATS_OUT.mkdir(parents=True, exist_ok=True)

import json, os, math
import numpy as np, pandas as pd
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
import networkx as nx
import geopandas as gpd
import pycountry
R = str(DATA)
OUT = str(FIG_OUT)
os.makedirs(OUT, exist_ok=True)
# ---------- style ----------
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
SEQ = mcolors.LinearSegmentedColormap.from_list("seqblue", ["#f4f8fd", "#c6dbf5", "#7fb0ea", "#2a78d6", "#123f7a"])
mpl.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 8.5, "axes.titlesize": 9.5, "axes.titleweight": "bold",
    "axes.labelsize": 8.5, "axes.edgecolor": MUTED, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.axisbelow": True, "legend.frameon": False, "legend.fontsize": 7.5, "savefig.dpi": 600, "figure.dpi": 150,
    "svg.fonttype": "none", "svg.hashsalt": "es-audit", "pdf.fonttype": 42, "axes.titlelocation": "left", "axes.titlepad": 6,
})
STATS = {}

def save(fig, name):
    """Write the figure as 600-dpi PNG, editable SVG and vector PDF (fonts embedded)."""
    fig.savefig(f"{OUT}/{name}.png", bbox_inches="tight", facecolor="white")
    fig.savefig(f"{OUT}/{name}.svg", bbox_inches="tight", facecolor="white")
    fig.savefig(f"{OUT}/{name}.pdf", bbox_inches="tight", facecolor="white")
    plt.close(fig)

def panel(ax, letter):
    ax.text(-0.02, 1.06, letter, transform=ax.transAxes, fontsize=11, fontweight="bold", color=INK, ha="right", va="bottom")
DECADES = [(1990, 1999, "1990s"), (2000, 2009, "2000s"), (2010, 2019, "2010s"), (2020, 2025, "2020–25")]
DEC_SHADE = ["#ffffff", "#f6f5f2", "#ffffff", "#f6f5f2"]

def dec_of(y):
    for a, b, l in DECADES:
        if a <= y <= b: return l
# ---------- data ----------
yr = pd.read_csv(f"{R}/year_overall.txt")
years = np.arange(1990, 2026)
cnt = yr.set_index("year")["count"].reindex(years, fill_value=0)
MNAME = {
    "InVEST": "InVEST suite", 'SWAT OR "Soil and Water Assessment Tool"': "SWAT",
    'ARIES OR "Co$ting Nature" OR "Costing Nature" OR SolVES': "ARIES / Co$ting Nature / SolVES",
    'RUSLE OR USLE OR "universal soil loss"': "(R)USLE",
    '"equivalent factor*" OR "value coefficient*" OR "benefit transfer" OR "unit value*" OR "ecosystem service value*"': "Value-coefficient / benefit transfer (ESV)",
    '"CA-Markov" OR Markov OR "cellular automat*"': "CA–Markov / cellular automata",
    '"PLUS model" OR FLUS OR "CLUE-S" OR "CLUE model" OR "Dyna-CLUE" OR "land use simulation" OR "LUCC simulation"': "PLUS / FLUS / CLUE-S simulation",
    '"machine learning" OR "random forest" OR "deep learning" OR "neural network*" OR XGBoost OR "support vector"': "Machine & deep learning",
    '"Google Earth Engine"': "Google Earth Engine",
    'geodetector OR "geographical detector" OR "geographically weighted regression" OR MGWR': "Geodetector / (M)GWR",
    'SSP* OR RCP* OR CMIP* OR "shared socioeconomic pathway*" OR "representative concentration pathway*"': "SSP–RCP / CMIP scenarios",
    'MaxEnt OR "species distribution model*" OR "ecological niche model*"': "MaxEnt / SDMs",
    'CASA OR "net primary productiv*" OR "light use efficiency"': "CASA / NPP light-use efficiency",
    '"participatory mapping" OR PPGIS OR "participatory GIS" OR stakeholder* OR "local knowledge"': "Participatory / stakeholder mapping",
    '"Bayesian network*" OR "system dynamics" OR "agent-based"': "Bayesian nets / system dynamics / ABM",
    '"uncertainty analysis" OR "sensitivity analysis" OR uncertaint* OR validation OR "field data" OR "in situ"': "Uncertainty, validation & field data",
}
MFAM = {"InVEST suite": "Biophysical ES models", "SWAT": "Biophysical ES models", "ARIES / Co$ting Nature / SolVES": "Biophysical ES models",
        "(R)USLE": "Biophysical ES models", "CASA / NPP light-use efficiency": "Biophysical ES models", "Value-coefficient / benefit transfer (ESV)": "Valuation",
        "CA–Markov / cellular automata": "Land-change simulation", "PLUS / FLUS / CLUE-S simulation": "Land-change simulation",
        "SSP–RCP / CMIP scenarios": "Climate scenarios", "Machine & deep learning": "AI, cloud & spatial statistics", "Google Earth Engine": "AI, cloud & spatial statistics",
        "Geodetector / (M)GWR": "AI, cloud & spatial statistics", "MaxEnt / SDMs": "Biodiversity models", "Participatory / stakeholder mapping": "Social–ecological",
        "Bayesian nets / system dynamics / ABM": "Social–ecological", "Uncertainty, validation & field data": "Credibility practices"}
GS_SET = set("CN IN BR ZA ET MX KE CO AR ID IR CL MY GH PE SA BD EC VN TH TZ TR NG NP PK MA PH LK EG UY BJ UG MZ QA BW CI TN ZW LB TG MN PA VE AE CD IQ KH MG CM DZ MW BF LA ML OM SN BO KW NA RW UZ ZM BT CU GA GY PY BN FJ GT JO KG SD DO MM MR NE SZ TT AF AZ BI CG GE JM KZ LR LS LY MU PG BH BS GM HN HT MV NI PS SC SL SV SY WS YE CR HK MO PR SG NC RE GF PF GP GU KY".split())
# NB: GS membership follows UN/OpenAlex convention for countries (China included); high-income city-states/territories flagged below.
NORTH_LIKE = {"HK", "MO", "SG", "PR", "NC", "RE", "GF", "PF", "GP", "GU", "KY", "QA", "AE", "KW", "BH", "SA", "BN", "IL", "KR", "TW"}

def is_gs(c): return c in GS_SET and c not in NORTH_LIKE


def write_stats(stem):
    """Write the summary statistics computed while drawing a figure (used in the text and tables)."""
    with open(STATS_OUT / f"{stem}.json", "w") as fh:
        json.dump(STATS, fh, indent=1, default=str)
