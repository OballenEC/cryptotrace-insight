"""
Modelo de hallazgo (Finding).

Representa el resultado estructurado de una heurística.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Finding:
    """
    Resultado de una heurística aplicada al grafo.

    Attributes:
        rule_id: Identificador corto de la regla (ej. "FANOUT_01").
        rule_name: Nombre legible (ej. "Fan-out Pattern").
        address: Dirección analizada que disparó el hallazgo.
        network: Red de origen (ethereum, stellar).
        period_start: Inicio del período analizado.
        period_end: Fin del período analizado.
        observed_value: Valor observado (ej. número de destinatarios).
        threshold: Umbral que se superó para disparar el hallazgo.
        related_transactions: Lista de hashes de transacciones involucradas.
        explanation: Explicación legible del hallazgo.
        limitation: Limitación o falso positivo posible.
    """

    rule_id: str
    rule_name: str
    address: str
    network: str
    period_start: str
    period_end: str
    observed_value: float
    threshold: float
    related_transactions: list[str] = field(default_factory=list)
    explanation: str = ""
    limitation: str = ""

    def summary(self) -> str:
        """Resumen en una línea."""
        return (
            f"[{self.rule_id}] {self.rule_name} | "
            f"{self.observed_value} (umbral: {self.threshold})"
        )