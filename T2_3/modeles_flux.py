from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class ClasseService:
    nom: str
    exemple: str
    latence_cible: float
    priorite: str
    rang_priorite: int  # 1 = plus haute priorité


CLASSES_SERVICE: Dict[str, ClasseService] = {
    "CONTROL": ClasseService(
        nom="CONTROL",
        exemple="signalisation temps réel",
        latence_cible=20.0,
        priorite="critique",
        rang_priorite=1,
    ),
    "LIVE": ClasseService(
        nom="LIVE",
        exemple="vidéo directe",
        latence_cible=180.0,
        priorite="élevée",
        rang_priorite=2,
    ),
    "VOD": ClasseService(
        nom="VOD",
        exemple="vidéo à la demande",
        latence_cible=220.0,
        priorite="normale",
        rang_priorite=3,
    ),
    "BACKUP": ClasseService(
        nom="BACKUP",
        exemple="réplication",
        latence_cible=300.0,
        priorite="faible",
        rang_priorite=4,
    ),
}


@dataclass
class FluxTagge:
    identifiant: str
    classe: str
    debit: float
    chemin: List[str]
    tags_supp: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.classe not in CLASSES_SERVICE:
            raise ValueError(f"Classe inconnue : {self.classe}")
        if self.debit < 0:
            raise ValueError("Le débit d'un flux doit être positif ou nul.")

    @property
    def arcs(self) -> List[Tuple[str, str]]:
        return list(zip(self.chemin[:-1], self.chemin[1:]))

    @property
    def spec(self) -> ClasseService:
        return CLASSES_SERVICE[self.classe]