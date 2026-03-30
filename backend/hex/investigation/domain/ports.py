from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class NewClue:
    clue: str
    score: int = 5


@dataclass
class ClassifyResult:
    type: str  # "scout" | "entity" | "unknown"
    new_clues: list = field(default_factory=list)  # list of NewClue
    summary: Optional[str] = None
    # contact info (populated when type == "entity" and agent found it)
    nom: Optional[str] = None
    mail: Optional[str] = None
    web: Optional[str] = None
    persona_contacte: Optional[str] = None
    telefon: Optional[str] = None
    notes: Optional[str] = None
    idioma: Optional[str] = None


@dataclass
class ExtractResult:
    nom: str
    mail: str
    web: str = ""
    persona_contacte: str = ""
    telefon: str = ""
    notes: str = ""
    idioma: str = ""
    new_clues: list = field(default_factory=list)  # list of NewClue


class InvestigationAgentPort(ABC):
    @abstractmethod
    def classify(self, clue: str, top_returned: list[str]) -> ClassifyResult: pass

    @abstractmethod
    def extract(self, clue: str, summary: str = "", web: str = "") -> ExtractResult: pass
