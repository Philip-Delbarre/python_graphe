# Ce module est la dernière version qui permet de répondre à toutes les questions du TP 1
# _____________________________________

from collections import deque


def construire_graphe_residuel(graphe, flot):
    residuel = {sommet: {} for sommet in graphe}
    for u, voisins in graphe.items():
        for v, capacite in voisins.items():
            flux = flot.get(u, {}).get(v, 0)
            residuel.setdefault(v, {})
            residuel[u][v] = capacite - flux
            residuel[v][u] = residuel[v].get(u, 0) + flux
    return residuel

# reconstruit le tableau des arcs
# depuis la sorurce vers le puit


def reconstruire_arcs(source, puits, parent):
    arcs = []
    sommet = puits
    while sommet != source:
        if sommet not in parent or parent[sommet] is None:
            return None
        precedent = parent[sommet]
        arcs.append((precedent, sommet))
        sommet = precedent
    arcs.reverse()
    return arcs


def reconstruire_sommets(source, puits, parent):
    chemin = []
    sommet = puits
    while sommet != source:
        if sommet not in parent or parent[sommet] is None:
            return None
        chemin.append(sommet)
        sommet = parent[sommet]
    chemin.append(source)
    chemin.reverse()
    return chemin


def bottleneck(graphe_residuel, chemin):
    if len(chemin) < 2:
        raise ValueError("Le chemin doit contenir au moins deux sommets.")

    capacites = []
    for depart, arrivee in zip(chemin, chemin[1:]):
        capacite = graphe_residuel.get(depart, {}).get(arrivee)
        if capacite is None or capacite <= 0:
            raise ValueError(
                f"Aucune capacité résiduelle positive pour {depart} -> {arrivee}"
            )
        capacites.append(capacite)
    return min(capacites)


def trouver_parents(source, puits, graphe, graphe_residuel):
    """BFS sur le graphe résiduel (arcs directs et inverses) avec capacité > 0."""
    parent = {source: None}
    file = deque([source])

    while file:
        sommet = file.popleft()
        if sommet == puits:
            return parent

        for voisin, capacite in graphe_residuel.get(sommet, {}).items():
            if capacite > 0 and voisin not in parent:
                parent[voisin] = sommet
                file.append(voisin)

    return None


def edmonds_karp(graphe, source, puits):
    """Calcule le flot maximal et retourne (valeur_totale, flot, graphe_residuel)."""
    flot = {u: {v: 0 for v in voisins} for u, voisins in graphe.items()}
    valeur_totale = 0

    while True:
        residuel = construire_graphe_residuel(graphe, flot)
        parent = trouver_parents(source, puits, graphe, residuel)
        if parent is None:
            break

        chemin = reconstruire_sommets(source, puits, parent)
        delta = bottleneck(residuel, chemin)

        for u, v in zip(chemin, chemin[1:]):
            if v in flot.get(u, {}):
                flot[u][v] += delta
            else:
                # Arc inverse emprunté : on réduit le flot sur l'arc direct (v -> u)
                flot[v][u] -= delta

        valeur_totale += delta

    residuel_final = construire_graphe_residuel(graphe, flot)
    return valeur_totale, flot, residuel_final


def sommets_accessibles_residuel(source, graphe_residuel):
    """Étape 6 : sommets accessibles depuis source dans le graphe résiduel."""
    visites = {source}
    file = deque([source])

    while file:
        u = file.popleft()
        for v, cap_res in graphe_residuel.get(u, {}).items():
            if cap_res > 0 and v not in visites:
                visites.add(v)
                file.append(v)

    return visites


def coupe_minimale(graphe, graphe_residuel, source):
    """Retourne (A, B, arcs_coupe, capacite_coupe) pour le graphe original."""
    A = sommets_accessibles_residuel(source, graphe_residuel)
    tous_sommets = set(graphe.keys()) | {
        v for voisins in graphe.values() for v in voisins
    }
    B = tous_sommets - A

    arcs_coupe = []
    capacite_coupe = 0
    for u, voisins in graphe.items():
        for v, cap in voisins.items():
            if u in A and v in B:
                arcs_coupe.append((u, v, cap))
                capacite_coupe += cap

    return A, B, arcs_coupe, capacite_coupe
