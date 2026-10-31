"""Fig. 2. Growth dynamics, 1990–2025.

Reproduces Fig. 2 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

Output: outputs/figures/Fig02_growth.png (600 dpi), .svg (editable) and .pdf (vector).
Run from the repository root:  python scripts/fig02_growth.py
"""
from _common import *  # noqa: F401,F403  (paths, style, palette, helpers)


def fig_growth():
    fig, axs = plt.subplots(2, 2, figsize=(7.2, 5.4))
    ax = axs[0, 0]
    for (a, b, l), c in zip(DECADES, DEC_SHADE):
        for A in axs.flat: A.axvspan(a - 0.5, b + 0.5, color=c, zorder=0, lw=0)
    colors = [CAT[i] for i in [6, 4, 0, 1]]
    for (a, b, l), c in zip(DECADES, colors):
        sel = (years >= a) & (years <= b)
        ax.bar(years[sel], cnt.values[sel], width=0.78, color=c, edgecolor="white", linewidth=0.4, zorder=3, label=l)
    # exponential fit 2000-2025
    m = (years >= 2000)
    b1, b0 = np.polyfit(years[m] - 2000, np.log(cnt.values[m]), 1)
    fit = np.exp(b0 + b1 * (years[m] - 2000))
    ss_res = np.sum((np.log(cnt.values[m]) - (b0 + b1 * (years[m] - 2000))) ** 2)
    ss_tot = np.sum((np.log(cnt.values[m]) - np.log(cnt.values[m]).mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    ax.plot(years[m], fit, color=INK, lw=1.2, ls="--", zorder=4, label="Exponential fit (2000–2025)")
    STATS["exp_growth_rate"] = float(np.exp(b1) - 1); STATS["exp_r2"] = float(r2); STATS["doubling_time"] = float(np.log(2) / b1)
    ax.set_title("Annual output"); ax.set_ylabel("Articles per year"); ax.set_xlim(1989, 2026)
    ax.text(0.03, 0.62, f"Growth rate = {100*(np.exp(b1)-1):.1f}% per year\nR² = {r2:.2f}; doubling time = {np.log(2)/b1:.1f} yr", transform=ax.transAxes, fontsize=7.2, color=INK2, va="top")
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0), ncol=1, fontsize=6.6, handlelength=1.2, borderaxespad=0.1)
    leg = ax.get_legend(); leg.set_bbox_to_anchor((0.0, 1.0)); ax.get_legend().remove()
    ax.legend(loc="upper left", fontsize=6.6, ncol=2, handlelength=1.0, columnspacing=0.8, bbox_to_anchor=(0, 1.02))
    panel(ax, "a")
    ax = axs[0, 1]
    cum = cnt.cumsum()
    ax.fill_between(years, cum.values, color=CAT[0], alpha=0.18, lw=0, zorder=2)
    ax.plot(years, cum.values, color=CAT[0], lw=2, zorder=3)
    for y in [1999, 2009, 2019, 2025]:
        ax.plot(y, cum[y], "o", ms=5, mfc="white", mec=CAT[0], mew=1.5, zorder=4)
        ax.annotate(f"{cum[y]:,}", (y, cum[y]), xytext=(-6, 6), textcoords="offset points", fontsize=7, color=INK, ha="right")
    ax.set_title("Cumulative corpus"); ax.set_ylabel("Cumulative articles"); ax.set_xlim(1989, 2026); panel(ax, "b")
    ax = axs[1, 0]
    yy = yr[yr.year >= 2000]
    ax.plot(yy.year, yy.median_cit, color=CAT[1], lw=2, marker="o", ms=3.5, mfc="white", mew=1.2)
    ax.set_title("Median citations per article"); ax.set_ylabel("Citations (median)"); ax.set_xlim(1999, 2026); panel(ax, "c")
    ax.text(2019.5, 50, "citation window\nstill open", fontsize=7, color=MUTED, ha="center")
    ax = axs[1, 1]
    ax.plot(yy.year, yy.pct_oa, color=CAT[2], lw=2, marker="o", ms=3.5, mfc="white", mew=1.2)
    ax.set_ylim(0, 100); ax.set_title("Open-access share"); ax.set_ylabel("% open access"); ax.set_xlim(1999, 2026); panel(ax, "d")
    for A in axs.flat: A.set_xlabel("Publication year")
    fig.tight_layout(h_pad=1.6, w_pad=1.6)
    save(fig, "Fig02_growth")
    # decadal stats
    rows = []
    for a, b, l in DECADES:
        s = yr[(yr.year >= a) & (yr.year <= b)]
        n = int(s["count"].sum())
        first, last = cnt[a], cnt[b]
        span = b - a
        cagr = (last / first) ** (1 / span) - 1 if first > 0 else np.nan
        rows.append(dict(period=l, years=f"{a}–{b}", n=n, share=100 * n / cnt.sum(), annual_mean=n / (span + 1),
                         cagr=100 * cagr if not np.isnan(cagr) else None,
                         mean_cit=float((s["count"] * s.mean_cit).sum() / n), fwci=float((s["count"] * s.fwci).sum() / n),
                         pct_oa=float((s["count"] * s.pct_oa).sum() / n)))
    STATS["decades"] = rows


if __name__ == "__main__":
    fig_growth()
    write_stats("fig02_growth")
    print("written", FIG_OUT / "Fig02_growth.png")
