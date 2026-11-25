from typing import Dict, Tuple
from latence_effective import GrapheCongestion

def calculer_metriques_arcs(
    graphe: "GrapheCongestion",
) -> Dict[Tuple[str, str], Dict[str, float]]:
    """
    Calcule pour chaque arc (u, v) :
    - flow (f)
    - capacity (C)
    - rho (f / C)
    - l0 (latence à vide)
    - latency_congested (latence congestionnée BPR)
    """
    metriques: Dict[Tuple[str, str], Dict[str, float]] = {}

    for u, voisins in graphe.adj.items():
        for v, attrs in voisins.items():
            f = attrs["flow"]
            c = attrs["capacity"]
            l0 = attrs["l0"]

            if c <= 0:
                raise ValueError(f"Capacité invalide sur {u} -> {v} : {c}")

            rho = f / c
            l_cong = l0 * (1.0 + 0.15 * (rho ** 4))

            metriques[(u, v)] = {
                "flow": f,
                "capacity": c,
                "rho": rho,
                "l0": l0,
                "latency_congested": l_cong,
            }

    return metriques
