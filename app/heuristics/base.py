"""
Interfaz base para heurísticas.

Toda heurística debe implementar el método analyze().
"""

from abc import ABC, abstractmethod

import networkx as nx

from app.models.finding import Finding


class Heuristic(ABC):
    """Clase base para todas las heurísticas."""

    @property
    @abstractmethod
    def rule_id(self) -> str:
        """Identificador corto de la regla."""
        ...

    @property
    @abstractmethod
    def rule_name(self) -> str:
        """Nombre legible de la regla."""
        ...

    @abstractmethod
    def analyze(self, graph: nx.DiGraph, analyzed_address: str) -> list:
        """
        Analiza el grafo y devuelve una lista de hallazgos.
        """
        ...