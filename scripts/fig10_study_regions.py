"""Fig. 10. Study-area regions.

Reproduces Fig. 10 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

Output: outputs/figures/Fig10_study_regions.png (600 dpi), .svg (editable) and .pdf (vector).
Run from the repository root:  python scripts/fig10_study_regions.py
"""
from _common import *  # noqa: F401,F403  (paths, style, palette, helpers)


def fig_regions():
    d = pd.read_csv(f"{R}/regions_year.csv")
    meta = {}
    for l in open(f"{R}/regions_year.txt"):
        n, c, mc, f, oa, _ = l.strip().split("|"); meta[n] = dict(n=int(c), mean_cit=float(mc), fwci=float(f), oa=float(oa))
    order = ["China", "Latin America & Caribbean", "Sub-Saharan Africa", "South & Southeast Asia", "MENA & Central Asia", "Pacific SIDS"]
    fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.3), gridspec_kw=dict(width_ratios=[1.35, 1]))
    ax = axs[0]
    for i, r in enumerate(order):
        s = d[d.region == r].set_index("year")["count"].reindex(range(2000, 2026), fill_value=0)
        ax.plot(s.index, s.values, color=CAT[i], lw=2 if i < 3 else 1.6, label=r)
    ax.set_yscale("symlog", linthresh=10); ax.set_xlim(2000, 2025); ax.set_ylabel("Articles per year (symlog)")
    ax.set_title("Study-area mentions by Global South region"); ax.legend(loc="upper left", fontsize=6.3)
    ax.set_xlabel("Publication year"); panel(ax, "a")
    ax = axs[1]
    rows = []
    for r in order[:-1]:
        s = d[d.region == r]
        rows.append([r] + [int(s[(s.year >= a) & (s.year <= b)]["count"].sum()) for a, b, l in DECADES])
    t = pd.DataFrame(rows, columns=["r"] + [x[2] for x in DECADES]).set_index("r")
    sh = t.div(t.sum(0), axis=1) * 100
    bottom = np.zeros(4)
    for i, r in enumerate(sh.index):
        ax.bar(range(4), sh.loc[r].values, bottom=bottom, color=CAT[i], edgecolor="white", linewidth=1.2, width=0.68)
        for j, v in enumerate(sh.loc[r].values):
            if v > 7: ax.text(j, bottom[j] + v / 2, f"{v:.0f}", ha="center", va="center", fontsize=6.6, color="white", fontweight="bold")
        bottom += sh.loc[r].values
    ax.set_xticks(range(4)); ax.set_xticklabels(sh.columns); ax.set_ylim(0, 100); ax.set_ylabel("% of region-tagged articles")
    ax.set_title("Regional composition by decade"); ax.grid(axis="x", visible=False); panel(ax, "b")
    fig.tight_layout(w_pad=4)
    STATS["regions"] = meta; STATS["region_dec"] = t.to_dict(); STATS["region_share_dec"] = sh.round(1).to_dict()
    save(fig, "Fig10_study_regions")


if __name__ == "__main__":
    fig_regions()
    write_stats("fig10_study_regions")
    print("written", FIG_OUT / "Fig10_study_regions.png")
