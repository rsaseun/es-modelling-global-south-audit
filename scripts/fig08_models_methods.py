"""Fig. 8. Diffusion of models, quantification systems and credibility practices.

Reproduces Fig. 8 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

Output: outputs/figures/Fig08_models_methods.png (600 dpi), .svg (editable) and .pdf (vector).
Run from the repository root:  python scripts/fig08_models_methods.py
"""
from _common import *  # noqa: F401,F403  (paths, style, palette, helpers)


def fig_methods():
    m = pd.read_csv(f"{R}/methods_year_fixed.csv").rename(columns={"level0": "m", "level1": "year"})
    m["name"] = m.m.map(MNAME); m["year"] = m.year.astype(int)
    hm = m[m.year >= 2005].pivot_table(index="name", columns="year", values="count", aggfunc="sum").fillna(0).reindex(columns=range(2005, 2026), fill_value=0)
    pct = hm.div(cnt.reindex(hm.columns).values, axis=1) * 100
    tot = m.groupby("name")["count"].sum()
    fams = list(dict.fromkeys(MFAM[n] for n in sorted(tot.index, key=lambda n: (list(MFAM.values()).index(MFAM[n]), -tot[n]))))
    order = sorted(tot.index, key=lambda n: (fams.index(MFAM[n]), -tot[n]))
    pct = pct.reindex(order); hm = hm.reindex(order)
    STATS["methods_tot"] = tot.to_dict()
    STATS["methods_share_2025"] = pct[2025].round(1).to_dict(); STATS["methods_share_2015"] = pct[2015].round(1).to_dict()
    fig = plt.figure(figsize=(7.4, 5.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[4.6, 1.3], wspace=0.04)
    ax = fig.add_subplot(gs[0])
    im = ax.imshow(pct.values, aspect="auto", cmap=SEQ, vmin=0, vmax=np.nanpercentile(pct.values, 98))
    ax.set_yticks(range(len(pct))); ax.set_yticklabels(pct.index, fontsize=7)
    ax.set_xticks(range(0, 21, 5)); ax.set_xticklabels(range(2005, 2026, 5)); ax.grid(False)
    for s in ax.spines.values(): s.set_visible(False)
    prev = None
    famcol = dict(zip(fams, CAT))
    for i, n in enumerate(order):
        if MFAM[n] != prev and i > 0: ax.axhline(i - 0.5, color="white", lw=2.2)
        prev = MFAM[n]
        ax.add_patch(plt.Rectangle((20.62, i - 0.5), 0.45, 1, color=famcol[MFAM[n]], clip_on=False))
    ax.set_xlim(-0.5, 21.1)
    cax = fig.add_axes([0.40, 0.02, 0.30, 0.014]); cb = fig.colorbar(im, cax=cax, orientation="horizontal"); cb.set_label("% of annual corpus mentioning the model/method", fontsize=7)
    ax.set_title("Diffusion of models and credibility practices, 2005–2025"); panel(ax, "a")
    fig.legend(handles=[Patch(color=famcol[f], label=f) for f in fams], loc="lower left", bbox_to_anchor=(0.0, -0.12), ncol=3, fontsize=6.3)
    ax2 = fig.add_subplot(gs[1], sharey=ax)
    ax2.barh(range(len(order)), tot.reindex(order).values, color=[famcol[MFAM[n]] for n in order], height=0.64, edgecolor="white")
    for i, v in enumerate(tot.reindex(order).values): ax2.text(v + 15, i, f"{int(v):,}", fontsize=6.3, va="center", color=INK2)
    ax2.tick_params(labelleft=False); ax2.grid(axis="y", visible=False); ax2.set_xlim(0, 1250); ax2.set_title("Articles, 1990–2025", fontsize=8); panel(ax2, "b")
    save(fig, "Fig08_models_methods")


if __name__ == "__main__":
    fig_methods()
    write_stats("fig08_models_methods")
    print("written", FIG_OUT / "Fig08_models_methods.png")
