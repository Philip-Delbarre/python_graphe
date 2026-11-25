from flux_congestion import calculer_metriques_arcs
from flux_tagge import appliquer_flux_tagges, tagger_flux_automatique
from latence_effective import GrapheCongestion

# 1. Construction du graphe de l'énoncé
g = GrapheCongestion()
for u, v, ce, l0 in [
    ("DC-A", "R1", 200, 5),
    ("DC-B", "R2", 250, 7),
    ("R1", "LIVE", 100, 18),
    ("R1", "R3", 160, 6),
    ("R2", "R3", 220, 12),
    ("R2", "BACKUP", 100, 25),
    ("R3", "LIVE", 220, 8),
    ("R3", "BACKUP", 250, 10),
]:
    g.add_edge(u, v, capacity=ce, l0=l0, flow=0.0)

# 2. Création et tagging de plusieurs flux
flux_list = [
    tagger_flux_automatique("F1", debit=80, chemin=["DC-A", "R1", "LIVE"], classe_forcee="LIVE"),
    tagger_flux_automatique("F2", debit=60, chemin=["DC-A", "R1", "R3", "LIVE"], classe_forcee="VOD"),
    tagger_flux_automatique("F3", debit=15, chemin=["DC-B", "R2", "R3", "LIVE"], classe_forcee="CONTROL"),
    tagger_flux_automatique("F4", debit=50, chemin=["DC-B", "R2", "BACKUP"], classe_forcee="BACKUP"),
]

detail_arcs = appliquer_flux_tagges(g, flux_list)
metriques = calculer_metriques_arcs(g)

# 3. Affichage console des flux taggés et vérification de la latence sur chaque chemin
print("=== FLUX TAGGES ===")
for f in flux_list:
    lat_totale = sum(g.edge_effective_latency(u, v) for u, v in f.arcs)
    statut_sla = "OK" if lat_totale <= f.spec.latence_cible else "DEPASSEMENT"
    print(
        f"{f.identifiant} | debit={f.debit:5.1f} | chemin={' -> '.join(f.chemin)} | "
        f"lat={lat_totale:5.2f} / cible={f.spec.latence_cible:5.1f} ({statut_sla})"
    )