"""Fig. 5. Evolution of concepts (OpenAlex keywords).

Reproduces Fig. 5 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

Output: outputs/figures/Fig05_concepts.png (600 dpi), .svg (editable) and .pdf (vector).
Run from the repository root:  python scripts/fig05_concepts.py
"""
from _common import *  # noqa: F401,F403  (paths, style, palette, helpers)


def fig_concepts():
    d = pd.read_csv(f"{R}/year_keyword.csv").rename(columns={"level0": "year", "level1": "kw"})
    d["year"] = d.year.astype(int); d["dec"] = d.year.apply(dec_of)
    labels = pd.read_csv(f"{R}/keywords_top60.csv").set_index("id")["name"].to_dict()
    pv = d.pivot_table(index="kw", columns="dec", values="count", aggfunc="sum").fillna(0)[[x[2] for x in DECADES]]
    decn = cnt.groupby([dec_of(y) for y in cnt.index]).sum().reindex(pv.columns)
    share = pv.div(decn, axis=1) * 100
    emerg = (share["2020–25"] + 0.01) / (share["2010s"] + 0.01)
    order = emerg.sort_values(ascending=True).index
    STATS["kw_share"] = share.round(2).to_dict(); STATS["kw_emergence"] = emerg.round(2).to_dict()
    fig = plt.figure(figsize=(7.2, 6.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[2.2, 1.3], wspace=0.06)
    ax = fig.add_subplot(gs[0])
    for i, k in enumerate(order):
        for j, c in enumerate(pv.columns):
            v = pv.loc[k, c]
            if v > 0:
                ax.scatter(j, i, s=6 + 0.45 * v, color=SEQ(min(1.0, 0.25 + share.loc[k, c] / 20.0)), edgecolor="white", linewidth=0.6, zorder=3)
            ax.text(j + 0.36, i, f"{share.loc[k,c]:.1f}%" if v > 0 else "", fontsize=5.6, va="center", color=MUTED)
    ax.set_yticks(range(len(order))); ax.set_yticklabels([labels.get(k, k) for k in order], fontsize=7)
    ax.set_xticks(range(4)); ax.set_xticklabels([f"{c}\n(n={int(decn[c]):,})" for c in pv.columns]); ax.set_xlim(-0.5, 3.9)
    ax.set_title("Concept prevalence by decade"); ax.grid(axis="x", visible=False)
    for s_ in [10, 100, 300]:
        ax.scatter([], [], s=6 + 0.45 * s_, color=SEQ(0.5), label=f"{s_}")
    ax.legend(title="Articles", loc="lower left", bbox_to_anchor=(0, -0.15), ncol=3, fontsize=6.5, title_fontsize=6.8)
    panel(ax, "a")
    ax2 = fig.add_subplot(gs[1], sharey=ax)
    v = emerg.reindex(order)
    col = [CAT[2] if x >= 1.5 else (CAT[0] if x >= 1 else CAT[1]) for x in v.values]
    ax2.barh(range(len(v)), v.values, color=col, height=0.62, edgecolor="white")
    ax2.axvline(1, color=INK2, lw=0.9)
    for i, x in enumerate(v.values): ax2.text(x + 0.05, i, f"{x:.2f}", fontsize=6.2, va="center", color=INK2)
    ax2.tick_params(labelleft=False); ax2.grid(axis="y", visible=False)
    ax2.set_title("Emergence index (2020–25 ÷ 2010s)", fontsize=8)
    ax2.legend(handles=[Patch(color=CAT[2], label="Strongly emergent (≥1.5)"), Patch(color=CAT[0], label="Growing (1–1.5)"),
                        Patch(color=CAT[1], label="Declining share (<1)")], loc="lower right", fontsize=6.2)
    panel(ax2, "b")
    save(fig, "Fig05_concepts")


if __name__ == "__main__":
    fig_concepts()
    write_stats("fig05_concepts")
    print("written", FIG_OUT / "Fig05_concepts.png")
