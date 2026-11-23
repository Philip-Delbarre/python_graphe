import networkx as nx
import matplotlib.pyplot as plt

def construire_graphe_tp1_principal():
    return {
        "S*": {"DC Lille": 420, "DC Paris": 650},
        "DC Lille": {"LIL": 350, "ROU": 220},
        "DC Paris": {"ROU": 250, "PAR": 500},
        "LIL": {"ROU": 240, "Nord": 160},
        "ROU": {"PAR": 280, "REI": 180},
        "PAR": {"REI": 320, "IDF": 400},
        "REI": {"IDF": 100, "Est": 260},
        "Nord": {"T*": 250},
        "IDF": {"T*": 430},
        "Est": {"T*": 280},
        "T*": {},
    }

graphe_tp1 = construire_graphe_tp1_principal()

# Construire le graphe orienté
G = nx.DiGraph()

for origine, destinations in graphe_tp1.items():
    for destination, capacite in destinations.items():
        G.add_edge(origine, destination, capacite=capacite)

# Disposition des nœuds
pos = nx.spring_layout(G, seed=42)

# Afficher le graphe
plt.figure(figsize=(12, 8))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=2200,
    node_color="lightblue",
    font_size=9,
    font_weight="bold",
    arrows=True,
    arrowsize=20,
)

# Afficher les capacités sur les arcs
labels = nx.get_edge_attributes(G, "capacite")
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=labels,
    font_size=9,
)

plt.title("Graphe de transport avec capacités")
plt.axis("off")
plt.tight_layout()
plt.show()

