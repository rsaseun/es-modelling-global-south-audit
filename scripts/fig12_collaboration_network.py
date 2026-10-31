"""Fig. 12. International co-authorship network.

Reproduces Fig. 12 of "More models, little validation: A quality-screened,
decade-resolved audit of spatially explicit ecosystem-service modelling in the
Global South (1990–2025)" (Ecosystem Services).

Output: outputs/figures/Fig12_collaboration_network.png (600 dpi), .svg (editable) and .pdf (vector).
Run from the repository root:  python scripts/fig12_collaboration_network.py
"""
from _common import *  # noqa: F401,F403  (paths, style, palette, helpers)


def fig_network():
    M = pd.read_csv(f"{R}/collab_matrix.csv", index_col=0)
    names = pd.read_csv(f"{R}/country_totals.csv", keep_default_na=False).set_index("iso2")["name"].to_dict()
    G = nx.Graph()
    for c in M.index: G.add_node(c, size=int(M.loc[c, c]))
    for i, a in enumerate(M.index):
        for b in M.index[i + 1:]:
            w = int(M.loc[a, b])
            if w >= 5: G.add_edge(a, b, weight=w)
    # Salton cosine for layout robustness
    H = nx.Graph(); H.add_nodes_from(G.nodes())
    for u, v, dd in G.edges(data=True): H.add_edge(u, v, distance=1.0 / np.log1p(dd["weight"]))
    pos = nx.kamada_kawai_layout(H, weight="distance")
    pos = nx.spring_layout(G, pos=pos, weight="weight", seed=7, k=1.6, iterations=60)
    deg = dict(G.degree(weight="weight")); btw = nx.betweenness_centrality(G, weight=None)
    comm = nx.community.louvain_communities(G, weight="weight", seed=3)
    cmap_ = {}
    for i, cset in enumerate(sorted(comm, key=lambda s: -sum(M.loc[c, c] for c in s))):
        for c in cset: cmap_[c] = CAT[i % 8]
    fig, ax = plt.subplots(figsize=(7.4, 6.2)); ax.set_axis_off()
    ws = np.array([G[u][v]["weight"] for u, v in G.edges()])
    for (u, v), w in zip(G.edges(), ws):
        x = [pos[u][0], pos[v][0]]; y = [pos[u][1], pos[v][1]]
        gs_link = is_gs(u) and is_gs(v)
        ax.plot(x, y, color=CAT[2] if gs_link else "#9a9994", lw=0.3 + 3.2 * (w / ws.max()) ** 0.6, alpha=0.55 if gs_link else 0.35, zorder=1)
    texts = []
    for n in G.nodes():
        s = G.nodes[n]["size"]
        ax.scatter(*pos[n], s=25 + 1.1 * s ** 0.9, color=cmap_[n], edgecolor="white" if is_gs(n) else INK, linewidth=1.6 if not is_gs(n) else 1.0, zorder=3,
                   marker="o" if is_gs(n) else "s")
        texts.append(ax.text(pos[n][0], pos[n][1], names.get(n, n), fontsize=6.4, ha="center", va="center", color=INK, zorder=5,
                             bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.75)))
    from adjustText import adjust_text
    # adjustText stops after 1 s of wall-clock time by default, which makes label placement machine-dependent.
    # A fixed iteration count (384, the number reached when the published figure was drawn) makes it reproducible.
    adjust_text(texts, ax=ax, expand=(1.3, 1.6), force_text=(0.6, 0.8), arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5),
                iter_lim=384, time_lim=None)
    ax.set_title("International co-authorship network of the 30 most productive countries (edges ≥5 co-authored articles)")
    leg = [Line2D([0], [0], marker="o", color="w", markerfacecolor=MUTED, markersize=7, label="Global South country"),
           Line2D([0], [0], marker="s", color="w", markerfacecolor=MUTED, markeredgecolor=INK, markersize=7, label="Global North country"),
           Line2D([0], [0], color=CAT[2], lw=2, label="South–South link"), Line2D([0], [0], color="#9a9994", lw=2, label="North–South / North–North link")]
    leg += [Patch(color=CAT[i], label=f"Community {i+1}") for i in range(len(comm))]
    ax.legend(handles=leg, loc="lower left", fontsize=6.4, ncol=2)
    STATS["network"] = dict(nodes=G.number_of_nodes(), edges=G.number_of_edges(), density=nx.density(G),
                            communities=[sorted(c) for c in comm], top_strength=sorted(deg.items(), key=lambda x: -x[1])[:10],
                            top_betweenness=sorted(btw.items(), key=lambda x: -x[1])[:8],
                            ss_edges=sum(1 for u, v in G.edges() if is_gs(u) and is_gs(v)),
                            ss_weight=int(sum(G[u][v]["weight"] for u, v in G.edges() if is_gs(u) and is_gs(v))), tot_weight=int(ws.sum()))
    # collaboration rate per country (share of works with each partner) => international share proxy
    save(fig, "Fig12_collaboration_network")


if __name__ == "__main__":
    fig_network()
    write_stats("fig12_collaboration_network")
    print("written", FIG_OUT / "Fig12_collaboration_network.png")
