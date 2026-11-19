from collections import deque
from copy import deepcopy
from modules import construire_graphe_residuel, reconstruire_arcs, trouver_parents

graphe = {  
            "DC-A": { "R1": 120, "R2": 100},
            "R1" : {"R3" : 70, "Zonex":40},
            "R2" : {"R3" : 90, "Zonex":30},
            "R3" : {"Zonex": 140 }          
        }

def capacite_minimale( graphe_residuel, chemin, flot):  
    
    graphe_ = deepcopy(graphe_residuel)
    flot= flot
    capacites = []     
    for i in range(len(chemin) - 1):         
        depart = chemin[i]         
        arrivee = chemin[i + 1]         
        if arrivee not in graphe_.get(depart, {}):             
            raise ValueError(f"Aucune arête de {depart} vers {arrivee}")       
        capacites.append(graphe_residuel[depart][arrivee])     
    if not capacites:         
        raise ValueError("Le chemin doit contenir au moins une arête")     
    return min(capacites)
 



# print(capacite_minimale(Graphe_residuel, ['DC-A', 'R1', 'Zonex'], 10))
# print(capacite_minimale_residuelle(graphe, 'DC-A', 'Zonex'))

def bottleneck (graphe_residuel, chemin):
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



flot = {
    "DC-A": {"R1": 0, "R2": 0},
    "R1": {"R3": 0, "Zonex": 0},
    "R2": {"R3": 0, "Zonex": 0},
    "R3": {"Zonex": 0}
}

Graphe_residuel = construire_graphe_residuel(graphe, flot)
parent_chemin = trouver_parents("DC-A", "Zonex", graphe, Graphe_residuel)
arc_reconstitué = reconstruire_arcs("DC-A", "Zonex", parent_chemin)     

print("les arcs du chemin:", arc_reconstitué)


