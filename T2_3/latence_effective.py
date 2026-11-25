import heapq
from typing import Dict, List, Optional, Tuple


def latency_bpr(l0: float, fe: float, ce: float) -> float:
    """Calcule la latence effective L_e(f) = L_{0,e} * (1 + 0.15 * (f_e / C_e)^4)."""
    if ce <= 0:
        raise ValueError("La capacité C_e doit être strictement positive.")
    return l0 * (1.0 + 0.15 * (fe / ce) ** 4)


class GrapheCongestion:
    """Graphe orienté avec capacité C_e, latence à vide L_{0,e} et flux f_e."""

    def __init__(self) -> None:
        # adj[u][v] = {"capacity": Ce, "l0": L0, "flow": fe}
        self.adj: Dict[str, Dict[str, dict]] = {}

    def add_node(self, node: str) -> None:
        if node not in self.adj:
            self.adj[node] = {}

    def add_edge(self, u: str, v: str, capacity: float, l0: float, flow: float = 0.0) -> None:
        self.add_node(u)
        self.add_node(v)
        self.adj[u][v] = {
            "capacity": capacity,
            "l0": l0,
            "flow": flow,
        }

    def set_flows(self, flows: Dict[Tuple[str, str], float]) -> None:
        """Met à jour le flux f_e sur les arêtes spécifiées."""
        for (u, v), fe in flows.items():
            if u in self.adj and v in self.adj[u]:
                self.adj[u][v]["flow"] = fe
            else:
                raise KeyError(f"Arête inconnue : {u} -> {v}")

    def reset_flows(self, flow: float = 0.0) -> None:
        for u in self.adj:
            for v in self.adj[u]:
                self.adj[u][v]["flow"] = flow

    def edge_effective_latency(self, u: str, v: str) -> float:
        attrs = self.adj[u][v]
        return latency_bpr(attrs["l0"], attrs["flow"], attrs["capacity"])

    def dijkstra_effective_latency(self, start: str, goal: str) -> Tuple[float, List[str]]:
        """Dijkstra sans NetworkX utilisant la latence effective L_e(f_e) comme poids."""
        if start not in self.adj or goal not in self.adj:
            raise ValueError("Nœud de départ ou d'arrivée absent du graphe.")

        dist: Dict[str, float] = {node: float("inf") for node in self.adj}
        prev: Dict[str, Optional[str]] = {node: None for node in self.adj}
        dist[start] = 0.0

        heap: List[Tuple[float, str]] = [(0.0, start)]
        visited = set()

        while heap:
            current_dist, u = heapq.heappop(heap)
            if u in visited:
                continue
            visited.add(u)

            if u == goal:
                break

            for v in self.adj[u]:
                if v in visited:
                    continue
                w = self.edge_effective_latency(u, v)
                new_dist = current_dist + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    heapq.heappush(heap, (new_dist, v))

        if dist[goal] == float("inf"):
            return float("inf"), []

        path: List[str] = []
        curr: Optional[str] = goal
        while curr is not None:
            path.append(curr)
            curr = prev[curr]
        path.reverse()

        return dist[goal], path

    def summary_edges(self) -> None:
        print(f"{'Arête':<18} {'Flux f_e':>8} {'Cap C_e':>8} {'L0':>8} {'L_eff':>10}")
        print("-" * 58)
        for u in self.adj:
            for v, a in self.adj[u].items():
                leff = self.edge_effective_latency(u, v)
                print(f"{u + ' -> ' + v:<18} {a['flow']:>8.1f} {a['capacity']:>8.1f} {a['l0']:>8.1f} {leff:>10.2f}")