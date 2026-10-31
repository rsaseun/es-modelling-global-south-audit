"""Fig. 13. Equity and capacity indicators.

Reproduces Fig. 13 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

Output: outputs/figures/Fig13_equity_challenges.png (600 dpi), .svg (editable) and .pdf (vector).
Run from the repository root:  python scripts/fig13_equity_challenges.py
"""
from _common import *  # noqa: F401,F403  (paths, style, palette, helpers)


def fig_equity():
    d = pd.read_csv(f"{R}/region_collab_gs.csv")
    regs = ["Sub-Saharan Africa", "Latin America & Caribbean", "South & Southeast Asia", "China"]
    fig, axs = plt.subplots(2, 2, figsize=(7.4, 5.6))
    ax = axs[0, 0]
    g = d.groupby(["region", "gs_author"])["count"].sum().unstack()
    pct = (100 * g[False] / (g[False] + g[True])).reindex(regs)
    ax.barh(regs[::-1], pct.reindex(regs[::-1]).values, color=[CAT[7], CAT[3], CAT[0], CAT[2]][::-1], height=0.6, edgecolor="white")
    for i, v in enumerate(pct.reindex(regs[::-1]).values): ax.text(v + 0.8, i, f"{v:.1f}%", fontsize=7, va="center", color=INK)
    ax.set_xlim(0, 45); ax.set_xlabel("% of articles with no Global South-affiliated author"); ax.grid(axis="y", visible=False)
    ax.set_title("Externally led (‘parachute’) research"); panel(ax, "a")
    ax = axs[0, 1]
    bins = ["0-1", "2", "3-4", "5+"]
    x = np.arange(len(bins)); w = 0.2
    for i, r in enumerate(regs):
        s = d[(d.region == r) & (d.gs_author == True)].set_index("countries_bin").reindex(bins)
        ax.bar(x + (i - 1.5) * w, s.fwci, width=w * 0.92, color=[CAT[7], CAT[3], CAT[0], CAT[2]][i], label=r, edgecolor="white")
    ax.set_xticks(x); ax.set_xticklabels(["1 country", "2", "3–4", "≥5"]); ax.set_xlabel("Countries per article (GS-inclusive teams)")
    ax.set_ylabel("Mean FWCI"); ax.set_title("Impact dividend of collaboration"); ax.legend(fontsize=6.2, loc="upper left"); ax.grid(axis="x", visible=False); panel(ax, "b")
    ax = axs[1, 0]
    f = pd.read_csv(f"{R}/funders_top20.csv")
    orig = f.groupby("country")["count"].sum().sort_values()
    lab = {"CN": "China", "BR": "Brazil", "US": "USA", "EU": "European Union", "GB": "UK", "DE": "Germany", "INT": "CGIAR (intl.)", "ZA": "South Africa"}
    colmap = {"CN": CAT[7], "BR": CAT[2], "ZA": CAT[5], "US": CAT[0], "EU": CAT[6], "GB": CAT[1], "DE": CAT[3], "INT": CAT[4]}
    ax.barh([lab[c] for c in orig.index], orig.values, color=[colmap[c] for c in orig.index], height=0.6, edgecolor="white")
    for i, v in enumerate(orig.values): ax.text(v + 25, i, f"{v:,}", fontsize=6.6, va="center", color=INK2)
    ax.set_xlim(0, 3700); ax.set_xlabel("Funding acknowledgements (top-20 funders)"); ax.grid(axis="y", visible=False)
    ax.set_title("Who funds the evidence base?"); panel(ax, "c")
    ax = axs[1, 1]
    cb = {"0-1": (4916, 3.06), "2": (1813, 4.15), "3-4": (914, 4.55), "5+": (329, 9.06)}
    tot = sum(v[0] for v in cb.values())
    ax.bar(range(4), [100 * v[0] / tot for v in cb.values()], color=CAT[0], width=0.6, edgecolor="white")
    for i, (k_, v) in enumerate(cb.items()):
        ax.text(i, 100 * v[0] / tot + 1.5, f"{100*v[0]/tot:.1f}%\nFWCI {v[1]:.2f}", ha="center", fontsize=6.4, color=INK2)
    ax.set_xticks(range(4)); ax.set_xticklabels(["1 country", "2", "3–4", "≥5"]); ax.set_ylim(0, 80); ax.set_ylabel("% of corpus")
    ax.set_title("Team internationalisation (whole corpus)"); ax.grid(axis="x", visible=False); panel(ax, "d")
    fig.tight_layout(h_pad=2.0, w_pad=2.0)
    STATS["parachute_pct"] = pct.round(1).to_dict(); STATS["funder_origin"] = orig.to_dict()
    save(fig, "Fig13_equity_challenges")


if __name__ == "__main__":
    fig_equity()
    write_stats("fig13_equity_challenges")
    print("written", FIG_OUT / "Fig13_equity_challenges.png")
