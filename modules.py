from collections import deque

def construire_graphe_residuel(graphe, flot):
    residuel = {sommet: {} for sommet in graphe}

    for u, voisins in graphe.items():
        for v, capacite in voisins.items():
            flux = flot.get(u, {}).get(v, 0)

            residuel[u][v] = capacite - flux
            residuel.setdefault(v, {})
            residuel[v][u] = residuel[v].get(u, 0) + flux

    return residuel

def reconstruire_arcs(source, puits, parent):
    arcs = []
    sommet = puits

    while sommet != source:
        if sommet not in parent or parent[sommet] is None:
            return None  # Aucun chemin trouvé

        precedent = parent[sommet]
        arcs.append((precedent, sommet))
        sommet = precedent

    arcs.reverse()
    return arcs

def trouver_parents(source, puits, graphe, graphe_residuel):
    parent = {source: None}
    file = deque([source])

    while file:
        sommet = file.popleft()

        if sommet == puits:
            return parent

        for voisin in graphe.get(sommet, {}):
            capacite = graphe_residuel.get(sommet, {}).get(voisin, 0)

            if capacite > 0 and voisin not in parent:
                parent[voisin] = sommet
                file.append(voisin)

    return None  # Aucun chemin résiduel trouvé

