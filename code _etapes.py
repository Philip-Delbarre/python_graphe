from collections import defaultdict, deque

def initialiser_residuel(graphe):
    residuel = defaultdict(dict)

    for u, voisins in graphe.items():
        for v, capacite in voisins.items():
            residuel[u][v] = capacite
            residuel[v].setdefault(u, 0)  # arc inverse

    return residuel


def bfs_residual(residuel, source, puits):
    parent = {source: None}
    file = deque([source])

    while file:
        u = file.popleft()

        for v, capacite in residuel[u].items():
            if capacite > 0 and v not in parent:
                parent[v] = u
                if v == puits:
                    return parent
                file.append(v)

    return None


def reconstruire_chemin(parent, source, puits):
    chemin = []
    v = puits

    while v != source:
        u = parent[v]
        chemin.append((u, v))
        v = u

    return list(reversed(chemin))


def capacite_minimale(chemin, residuel):
    return min(residuel[u][v] for u, v in chemin)


def augmenter_flot(residuel, chemin, quantite):
    for u, v in chemin:
        residuel[u][v] -= quantite
        residuel[v][u] += quantite


def flot_maximal(graphe, source, puits):
    residuel = initialiser_residuel(graphe)
    valeur_flot = 0

    while True:
        parent = bfs_residual(residuel, source, puits)
        if parent is None:
            break

        chemin = reconstruire_chemin(parent, source, puits)
        quantite = capacite_minimale(chemin, residuel)
        augmenter_flot(residuel, chemin, quantite)
        valeur_flot += quantite

        print(f"Chemin : {chemin} ; augmentation : {quantite} Mbit/s")

    return valeur_flot, residuel

Graphe = {
    "DC-A": {"R1": 120, "R2": 100},
    "R1": {"R3": 70, "Zonex": 40},
    "R2": {"R3": 90, "Zonex": 30},
    "R3": {"Zonex": 140}
}

valeur, residuel_final = flot_maximal(Graphe, "DC-A", "Zonex")
print("Flot maximal :", valeur, "Mbit/s")