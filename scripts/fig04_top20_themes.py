"""Fig. 4. Annual growth of the top-20 research themes.

Reproduces Fig. 4 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

Output: outputs/figures/Fig04_top20_themes.png (600 dpi), .svg (editable) and .pdf (vector).
Run from the repository root:  python scripts/fig04_top20_themes.py
"""
from _common import *  # noqa: F401,F403  (paths, style, palette, helpers)


def fig_themes():
    d = pd.read_csv(f"{R}/year_topic.csv").rename(columns={"level0": "year", "level1": "topic"})
    d["year"] = d.year.astype(int)
    topics = pd.read_csv(f"{R}/topics_top25.csv")
    order = [t for t in topics.name if t in d.topic.unique()][:20]
    hm = d[(d.year >= 2000) & d.topic.isin(order)].pivot_table(index="topic", columns="year", values="count", aggfunc="sum").reindex(order).fillna(0)
    hm = hm.reindex(columns=range(2000, 2026), fill_value=0)
    tot = d[d.topic.isin(order)].groupby("topic")["count"].sum().reindex(order)
    def cagr(row):
        a = row.loc[2015:2017].mean(); b = row.loc[2023:2025].mean()
        return 100 * ((b / a) ** (1 / 8) - 1) if a > 0 else np.nan
    cg = hm.apply(cagr, axis=1)
    STATS["topic_cagr"] = cg.round(1).to_dict(); STATS["topic_tot"] = tot.to_dict()
    fig = plt.figure(figsize=(7.4, 6.2))
    gs = fig.add_gridspec(1, 3, width_ratios=[5.2, 1.1, 1.0], wspace=0.05)
    ax = fig.add_subplot(gs[0])
    im = ax.imshow(np.log10(hm.values + 1), aspect="auto", cmap=SEQ)
    ax.set_yticks(range(len(hm))); ax.set_yticklabels([f"T{i+1:02d}  {t}" for i, t in enumerate(hm.index)], fontsize=6.9)
    ax.set_xticks(range(0, 26, 5)); ax.set_xticklabels(range(2000, 2026, 5)); ax.grid(False)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title("Annual output of the top-20 research themes (OpenAlex topics)")
    for (a, b, l) in DECADES[1:]:
        ax.axvline(max(a, 2000) - 2000 - 0.5, color="white", lw=1.6)
    cax = fig.add_axes([0.13, 0.035, 0.32, 0.015])
    cb = fig.colorbar(im, cax=cax, orientation="horizontal"); cb.set_label("Articles per year (log₁₀[n+1])", fontsize=7)
    panel(ax, "a")
    ax2 = fig.add_subplot(gs[1], sharey=ax)
    ax2.barh(range(len(tot)), tot.values, color=CAT[0], height=0.66, edgecolor="white")
    ax2.set_xscale("log"); ax2.set_title("Total", fontsize=8); ax2.tick_params(labelleft=False); ax2.grid(axis="y", visible=False)
    for i, v in enumerate(tot.values): ax2.text(v * 1.08, i, f"{int(v):,}", va="center", fontsize=6.2, color=INK2)
    ax2.set_xlim(10, 40000); ax2.set_xticks([100, 1000]); ax2.set_xticklabels(["100", "1k"], fontsize=6.5); panel(ax2, "b")
    ax3 = fig.add_subplot(gs[2], sharey=ax)
    colors = [CAT[2] if v >= cg.median() else CAT[1] for v in cg.values]
    ax3.barh(range(len(cg)), cg.values, color=colors, height=0.66, edgecolor="white")
    ax3.axvline(cg.median(), color=INK2, lw=0.8, ls=":")
    ax3.set_title("CAGR %\n2016→2024", fontsize=8); ax3.tick_params(labelleft=False); ax3.grid(axis="y", visible=False)
    for i, v in enumerate(cg.values):
        if not np.isnan(v): ax3.text(max(v, 0) + 1, i, f"{v:.0f}", va="center", fontsize=6.2, color=INK2)
    panel(ax3, "c")
    save(fig, "Fig04_top20_themes")


if __name__ == "__main__":
    fig_themes()
    write_stats("fig04_top20_themes")
    print("written", FIG_OUT / "Fig04_top20_themes.png")
