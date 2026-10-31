"""Fig. 7. ES categories by country of authorship (activity index).

Reproduces Fig. 7 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

Output: outputs/figures/Fig07_ES_country_activity_index.png (600 dpi), .svg (editable) and .pdf (vector).
Run from the repository root:  python scripts/fig07_es_country_activity_index.py
"""
from _common import *  # noqa: F401,F403  (paths, style, palette, helpers)


def fig_service_country():
    d = pd.read_csv(f"{R}/services_country.csv").set_index("service")
    tot_c = pd.read_csv(f"{R}/country_totals.csv", keep_default_na=False).set_index("iso2")["count"]
    tot_s = {"Crop/food production": 768, "Water yield/provision": 1209, "Habitat quality/biodiversity": 2452, "Nutrient cycling/retention": 339,
             "Soil conservation/erosion": 999, "Carbon storage/sequestration": 1536, "Urban heat/cooling": 112, "Marine & coastal": 1111}
    N = 7972
    ai = d.copy().astype(float)
    for c in d.columns:
        for s in d.index:
            ai.loc[s, c] = (d.loc[s, c] / tot_c[c]) / (tot_s[s] / N)
    share = d.div([tot_c[c] for c in d.columns], axis=1) * 100
    names = {"CN": "China", "BR": "Brazil", "IN": "India", "ZA": "S. Africa", "ET": "Ethiopia", "KE": "Kenya", "MX": "Mexico", "ID": "Indonesia", "US": "USA", "GB": "UK"}
    div = mcolors.LinearSegmentedColormap.from_list("div", ["#c2410c", "#f2a56f", "#efefec", "#7fb0ea", "#123f7a"])
    norm = mcolors.TwoSlopeNorm(vmin=0, vcenter=1, vmax=2.5)
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    im = ax.imshow(ai.values.clip(0, 2.5), cmap=div, norm=norm, aspect="auto")
    for i in range(ai.shape[0]):
        for j in range(ai.shape[1]):
            v = ai.values[i, j]
            ax.text(j, i, f"{v:.2f}\n({int(d.values[i, j])})", ha="center", va="center", fontsize=6.2,
                    color="white" if (v > 1.9 or v < 0.35) else INK)
    ax.set_xticks(range(len(d.columns))); ax.set_xticklabels([names[c] for c in d.columns])
    ax.set_yticks(range(len(d.index))); ax.set_yticklabels(d.index)
    ax.grid(False)
    for s_ in ax.spines.values(): s_.set_visible(False)
    ax.axvline(7.5, color="white", lw=3)
    ax.text(3.5, -0.85, "Global South authorship", ha="center", fontsize=7.5, color=INK2, fontweight="bold")
    ax.text(8.5, -0.85, "Global North", ha="center", fontsize=7.5, color=INK2, fontweight="bold")
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02); cb.set_label("Activity index (1 = corpus average)", fontsize=7)
    ax.set_title("Thematic specialisation of national ES research (activity index; article counts in brackets)", pad=18)
    STATS["activity_index"] = ai.round(2).to_dict(); STATS["service_share_country"] = share.round(1).to_dict()
    save(fig, "Fig07_ES_country_activity_index")


if __name__ == "__main__":
    fig_service_country()
    write_stats("fig07_es_country_activity_index")
    print("written", FIG_OUT / "Fig07_ES_country_activity_index.png")
