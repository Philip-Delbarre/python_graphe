import heapq
from typing import Dict, List, Optional, Tuple


class GrapheReseau:
    """Structure de graphe orienté pondéré sans dépendance à NetworkX."""

    def __init__(self) -> None:
        # adj[u][v] = {"cost": ..., "latency": ..., "bandwidth": ...}
        self.adj: Dict[str, Dict[str, dict]] = {}

    def add_node(self, node: str) -> None:
        if node not in self.adj:
            self.adj[node] = {}

    def add_edge(self, u: str, v: str, cost: float, latency: float, bandwidth: float) -> None:
        self.add_node(u)
        self.add_node(v)
        self.adj[u][v] = {
            "cost": cost,
            "latency": latency,
            "bandwidth": bandwidth,
        }

    def dijkstra(
        self,
        start: str,
        goal: str,
        weight: str = "latency",
    ) -> Tuple[float, List[str]]:
        """
        Retourne (distance_minimale, chemin) entre `start` et `goal`
        en utilisant `weight` (par défaut 'latency') comme poids d'arête.
        """
        if start not in self.adj or goal not in self.adj:
            raise ValueError("Le nœud de départ ou d'arrivée est absent du graphe.")

        distances: Dict[str, float] = {node: float("inf") for node in self.adj}
        predecessors: Dict[str, Optional[str]] = {node: None for node in self.adj}
        distances[start] = 0.0

        # File de priorité : (distance_accumulée, nœud_courant)
        heap: List[Tuple[float, str]] = [(0.0, start)]
        visited = set()

        while heap:
            current_dist, u = heapq.heappop(heap)

            if u in visited:
                continue
            visited.add(u)

            if u == goal:
                break

            for v, attrs in self.adj[u].items():
                if v in visited:
                    continue
                edge_weight = attrs[weight]
                if edge_weight < 0:
                    raise ValueError("Dijkstra requiert des poids positifs ou nuls.")

                new_dist = current_dist + edge_weight
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    predecessors[v] = u
                    heapq.heappush(heap, (new_dist, v))

        if distances[goal] == float("inf"):
            return float("inf"), []

        # Reconstruction du chemin depuis `goal` jusqu'à `start`
        path: List[str] = []
        curr: Optional[str] = goal
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        path.reverse()

        return distances[goal], path