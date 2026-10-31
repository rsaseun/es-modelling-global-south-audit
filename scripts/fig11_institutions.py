"""Fig. 11. The 20 most active institutions.

Reproduces Fig. 11 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

Output: outputs/figures/Fig11_institutions.png (600 dpi), .svg (editable) and .pdf (vector).
Run from the repository root:  python scripts/fig11_institutions.py
"""
from _common import *  # noqa: F401,F403  (paths, style, palette, helpers)


def fig_inst():
    d = pd.read_csv(f"{R}/institutions_top.csv")
    k = d[d.keep == 1].head(20).iloc[::-1]
    grp = {"CN": "China", "FR": "France", "DE": "Germany", "NL": "Netherlands", "BR": "Latin America", "AR": "Latin America", "INT": "International (CGIAR)", "ET": "Africa"}
    gcol = {"China": CAT[7], "France": CAT[0], "Germany": CAT[3], "Netherlands": CAT[1], "Latin America": CAT[2], "International (CGIAR)": CAT[6], "Africa": CAT[5]}
    fig, axs = plt.subplots(1, 2, figsize=(7.4, 4.6), sharey=True, gridspec_kw=dict(width_ratios=[1.5, 1]))
    ax = axs[0]
    cols = [gcol[grp[c]] for c in k.country]
    ax.barh(k.name, k["count"], color=cols, height=0.7, edgecolor="white")
    for i, v in enumerate(k["count"]): ax.text(v + 12, i, f"{v:,}", fontsize=6.3, va="center", color=INK2)
    ax.set_xlabel("Articles"); ax.tick_params(axis="y", labelsize=6.6); ax.set_xlim(0, 1300); ax.grid(axis="y", visible=False)
    ax.set_title("Top-20 active institutions"); panel(ax, "a")
    used = list(dict.fromkeys(grp[c] for c in k.country[::-1]))
    ax.legend(handles=[Patch(color=gcol[g], label=g) for g in used], loc="lower right", fontsize=6.4)
    ax = axs[1]
    ax.hlines(range(len(k)), 0, k.fwci, color=GRID, lw=2)
    ax.scatter(k.fwci, range(len(k)), color=cols, s=36, edgecolor="white", linewidth=0.8, zorder=3)
    ax.axvline(3.73, color=MUTED, ls=":", lw=0.9)
    ax.set_xlabel("Mean FWCI"); ax.set_title("Field-weighted impact"); ax.grid(axis="y", visible=False); panel(ax, "b")
    fig.tight_layout()
    save(fig, "Fig11_institutions")


if __name__ == "__main__":
    fig_inst()
    write_stats("fig11_institutions")
    print("written", FIG_OUT / "Fig11_institutions.png")
