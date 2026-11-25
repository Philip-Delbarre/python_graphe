import matplotlib.pyplot as plt
import networkx as nx

from flux_congestion import calculer_metriques_arcs
from flux_tagge import appliquer_flux_tagges, tagger_flux_automatique
from latence_effective import GrapheCongestion
from modeles_flux import CLASSES_SERVICE

# --- 1. Données d'entrée : graphe + flux taggés ---
g = GrapheCongestion()
for u, v, ce, l0 in [
    ("DC-A", "R1", 200, 5),
    ("DC-B", "R2", 250, 7),
    ("R1", "LIVE", 100, 18),
    ("R1", "R3", 160, 6),
    ("R2", "R3", 220, 12),
    ("R2", "BACKUP", 100, 25),
    ("R3", "LIVE", 220, 8),
    ("R3", "BACKUP", 250, 10),
]:
    g.add_edge(u, v, capacity=ce, l0=l0, flow=0.0)

flux_list = [
    tagger_flux_automatique("F1", debit=20, chemin=["DC-A", "R1", "LIVE"], classe_forcee="LIVE"),
    tagger_flux_automatique("F2", debit=70, chemin=["DC-A", "R1", "R3", "LIVE"], classe_forcee="VOD"),
    tagger_flux_automatique("F3", debit=40, chemin=["DC-B", "R2", "R3", "LIVE"], classe_forcee="CONTROL"),
    tagger_flux_automatique("F4", debit=80, chemin=["DC-B", "R2", "BACKUP"], classe_forcee="BACKUP"),
]

detail_arcs = appliquer_flux_tagges(g, flux_list)
metriques = calculer_metriques_arcs(g)

# --- 2. Construction du graphe NetworkX ---
nx_g = nx.DiGraph()
for u in g.adj:
    nx_g.add_node(u)
    for v in g.adj[u]:
        nx_g.add_edge(u, v, **metriques[(u, v)], **detail_arcs[(u, v)])

pos = {
    "DC-A": (0.0, 1.0),
    "DC-B": (0.0, 0.0),
    "R1": (1.0, 1.0),
    "R2": (1.0, 0.0),
    "R3": (2.0, 0.45),
    "LIVE": (3.0, 1.0),
    "BACKUP": (3.0, 0.0),
}

# --- 3. Mise en forme selon les classes présentes sur chaque arc ---
classes_couleurs = {
    "CONTROL": "#c0392b",  # priorité critique
    "LIVE": "#d68910",     # priorité élevée (surligné sur le tableau)
    "VOD": "#2980b9",      # priorité normale (surligné sur le tableau)
    "BACKUP": "#7f8c8d",   # priorité faible
}

edge_list = list(nx_g.edges())
edge_colors = []
edge_widths = []
edge_labels = {}

max_flow = max((detail_arcs[e]["total"] for e in edge_list), default=1.0) or 1.0

for u, v in edge_list:
    d_arc = detail_arcs[(u, v)]
    m_arc = metriques[(u, v)]

    # Classes présentes sur l'arc (triées par rang de priorité)
    actives = [
        cls
        for cls, spec in sorted(CLASSES_SERVICE.items(), key=lambda item: item[1].rang_priorite)
        if d_arc[cls] > 0
    ]

    # Couleur dominante : priorité sur LIVE/VOD si présents, sinon classe la plus prioritaire
    if "LIVE" in actives:
        color = classes_couleurs["LIVE"]
    elif "VOD" in actives:
        color = classes_couleurs["VOD"]
    elif actives:
        color = classes_couleurs[actives[0]]
    else:
        color = "#bdc3c7"

    edge_colors.append(color)

    # Épaisseur liée au débit total + léger relief si LIVE ou VOD passe dessus
    bonus_focus = 1.2 if ("LIVE" in actives or "VOD" in actives) else 0.0
    width = 1.5 + 3.0 * (d_arc["total"] / max_flow) + bonus_focus
    edge_widths.append(width)

    if actives:
        tags_txt = " + ".join(f"{cls}({d_arc[cls]:.0f})" for cls in actives)
    else:
        tags_txt = "aucune classe"

    edge_labels[(u, v)] = (
        f"[{tags_txt}]\n"
        f"f={m_arc['flow']:.0f}/{m_arc['capacity']:.0f} | L={m_arc['latency_congested']:.1f}"
    )

# --- 4. Dessin du graphe ---
fig, ax = plt.subplots(figsize=(12.5, 6))

nx.draw_networkx_nodes(
    nx_g,
    pos,
    nodelist=["R1", "R2", "R3"],
    node_shape="o",
    node_size=1250,
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
    node_size=2300,
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
    node_size=2300,
    node_color="#e8f0ea",
    edgecolors="#3c6e47",
    linewidths=1.5,
    ax=ax,
)
nx.draw_networkx_labels(nx_g, pos, font_size=10, font_weight="bold", ax=ax)

nx.draw_networkx_edges(
    nx_g,
    pos,
    edgelist=edge_list,
    edge_color=edge_colors,
    width=edge_widths,
    arrows=True,
    arrowsize=18,
    min_source_margin=24,
    min_target_margin=24,
    ax=ax,
)

nx.draw_networkx_edge_labels(
    nx_g,
    pos,
    edge_labels=edge_labels,
    font_size=7.5,
    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#dcdcdc", alpha=0.92),
    ax=ax,
)

# Légende rappelant les classes et cibles du tableau
legend_handles = [
    plt.Line2D([0], [0], color=classes_couleurs["LIVE"], lw=4, label="LIVE (vidéo directe, cible 180, élevée)"),
    plt.Line2D([0], [0], color=classes_couleurs["VOD"], lw=4, label="VOD (vidéo à la demande, cible 220, normale)"),
    plt.Line2D([0], [0], color=classes_couleurs["CONTROL"], lw=3, label="CONTROL (signalisation TR, cible 20, critique)"),
    plt.Line2D([0], [0], color=classes_couleurs["BACKUP"], lw=3, label="BACKUP (réplication, cible 300, faible)"),
]
ax.legend(handles=legend_handles, loc="lower center", ncol=2, frameon=True, fontsize=8.5)

ax.set_title("Classes de service et flux sur le graphe (LIVE et VOD mis en avant)")
ax.set_xlim(-0.4, 3.4)
ax.set_ylim(-0.48, 1.35)
ax.axis("off")
plt.tight_layout()
plt.show()