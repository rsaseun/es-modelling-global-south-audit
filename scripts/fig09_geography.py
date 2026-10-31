"""Fig. 9. Geographic distribution of authorship.

Reproduces Fig. 9 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

Output: outputs/figures/Fig09_geography.png (600 dpi), .svg (editable) and .pdf (vector).
Run from the repository root:  python scripts/fig09_geography.py
"""
from _common import *  # noqa: F401,F403  (paths, style, palette, helpers)


def fig_geo():
    ct = pd.read_csv(f"{R}/country_totals.csv", keep_default_na=False)
    world = gpd.read_file(str(GEO), layer="countries")
    def a2(num):
        try: return pycountry.countries.get(numeric=str(num).zfill(3)).alpha_2
        except Exception: return None
    world["iso2"] = world["id"].apply(a2)
    world.loc[world.name == "Kosovo", "iso2"] = "XK"
    world = world[world.name != "Antarctica"].set_crs("EPSG:4326")
    from shapely.ops import transform as _tf
    from shapely.geometry import box as _box
    world = world.explode(index_parts=False)
    def _fix(geom):
        x0, y0, x1, y1 = geom.bounds
        if x1 - x0 < 300: return geom
        g2 = _tf(lambda x, y, z=None: (np.where(np.asarray(x) < 0, np.asarray(x) + 360, x), y), geom)
        return g2.intersection(_box(-180, -90, 180, 90)).union(_tf(lambda x, y, z=None: (np.asarray(x) - 360, y), g2).intersection(_box(-180, -90, 180, 90)))
    world["geometry"] = world.geometry.apply(_fix)
    world = world[~world.geometry.is_empty].dissolve(by=["id", "name"], as_index=False)
    world = world.merge(ct[["iso2", "count", "fwci"]], on="iso2", how="left")
    fig = plt.figure(figsize=(7.4, 6.4))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.35, 1], width_ratios=[1, 1], hspace=0.30, wspace=0.35)
    ax = fig.add_subplot(gs[0, :])
    bounds = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 4000]
    cmap = mcolors.LinearSegmentedColormap.from_list("s", ["#e3eefb", "#9cc2ef", "#2a78d6", "#14478c", "#0a2550"], N=len(bounds) - 1)
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    world[world["count"].isna()].plot(ax=ax, color="#efeeeb", edgecolor="white", linewidth=0.25)
    world[world["count"].notna()].plot(ax=ax, column="count", cmap=cmap, norm=norm, edgecolor="white", linewidth=0.25)
    ax.set_xlim(-170, 190); ax.set_ylim(-57, 84); ax.set_aspect(1.15); ax.set_axis_off(); ax.set_title("Geographic distribution of authorship (articles with ≥1 author affiliated in the country)")
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cax = fig.add_axes([0.30, 0.475, 0.40, 0.011])
    cb = fig.colorbar(sm, cax=cax, orientation="horizontal", ticks=bounds); cb.ax.tick_params(labelsize=6.3); cb.set_label("Articles (1990–2025)", fontsize=7)
    panel(ax, "a")
    ax2 = fig.add_subplot(gs[1, 0])
    top = ct.head(20).iloc[::-1]
    cols = [CAT[1] if is_gs(c) else CAT[0] for c in top.iso2]
    ax2.barh(top.name, top["count"], color=cols, height=0.7, edgecolor="white")
    for i, v in enumerate(top["count"]): ax2.text(v + 30, i, f"{v:,}", fontsize=6.2, va="center", color=INK2)
    ax2.tick_params(axis="y", labelsize=6.6); ax2.set_xlabel("Articles"); ax2.set_xlim(0, 4600); ax2.grid(axis="y", visible=False)
    ax2.set_title("Top-20 countries"); panel(ax2, "b")
    ax2.legend(handles=[Patch(color=CAT[1], label="Global South"), Patch(color=CAT[0], label="Global North")], loc="lower right", fontsize=6.5)
    ax3 = fig.add_subplot(gs[1, 1])
    c30 = ct[ct["count"] >= 40].copy()
    c30["gs"] = c30.iso2.apply(is_gs)
    for g, col, lab in [(True, CAT[1], "Global South"), (False, CAT[0], "Global North")]:
        s = c30[c30.gs == g]
        ax3.scatter(s["count"], s.fwci, s=18, color=col, edgecolor="white", linewidth=0.6, label=lab, zorder=3)
    for _, r in c30.iterrows():
        if r["count"] > 250 or r.fwci > 8 or r.iso2 in ("ET", "KE", "NG", "GH"):
            ax3.annotate(r.iso2, (r["count"], r.fwci), xytext=(3, 2), textcoords="offset points", fontsize=6.2, color=INK2)
    ax3.set_xscale("log"); ax3.axhline(3.73, color=MUTED, ls=":", lw=0.9); ax3.text(1500, 3.95, "corpus mean = 3.73", fontsize=6.2, color=MUTED)
    ax3.set_xlabel("Articles (log scale)"); ax3.set_ylabel("Mean FWCI"); ax3.set_title("Volume vs. impact (countries ≥40 articles)")
    ax3.legend(loc="upper right", fontsize=6.5); panel(ax3, "c")
    STATS["gs_share_top20"] = int(sum(is_gs(c) for c in ct.head(20).iso2))
    save(fig, "Fig09_geography")


if __name__ == "__main__":
    fig_geo()
    write_stats("fig09_geography")
    print("written", FIG_OUT / "Fig09_geography.png")
