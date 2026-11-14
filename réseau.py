
import networkx as nx
import matplotlib.pyplot as plt 

G = nx.DiGraph()

Graphe = {  
            "DC-A": { "R1": 120, "R2": 100},
            "R1" : {"R3" : 70, "Zonex":40},
            "R2" : {"R3" : 90, "Zonex":30},
            "R3" : {"Zonex": 140 }          
        }

G.add_edge("DC-A", "R1", poids=120) 
G.add_edge("DC-A", "R2", poids=100)
G.add_edge("R1", "R3", poids=70)
G.add_edge("R1", "Zonex", poids=40)
G.add_edge("R2", "R3", poids=90)
G.add_edge("R2", "Zonex", poids=30) 
G.add_edge("R3", "Zonex", poids=140)

'''
positions = nx.spring_layout(G)
nx.draw( G, positions,with_labels=True,node_color="lightblue",node_size=2000, arrows=True, )
nx.draw_networkx_edge_labels(G,positions, edge_labels=nx.get_edge_attributes(G, "poids"), )
plt.show()
'''
def calculer_capacite_maximale(graphe, source):
    capacitéMax = 0
    for key, value in graphe.items():
        if key == source:
            for key2, value2 in value.items():
                capacitéMax += value2
    return capacitéMax

capacitéMax = calculer_capacite_maximale(Graphe, "DC-A")

capacitéMax = 0
for key, value in Graphe.items():
    if key == "DC-A":
        for key2, value2 in value.items():
            capacitéMax += value2
print(f"La capacité maximale du réseau est de {capacitéMax}.")


def constructionArc(graphe, source, destination, capacité):
    if source not in graphe:
        graphe[source] = {}
    graphe[source][destination] = capacité
     

def afficheArc(graphe):

    for key, values in Graphe.items():
        for key2, value2 in values.items():
            print(f"Le lien {key} -> {key2} a une capacité de {value2}.")

#afficheArc(Graphe)

'''

for key, values in Graphe.items():
    for key2, value2 in values.items():
        if value2 > capacitéMax:
            print(f"Le lien {key} -> {key2} a une capacité de {value2} qui dépasse la capacité maximale de {capacitéMax}.")
        elif value2 == capacitéMax:
            print(f"Le lien {key} -> {key2} a une capacité de {value2} qui est égale à la capacité maximale de {capacitéMax}.")     
        elif value2 < capacitéMax:
            print(f"Le lien {key} -> {key2} a une capacité de {value2} qui est inférieure à la capacité maximale de {capacitéMax}.")
        else:
            print(f"Le lien {key} -> {key2} a une capacité de {value2} qui est égale à la capacité maximale de {capacitéMax}.") 
            '''

def successeurs(graphe, sommet):
    return list(graphe.get(sommet, {}).keys())

def predecesseurs(graphe, sommet):
    return [origine for origine, voisins in graphe.items() if sommet in voisins]

print("les successeurs", successeurs(Graphe, "R1"))
# ['R3', 'Zonex']

print("les prédécesseurs", predecesseurs(Graphe, "R3"))    # ['R1', 'R2']

def afficher_capacites_sommet(graphe, sommet):     
      entrants = [         
             (origine, graphe[origine][sommet])         
             for origine in graphe         
             if sommet in graphe[origine]     
      ]     
      sortants = list(graphe.get(sommet, {}).items()) 
      
      print(f"Sommet : {sommet}")     
      print("Arcs entrants :", entrants)     
      print("Arcs sortants :", sortants) 


afficher_capacites_sommet(Graphe, "R1")

def entrants_superieurs_ou_egaux_sortants(graphe, sommet) -> bool:     
    total_entrant = sum(         
            voisins[sommet]         
            for voisins in graphe.values()         
            if sommet in voisins     
      )     
    total_sortant = sum(graphe.get(sommet, {}).values())  
    print(f"Total entrant pour {sommet} : {total_entrant}")     
    print(f"Total sortant pour {sommet} : {total_sortant}") 
    return total_entrant >= total_sortant 

print(entrants_superieurs_ou_egaux_sortants(Graphe, "R3"))


def calculer_chemins_intermediaire(graph, routeur_intermediaire, source='DC-A', dest='Zonex'):
    capaciteMax_ = calculer_capacite_maximale(Graphe, "DC-A")
    dico = {}
    
    def dfs(noeud_actuel, chemin, poids_total):
        if noeud_actuel == dest:
            if routeur_intermediaire in chemin and poids_total <= capaciteMax_:
                dico[tuple(chemin)] = poids_total
            return
        
        if noeud_actuel not in graph:
            return
            
        for voisin, poids in graph[noeud_actuel].items():
            if voisin not in chemin:
                dfs(voisin, chemin + [voisin], poids_total + poids) 
                # fonction récursive pour explorer les voisins du noeud actuel

    dfs(source, [source], 0)
    return dico

# Exemple de définition du graphe basé sur l'image :
print(calculer_chemins_intermediaire(Graphe, 'R3'))


# Exemple d'utilisation pour R1 :
# print(calculer_chemins_intermediaire(graphe, 'R1'))