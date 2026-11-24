from typing import Dict, List, Optional, Tuple

from latence_effective import GrapheCongestion
from modeles_flux import CLASSES_SERVICE, FluxTagge


def tagger_flux_automatique(
    identifiant: str,
    debit: float,
    chemin: List[str],
    latence_chemin: Optional[float] = None,
    classe_forcee: Optional[str] = None,
) -> FluxTagge:
    """
    Assigne une classe et des tags contextuels à un flux.
    Si `classe_forcee` n'est pas fournie, déduit une classe par défaut
    à partir de la destination finale (ex. LIVE -> LIVE, BACKUP -> BACKUP).
    """
    destination = chemin[-1] if chemin else ""

    if classe_forcee is not None:
        classe = classe_forcee
    elif destination == "LIVE":
        classe = "LIVE"
    elif destination == "BACKUP":
        classe = "BACKUP"
    else:
        classe = "VOD"

    spec = CLASSES_SERVICE[classe]
    tags: List[str] = [f"dst:{destination}"]

    if debit >= 150:
        tags.append("gros-debit")

    if latence_chemin is not None:
        if latence_chemin > spec.latence_cible:
            tags.append("sla-latence-depasse")
        else:
            tags.append("sla-ok")

    return FluxTagge(
        identifiant=identifiant,
        classe=classe,
        debit=debit,
        chemin=chemin,
        tags_supp=tags,
    )


def appliquer_flux_tagges(
    graphe: GrapheCongestion,
    flux_list: List[FluxTagge],
) -> Dict[Tuple[str, str], Dict[str, float]]:
    graphe.reset_flows(0.0)

    detail_arcs: Dict[Tuple[str, str], Dict[str, float]] = {
        (u, v): {"total": 0.0, "CONTROL": 0.0, "LIVE": 0.0, "VOD": 0.0, "BACKUP": 0.0}
        for u, voisins in graphe.adj.items()
        for v in voisins
    }

    for flux in flux_list:
        for u, v in flux.arcs:
            if u not in graphe.adj or v not in graphe.adj[u]:
                raise KeyError(f"Arc inexistant dans le graphe : {u} -> {v}")
            graphe.adj[u][v]["flow"] += flux.debit
            detail_arcs[(u, v)]["total"] += flux.debit
            detail_arcs[(u, v)][flux.classe] += flux.debit

    return detail_arcs