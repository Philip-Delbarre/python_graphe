import matplotlib.pyplot as plt
import networkx as nx
G = nx.DiGraph()

# Nœuds
G.add_nodes_from(["DC", "R1", "R2", "Clients"])

# Arêtes orientées : (source, cible, {"cost": ..., "latency_ms": ..., "bandwidth": ...})
edges = [
    ("DC", "R1", {"cost": 120, "latency_ms": 8, "bandwidth": 4}),
    ("R1", "Clients", {"cost": 120, "latency_ms": 8, "bandwidth": 4}),
    ("DC", "R2", {"cost": 120, "latency_ms": 25, "bandwidth": 1}),
    ("R2", "Clients", {"cost": 120, "latency_ms": 25, "bandwidth": 1}),
]
G.add_edges_from(edges)

# Vérification des attributs
for u, v, data in G.edges(data=True):
    print(f"{u} -> {v} : {data}")
# Positions fixes pour reproduire la disposition du schéma
pos = {
    "DC": (0.0, 0.5),
    "R1": (1.0, 1.0),
    "R2": (1.0, 0.0),
    "Clients": (2.0, 0.5),
}

fig, ax = plt.subplots(figsize=(8, 3.8))

# Nœuds intermédiaires (cercles R1, R2)
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=["R1", "R2"],
    node_shape="o",
    node_size=1300,
    node_color="#e8eff5",
    edgecolors="#3b6e8c",
    linewidths=1.5,
    ax=ax,
)

# Nœuds extrémités (rectangles DC, Clients)
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=["DC"],
    node_shape="s",
    node_size=2200,
    node_color="#e6e9ec",
    edgecolors="#2f3640",
    linewidths=1.5,
    ax=ax,
)
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=["Clients"],
    node_shape="s",
    node_size=2200,
    node_color="#e8f0ea",
    edgecolors="#3c6e47",
    linewidths=1.5,
    ax=ax,
)

# Labels des nœuds
nx.draw_networkx_labels(
    G,
    pos,
    font_size=11,
    font_weight="bold",
    font_family="serif",
    ax=ax,
)

# Épaisseur proportionnelle au débit (optionnel : ici 2.5 pour débit 4 et 1.2 pour débit 1)
widths = [2.5 if G[u][v]["bandwidth"] >= 4 else 1.2 for u, v in G.edges()]

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=list(G.edges()),
    width=widths,
    edge_color="#6c757d",
    arrows=True,
    arrowsize=16,
    min_source_margin=24,
    min_target_margin=24,
    ax=ax,
)

# Étiquettes d'arêtes formatées comme sur l'image
edge_labels = {
    (u, v): f"{d['cost']} / {d['latency_ms']} ms / {d['bandwidth']}"
    for u, v, d in G.edges(data=True)
}
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    font_size=9,
    font_color="#b07d2b",
    label_pos=0.52,
    bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85),
    ax=ax,
)

ax.set_xlim(-0.35, 2.35)
ax.set_ylim(-0.3, 1.3)
ax.axis("off")
plt.tight_layout()
plt.show()