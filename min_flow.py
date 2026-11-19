from collections import deque
from copy import deepcopy
from modules import construire_graphe_residuel, reconstruire_arcs, trouver_parents, reconstruire_sommets, bottleneck

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

# Flot partiel valide : 20 via R1->Zonex et 30 via R2->Zonex (total = 50)
flot_valide = {
    "DC-A": {"R1": 20, "R2": 30},
    "R1": {"R3": 0, "Zonex": 20},
    "R2": {"R3": 0, "Zonex": 30},
    "R3": {"Zonex": 0},
    "Zonex": {},
}

residuel = construire_graphe_residuel(graphe, flot_valide)
parents = trouver_parents("DC-A", "Zonex", graphe, residuel)
chemin_sommets = reconstruire_sommets("DC-A", "Zonex", parents)
chemin_arcs = reconstruire_arcs("DC-A", "Zonex", parents)
cap_min = bottleneck(residuel, chemin_sommets)

print("Parents BFS :", parents)
print("Chemin sommets :", chemin_sommets)
print("Chemin arcs :", chemin_arcs)
print("Bottleneck résiduel :", cap_min)

