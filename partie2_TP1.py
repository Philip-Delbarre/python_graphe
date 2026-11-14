from collections import deque
import copy

graphe = {  
            "DC-A": { "R1": 120, "R2": 100},
            "R1" : {"R3" : 70, "Zonex":40},
            "R2" : {"R3" : 90, "Zonex":30},
            "R3" : {"Zonex": 140 }          
        }

def bfs_residual(graph, source, sink, residual):
    """Retourne le dictionnaire des predecesseurs, ou None si aucun chemin."""
    parent = {}
    queue = deque([source])
    visited = {source}
    
    while queue:
        u = queue.popleft()
        if u == sink:
            break
        for v in residual.get(u, {}):
            if v not in visited and residual[u][v] > 0:
                visited.add(v)
                parent[v] = u
                queue.append(v)
                
    return parent if sink in visited else None

def reconstruct_path(parent, source, sink):
    """Reconstruit la liste des arcs du chemin."""
    path = []
    current = sink
    while current != source:
        prev = parent[current]
        path.append((prev, current))
        current = prev
    path.reverse()
    return path

def bottleneck(path, residual):
    """Retourne la plus petite capacite residuelle du chemin."""
    return min(residual[u][v] for u, v in path)




# Copie du graphe initial
residual = copy.deepcopy(graphe)

graphe2 = {  
            "DC-A": { "R1": 20, "R2": 30},
            "R1" : {"R3" : 6, "Zonex":20},
            "R2" : {"R3" : 9, "Zonex":10},
            "R3" : {"Zonex": 14 }          
        }
# Test de la fonction
parent = bfs_residual(graphe, 'DC-A', 'Zonex', graphe2)
print(parent)


# print(reconstruct_path({"R3" : {"Zonex": 140 } }, 'DC-A', 'Zonex'))

# usage d'un graphe résiduel par incrémentation de 20 sur chaque arc du graphe initial
#  
DCA = { "R1": 35, "R2": 30}
R1 = {"R3" : 15, "Zonex":5}
R2 = {"R3" : 25, "Zonex":5}    
R3 = {"Zonex": 40 }
masterDict = {"DC-A": dict(DCA), "R1": dict(R1), "R2": dict(R2), "R3": dict(R3)}

# La masterDict est le graphe initial avec des capacités de départ proportionelle 
# à la réalité à atteindred ...  en incrémentant chaque arc de 20 on testera la fonction
# bfs_residual avec handleResiduel pour voir si elle fonctionne correctement.

'''
dicoCible = {}
for key, values in masterDict.items():
    t={}
    #print(key, values)
    for key2, value2 in values.items():
        print(key2, value2)
        t[key2]=  value2 + 20
    dicoCible[key] = t

print("dicoCible: " + str(dicoCible))
'''

def handleResiduel(increments, master):
    masterDict = copy.deepcopy(master)
    dicoCible = {
    key: {key2: value2 + increments for key2, value2 in values.items()}
    for key, values in masterDict.items()  }
    return dicoCible

# print("residuel: " + str(handleResiduel(20, master)))

residual = handleResiduel(20, masterDict)

bfs_result = bfs_residual(masterDict, 'DC-A', 'Zonex', residual)
if bfs_result:
    path = reconstruct_path(bfs_result, 'DC-A', 'Zonex')
    print("Chemin trouvé:", path)
    print("Bottleneck:", bottleneck(path, residual))    
else:
    print("Aucun chemin trouvé.")
print("Résultat après incrémentation du graphe résiduel de 20:", residual)









