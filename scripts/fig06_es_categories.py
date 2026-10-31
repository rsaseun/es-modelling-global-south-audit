"""Fig. 6. Annual output of 12 ecosystem-service categories.

Reproduces Fig. 6 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

Output: outputs/figures/Fig06_ES_categories.png (600 dpi), .svg (editable) and .pdf (vector).
Run from the repository root:  python scripts/fig06_es_categories.py
"""
from _common import *  # noqa: F401,F403  (paths, style, palette, helpers)


def fig_services():
    d = pd.read_csv(f"{R}/services_year.csv")
    meta = {}
    for l in open(f"{R}/services_year.txt"):
        n, c, mc, f, _ = l.strip().split("|"); meta[n] = dict(n=int(c), mean_cit=float(mc), fwci=float(f))
    order = sorted(meta, key=lambda k: -meta[k]["n"])
    fig, axs = plt.subplots(3, 4, figsize=(7.4, 5.4), sharex=True)
    for i, (svc, ax) in enumerate(zip(order, axs.flat)):
        s = d[d.service == svc].set_index("year")["count"].reindex(range(2000, 2026), fill_value=0)
        col = CAT[i % 8] if i < 8 else ["#2a78d6", "#eb6834", "#1baf7a", "#6250d6"][i - 8]
        ax.fill_between(s.index, s.values, color=col, alpha=0.22, lw=0)
        ax.plot(s.index, s.values, color=col, lw=1.8)
        ax.set_title(svc, fontsize=7.6, loc="left")
        ax.text(0.03, 0.80, f"n = {meta[svc]['n']:,}\nFWCI {meta[svc]['fwci']:.2f}", transform=ax.transAxes, fontsize=6.4, color=INK2, va="top")
        ax.tick_params(labelsize=6.5); ax.set_xlim(2000, 2025)
        a = s.loc[2015:2017].mean(); b = s.loc[2023:2025].mean()
        meta[svc]["cagr"] = 100 * ((b / a) ** (1 / 8) - 1) if a > 0 else None
        meta[svc]["share_2020s"] = float(d[(d.service == svc) & (d.year >= 2020)]["count"].sum() / meta[svc]["n"] * 100)
        for (aa, bb, l) in DECADES: meta[svc][l] = int(d[(d.service == svc) & (d.year >= aa) & (d.year <= bb)]["count"].sum())
    fig.supylabel("Articles per year", fontsize=8, color=INK2); fig.supxlabel("Publication year", fontsize=8, color=INK2)
    fig.suptitle("Ecosystem-service categories mapped in the corpus (independent axes)", x=0.01, ha="left", fontsize=9.5, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    STATS["services"] = meta
    save(fig, "Fig06_ES_categories")


if __name__ == "__main__":
    fig_services()
    write_stats("fig06_es_categories")
    print("written", FIG_OUT / "Fig06_ES_categories.png")
