"""Fig. 1. Retrieval and screening workflow.

Reproduces Fig. 1 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

Output: outputs/figures/Fig01_screening_flow.png (600 dpi), .svg (editable) and .pdf (vector).
Run from the repository root:  python scripts/fig01_screening_flow.py
"""
from _common import *  # noqa: F401,F403  (paths, style, palette, helpers)


def fig_flow():
    fig, ax = plt.subplots(figsize=(7.0, 5.6)); ax.set_axis_off(); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    def box(x, y, w, h, title, body, fc, ec):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.6", fc=fc, ec=ec, lw=1.1))
        ax.text(x + w / 2, y + h - 2.2, title, ha="center", va="top", fontsize=8.3, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 7.0, body, ha="center", va="top", fontsize=7.3, color=INK2, linespacing=1.35)
    def arrow(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.0))
    stages = [("IDENTIFICATION", 86), ("SCREENING", 63), ("ELIGIBILITY", 36), ("INCLUDED", 8)]
    for s, y in stages:
        ax.text(1, y + 4, s, rotation=90, fontsize=7.5, fontweight="bold", color=CAT[0], va="center")
    box(8, 80, 48, 17, "OpenAlex OQL retrieval (1990–2025)",
        "ES × spatial modelling × climate/environmental\nchange × Global South (affiliation or study area)\nn = 9,632 records (articles + reviews)", "#eaf2fc", CAT[0])
    box(62, 80, 36, 17, "Cross-validation sources",
        "Google Scholar & Dimensions: recall\nbenchmarking of seed set; no\nrecords harvested (see §3.1)", "#fdf0ea", CAT[1])
    arrow(32, 80, 32, 74)
    box(8, 53, 48, 21, "Automated screening",
        "Retracted (−4) → 9,628\nNon-journal: repositories/preprints,\nconference, book series (−587) → 9,041\nNon-English (−249) → 8,792", "#f6f5f2", MUTED)
    box(62, 53, 36, 21, "Excluded records",
        "Retracted 4\nNon-journal 587\nNon-English 249\nΣ 840", "#fbeaea", CAT[7])
    arrow(56, 63, 62, 63); arrow(32, 53, 32, 49)
    box(8, 27, 48, 21, "Source-quality screening",
        "No CWTS-core indexation and not in DOAJ\n(untracked peer review) (−706) → 8,086\nStop Predatory Journals publisher list\nmatches, 12 publishers (−75) → 8,011", "#f6f5f2", MUTED)
    box(62, 27, 36, 21, "Excluded sources",
        "Untracked peer review 706\nPredatory-listed 75\nOff-domain primary field\n(medicine, nursing, arts…) 39", "#fbeaea", CAT[7])
    arrow(56, 37, 62, 37); arrow(32, 27, 32, 22.5)
    box(8, 3, 48, 19, "Final analytical corpus",
        "n = 7,972 peer-reviewed journal articles\n1,143 journals · 168 countries · 5,150 institutions\nPrecision (random audit, n = 25): 72–80%", "#e8f6ef", CAT[2])
    box(62, 3, 36, 19, "Analyses",
        "Growth & decadal dynamics · subjects\nthemes & concepts · ES categories\nmodels · geography · institutions\ncollaboration network · equity", "#f1eefb", CAT[6])
    arrow(56, 12, 62, 12)
    ax.text(34, 24.6, "Topical filter (−39) → 7,972", ha="left", fontsize=7, color=CAT[7], style="italic")
    save(fig, "Fig01_screening_flow")


if __name__ == "__main__":
    fig_flow()
    write_stats("fig01_screening_flow")
    print("written", FIG_OUT / "Fig01_screening_flow.png")
