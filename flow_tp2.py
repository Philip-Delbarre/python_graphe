from copy import deepcopy
from modules_ import edmonds_karp, coupe_minimale


def construire_graphe_tp1_principal():
    """
    Partie 2.4 - Étape 5 :
    Super-source S* -> DC Lille (420), DC Paris (650)
    Zones -> Super-puits T* : Nord (250), IDF (430), Est (280)
    """
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

# fonction appellée par l'étape 6 de la deuxieme partie du Tp
# on rajoute 100 sur chacune des arretes pour tester si la capité 
# est encore bonne !
# ________________________________________________ 
def renforcer_arete(graphe, u, v, ajout=100):
    copie = deepcopy(graphe)
    if u in copie and v in copie[u]:
        copie[u][v] += ajout
    return copie



graphe_tp1 = construire_graphe_tp1_principal()

# Étape 5 : Calcul du flot maximal via S* -> T*
flot_max, flot, residuel = edmonds_karp(graphe_tp1, "S*", "T*")
print(f"=== Partie 2.4 (Étape 5) : Flot maximal = {flot_max} Mbit/s ===")

print("\nTrafic servi par zone (vers T*) :")
for zone in ["Nord", "IDF", "Est"]:
    demande = graphe_tp1[zone]["T*"]
    servi = flot[zone]["T*"]
    print(f"  {zone:4s} : {servi}/{demande} Mbit/s")

print("\nArcs saturés (f == c) :")
for u, voisins in graphe_tp1.items():
    for v, cap in voisins.items():
        f = flot[u][v]
        if f == cap:
            print(f"  {u} -> {v} : {f}/{cap}")

# Étape 6 : Coupe minimale (A, B)
A, B, arcs_coupe, cap_coupe = coupe_minimale(graphe_tp1, residuel, "S*")
print("\n=== Partie 2.5 (Étape 6) : Coupe minimale ===")
print("A (accessible depuis S*) :", sorted(A))
print("B (non accessible)        :", sorted(B))
print("Arcs de la coupe (u in A, v in B) :", arcs_coupe)
print(f"Capacité de la coupe = {cap_coupe} Mbit/s (doit égaler flot_max = {flot_max})")

# Réflexion d'ingénieur : +100 Mbit/s sur différentes liaisons
print("\n=== Partie 2.5 : Test de renforcement (+100 Mbit/s) ===")
tests = [
    ("DC Paris", "PAR"),
    ("LIL", "Nord"),
    ("REI", "IDF"),
]
for u, v in tests:
    g_test = renforcer_arete(graphe_tp1, u, v, ajout=100)
    f_test, _, _ = edmonds_karp(g_test, "S*", "T*")
    print(f"  +100 sur {u} -> {v} : nouveau flot max = {f_test} (gain = {f_test - flot_max:+d} Mbit/s)")
