from collections import deque
from copy import deepcopy
from modules_ import ( 
    construire_graphe_residuel, 
    trouver_parents, 
    reconstruire_arcs,
    reconstruire_sommets, 
    bottleneck)

graphe = {  
            "DC-A": { "R1": 120, "R2": 100},
            "R1" : {"R3" : 70, "Zonex":40},
            "R2" : {"R3" : 90, "Zonex":30},
            "R3" : {"Zonex": 140 }          
        }


# print(capacite_minimale(Graphe_residuel, ['DC-A', 'R1', 'Zonex'], 10))
# print(capacite_minimale_residuelle(graphe, 'DC-A', 'Zonex'))

# retourne la plus petite capacite residuelle du chemin passé en paramètre.
print(bottleneck(graphe, ['DC-A', 'R1','R3', 'Zonex']))



#  le dico "parent" est un dictionnaire qui associe chaque sommet
#  à son prédécesseur dans le chemin trouvé par l'algorithme de recherche en largeur (BFS).
#  La fonction reconstruire_arcs utilise ce dictionnaire pour reconstruire le chemin complet depuis la source jusqu'au puits, en ajoutant chaque arc (prédécesseur, sommet) à une liste. Enfin, la liste des arcs est inversée pour obtenir l'ordre correct du chemin.
parent = {
    "R1": "DC-A",
    "R3": "R1",
    "Zonex": "R3"
}

value= 40
flot = {
    "DC-A": {"R1": value, "R2": value},
    "R1": {"R3": value, "Zonex": value},
    "R2": {"R3": value, "Zonex": value},
    "R3": {"Zonex": value}
}

Graphe_residuel = construire_graphe_residuel(graphe, flot)
parent_chemin = trouver_parents("DC-A", "Zonex", graphe, Graphe_residuel)
print("le dico parent du chemin trouvé:", parent_chemin)
# ________________

sommets_chemin = reconstruire_sommets("DC-A", "Zonex", parent_chemin)
print("les sommets du chemin:", sommets_chemin)

# ==========================================================
bottleneck_value = bottleneck(Graphe_residuel, sommets_chemin)
print("la plus petite capacité résiduelle du chemin est:", bottleneck_value)


def executer_edmonds_karp(graphe, source, puits):
    """Calcule le flot maximal en réutilisant les fonctions de modules_.py."""
    flot = {u: {v: 0 for v in voisins} for u, voisins in graphe.items()}
    valeur_totale = 0

    while True:
        residuel = construire_graphe_residuel(graphe, flot)
        parent = trouver_parents(source, puits, graphe, residuel)
        if parent is None:
            break

        chemin = reconstruire_sommets(source, puits, parent)
        arcs = reconstruire_arcs(source, puits, parent)
        if not chemin or not arcs:
            break

        delta = bottleneck(residuel, chemin)

        for u, v in arcs:
            if v in flot.get(u, {}):
                flot[u][v] += delta
            else:
                # Arc inverse emprunté : on diminue le flot existant sur (v -> u)
                flot[v][u] -= delta

        valeur_totale += delta

    residuel_final = construire_graphe_residuel(graphe, flot)
    return valeur_totale, flot, residuel_final


print("\n=== Usge de l'algorithme d'Edmonds-Karp ===")
valeur_maximale, flot_final, graphe_residuel_final = executer_edmonds_karp(graphe, "DC-A", "Zonex")
print("Valeur maximale du flot:", valeur_maximale)      
print("Flot final:", flot_final)
print("graphe residuel final: " , graphe_residuel_final)






