import matplotlib.pyplot as plt
import networkx as nx
from flux_congestion import *
from latence_effective import *

def classer_charge(rho: float) -> Tuple[str, str]:
    """Retourne (catégorie, couleur) selon le taux d'utilisation rho = f / C."""
    if rho >= 0.85:
        return "Proche saturation / saturé", "#c0392b"  # Rouge vif
    elif rho >= 0.50:
        return "Chargé", "#e67e22"  # Orange
    else:
        return "Peu chargé", "#27ae60"  # Vert


def dessiner_graphe_congestion(graphe: "GrapheCongestion") -> None:
    metriques = calculer_metriques_arcs(graphe)

    nx_g = nx.DiGraph()
    for u in graphe.adj:
        nx_g.add_node(u)
        for v, m in metriques.items():
            if v[0] == u:
                nx_g.add_edge(u, v[1], **m)

    pos = {
        "DC-A": (0.0, 1.0),
        "DC-B": (0.0, 0.0),
        "R1": (1.0, 1.0),
        "R2": (1.0, 0.0),
        "R3": (2.0, 0.45),
        "LIVE": (3.0, 1.0),
        "BACKUP": (3.0, 0.0),
    }

    edge_list = list(nx_g.edges())
    flows = [metriques[e]["flow"] for e in edge_list]
    rhos = [metriques[e]["rho"] for e in edge_list]

    max_flow = max(flows) if flows and max(flows) > 0 else 1.0

    # Épaisseur : varie avec le débit f, avec un bonus d'épaisseur pour les liens congestionnés
    widths = []
    colors = []
    for f, rho in zip(flows, rhos):
        base_width = 1.5 + 3.5 * (f / max_flow)          # Varie avec le débit
        congestion_bonus = 2.5 if rho >= 0.85 else (1.0 if rho >= 0.50 else 0.0)
        widths.append(base_width + congestion_bonus)

        _, color = classer_charge(rho)
        colors.append(color)

    fig, ax = plt.subplots(figsize=(11, 5.2))

    # Nœuds
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

    # Arêtes : épaisseur + couleur de congestion
    nx.draw_networkx_edges(
        nx_g,
        pos,
        edgelist=edge_list,
        edge_color=colors,
        width=widths,
        arrows=True,
        arrowsize=18,
        min_source_margin=22,
        min_target_margin=22,
        ax=ax,
    )

    # Étiquettes : f/C, rho et latence congestionnée
    edge_labels = {
        (u, v): (
            f"f={m['flow']:.0f}/{m['capacity']:.0f} "
            f"(ρ={m['rho']:.2f}) | L={m['latency_congested']:.1f}"
        )
        for (u, v), m in metriques.items()
    }
    nx.draw_networkx_edge_labels(
        nx_g,
        pos,
        edge_labels=edge_labels,
        font_size=7.5,
        bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.88),
        ax=ax,
    )

    # Légende des niveaux de charge
    legend_handles = [
        plt.Line2D([0], [0], color="#27ae60", lw=3, label="Peu chargé (ρ < 0.50)"),
        plt.Line2D([0], [0], color="#e67e22", lw=4, label="Chargé (0.50 ≤ ρ < 0.85)"),
        plt.Line2D([0], [0], color="#c0392b", lw=6, label="Proche saturation / saturé (ρ ≥ 0.85)"),
    ]
    ax.legend(handles=legend_handles, loc="lower center", ncol=3, frameon=True, fontsize=8.5)

    ax.set_title("Métriques d'une solution : débit (épaisseur), taux d'utilisation ρ (couleur/gras) et latence L")
    ax.set_xlim(-0.4, 3.4)
    ax.set_ylim(-0.4, 1.35)
    ax.axis("off")
    plt.tight_layout()
    plt.show()


# --- Exemple d'utilisation ---
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

g.set_flows({
    ("DC-A", "R1"): 180,     # rho = 0.90 (rouge, très gras)
    ("R1", "LIVE"): 95,      # rho = 0.95 (rouge, très gras)
    ("R1", "R3"): 85,      # rho = 0.53 (orange, moyen)
    ("DC-B", "R2"): 80,      # rho = 0.32 (vert, fin)
    ("R2", "R3"): 50,      # rho = 0.23 (vert, fin)
    ("R2", "BACKUP"): 30,    # rho = 0.30 (vert, fin)
    ("R3", "LIVE"): 135,     # rho = 0.61 (orange, moyen)
    ("R3", "BACKUP"): 0,     # rho = 0.00 (vert, fin)
})

for (u, v), m in calculer_metriques_arcs(g).items():
    cat, _ = classer_charge(m["rho"])
    print(f"{u:<4} -> {v:<6} | f={m['flow']:5.1f} / C={m['capacity']:5.1f} | "
        f"rho={m['rho']:5.2f} | L={m['latency_congested']:6.2f} | {cat}"
        )

dessiner_graphe_congestion(g)