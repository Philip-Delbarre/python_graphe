from .dijkstra import *

# test #1 
g = GrapheReseau()

g.add_edge("DC", "R1", cost=4, latency=8, bandwidth=120)
g.add_edge("R1", "Clients", cost=4, latency=8, bandwidth=120)
g.add_edge("DC", "R2", cost=1, latency=25, bandwidth=120)
g.add_edge("R2", "Clients", cost=1, latency=25, bandwidth=120)

latence_min, chemin = g.dijkstra("DC", "Clients", weight="latency")
print(f"Latence minimale : {latence_min} ms")
print(f"Chemin : {' -> '.join(chemin)}")
print("====================================/n")


# second Test
g2 = GrapheReseau()

g2.add_edge("DC", "R4", cost=10, latency=2, bandwidth=120)
g2.add_edge("R4", "Clients", cost=10, latency=2, bandwidth=120)
g2.add_edge("DC", "R5", cost=1, latency=22, bandwidth=120)
g2.add_edge("R5", "Clients", cost=1, latency=22, bandwidth=120)

latence_min_, chemin_ = g2.dijkstra("DC", "Clients", weight="latency")
print(f"Latence minimale : {latence_min_} ms")
print(f"Chemin : {' -> '.join(chemin_)}")



