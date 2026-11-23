from latence_effective import *
import matplotlib.pyplot as plt
import networkx as nx


g = GrapheCongestion()

# Arêtes du schéma : (source, cible, capacité Ce, latence à vide L0,e)
edges = [
    ("DC-A", "R1", 200, 5),
    ("DC-B", "R2", 250, 7),
    ("R1", "LIVE", 100, 18),
    ("R1", "R3", 160, 6),
    ("R2", "R3", 220, 12),
    ("R2", "BACKUP", 100, 25),
    ("R3", "LIVE", 220, 8),
    ("R3", "BACKUP", 250, 10),
]

for u, v, ce, l0 in edges:
    g.add_edge(u, v, capacity=ce, l0=l0, flow=0.0)

# 1) À vide (f_e = 0) : L_eff == L0
lat_vide, chemin_vide = g.dijkstra_effective_latency("DC-A", "LIVE")
print(f"À vide (DC-A -> LIVE) : latence = {lat_vide:.2f}, chemin = {' -> '.join(chemin_vide)}\n")

# 2) Exemple avec du trafic (ex. saturation partielle de R1 -> LIVE)
g.set_flows({
    ("DC-A", "R1"): 150,
    ("R1", "LIVE"): 110,   # > capacité 100 -> forte hausse de latence
    ("R1", "R3"): 40,
    ("R3", "LIVE"): 40,
})

g.summary_edges()
lat_charge, chemin_charge = g.dijkstra_effective_latency("DC-A", "LIVE")
print(f"\nEn charge (DC-A -> LIVE) : latence = {lat_charge:.2f}, chemin = {' -> '.join(chemin_charge)}")



nx_g = nx.DiGraph()
for u in g.adj:
    nx_g.add_node(u)
    for v, attrs in g.adj[u].items():
        nx_g.add_edge(
            u,
            v,
            capacity=attrs["capacity"],
            l0=attrs["l0"],
            flow=attrs["flow"],
            leff=g.edge_effective_latency(u, v),
        )

pos = {
    "DC-A": (0.0, 1.0),
    "DC-B": (0.0, 0.0),
    "R1": (1.0, 1.0),
    "R2": (1.0, 0.0),
    "R3": (2.0, 0.45),
    "LIVE": (3.0, 1.0),
    "BACKUP": (3.0, 0.0),
}

fig, ax = plt.subplots(figsize=(10, 4.8))

nx.draw_networkx_nodes(
    nx_g,
    pos,
    nodelist=["R1", "R2", "R3"],
    node_shape="o",
    node_size=1200,
    node_color="#e8eff5",
    edgecolors="#3b6e8c",
    linewidths=1.5,
    ax=ax,
)
nx.draw_networkx_nodes(
    nx_g,
    pos,
    nodelist=["DC-A", "DC-B"],
    node_shape="s",
    node_size=2200,
    node_color="#e6e9ec",
    edgecolors="#2f3640",
    linewidths=1.5,
    ax=ax,
)
nx.draw_networkx_nodes(
    nx_g,
    pos,
    nodelist=["LIVE", "BACKUP"],
    node_shape="s",
    node_size=2200,
    node_color="#e8f0ea",
    edgecolors="#3c6e47",
    linewidths=1.5,
    ax=ax,
)
nx.draw_networkx_labels(nx_g, pos, font_size=10, font_weight="bold", ax=ax)

nx.draw_networkx_edges(
    nx_g,
    pos,
    edge_color="#6c757d",
    width=1.8,
    arrows=True,
    arrowsize=16,
    min_source_margin=22,
    min_target_margin=22,
    ax=ax,
)

edge_labels = {
    (u, v): f"f={d['flow']:.0f} | {d['capacity']:.0f}/{d['l0']:.0f} | L={d['leff']:.1f}"
    for u, v, d in nx_g.edges(data=True)
}
nx.draw_networkx_edge_labels(
    nx_g,
    pos,
    edge_labels=edge_labels,
    font_size=7.5,
    bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85),
    ax=ax,
)

ax.set_xlim(-0.4, 3.4)
ax.set_ylim(-0.35, 1.35)
ax.axis("off")
plt.tight_layout()
plt.show()
