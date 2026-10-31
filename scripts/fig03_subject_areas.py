"""Fig. 3. Emergence and advancement of subject areas.

Reproduces Fig. 3 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

Output: outputs/figures/Fig03_subject_areas.png (600 dpi), .svg (editable) and .pdf (vector).
Run from the repository root:  python scripts/fig03_subject_areas.py
"""
from _common import *  # noqa: F401,F403  (paths, style, palette, helpers)


def fig_subjects():
    d = pd.read_csv(f"{R}/year_subfield.csv").rename(columns={"level0": "year", "level1": "subfield"})
    d["year"] = d.year.astype(int)
    tot = d.groupby("subfield")["count"].sum().sort_values(ascending=False)
    top = tot.index[:7].tolist()
    d["grp"] = np.where(d.subfield.isin(top), d.subfield, "Other subfields")
    d["dec"] = d.year.apply(dec_of)
    pv = d.pivot_table(index="dec", columns="grp", values="count", aggfunc="sum").reindex([x[2] for x in DECADES]).fillna(0)
    pv = pv[top + ["Other subfields"]]
    sh = pv.div(pv.sum(1), axis=0) * 100
    STATS["subfield_share_by_decade"] = sh.round(1).to_dict()
    STATS["subfield_totals"] = tot.head(15).to_dict()
    fig = plt.figure(figsize=(7.2, 6.4))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.35], hspace=0.75)
    ax = fig.add_subplot(gs[0])
    cols = CAT[:7] + ["#b9b8b3"]
    left = np.zeros(len(sh))
    for i, c in enumerate(sh.columns):
        ax.barh(range(len(sh)), sh[c].values, left=left, color=cols[i], edgecolor="white", linewidth=1.2, height=0.66, label=c)
        for j, v in enumerate(sh[c].values):
            if v >= 6: ax.text(left[j] + v / 2, j, f"{v:.0f}", ha="center", va="center", fontsize=6.8, color="white", fontweight="bold")
        left += sh[c].values
    ax.set_yticks(range(len(sh))); ax.set_yticklabels([f"{i}  (n={int(pv.loc[i].sum()):,})" for i in sh.index]); ax.invert_yaxis()
    ax.set_xlim(0, 100); ax.set_xlabel("Share of decade output (%)"); ax.grid(axis="y", visible=False)
    ax.set_title("Primary subfield composition by decade")
    ax.legend(ncol=4, loc="upper left", bbox_to_anchor=(-0.25, -0.30), fontsize=6.6, handlelength=1, columnspacing=0.9)
    panel(ax, "a")
    ax = fig.add_subplot(gs[1])
    top12 = tot.index[:12].tolist()
    hm = d[d.subfield.isin(top12) & (d.year >= 2000)].pivot_table(index="subfield", columns="year", values="count", aggfunc="sum").reindex(top12).fillna(0)
    im = ax.imshow(np.log10(hm.values + 1), aspect="auto", cmap=SEQ, vmin=0, vmax=np.log10(hm.values.max() + 1))
    ax.set_yticks(range(len(hm))); ax.set_yticklabels([f"{s} ({int(tot[s]):,})" for s in hm.index], fontsize=7)
    ax.set_xticks(range(0, len(hm.columns), 5)); ax.set_xticklabels(hm.columns[::5]); ax.grid(False)
    for s in ax.spines.values(): s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01); cb.set_label("Articles (log₁₀ scale)", fontsize=7)
    cb.set_ticks([0, 1, 2, np.log10(hm.values.max() + 1)]); cb.set_ticklabels(["0", "9", "99", f"{int(hm.values.max())}"])
    ax.set_title("Annual emergence of the 12 leading subfields (2000–2025)"); panel(ax, "b")
    save(fig, "Fig03_subject_areas")


if __name__ == "__main__":
    fig_subjects()
    write_stats("fig03_subject_areas")
    print("written", FIG_OUT / "Fig03_subject_areas.png")
