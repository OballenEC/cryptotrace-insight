"""
Heurística: Fan-out Pattern.

Detecta direcciones que envían fondos a muchos destinatarios únicos.
"""

import networkx as nx

from app.heuristics.base import Heuristic
from app.models.finding import Finding


FANOUT_THRESHOLD = 5


class FanOutHeuristic(Heuristic):
    """Detecta patrones de fan-out."""

    @property
    def rule_id(self) -> str:
        return "FANOUT_01"

    @property
    def rule_name(self) -> str:
        return "Fan-out Pattern"

    def analyze(self, graph: nx.DiGraph, analyzed_address: str) -> list:
        if analyzed_address not in graph:
            return []

        successors = list(graph.successors(analyzed_address))
        num_recipients = len(successors)

        if num_recipients < FANOUT_THRESHOLD:
            return []

        related_hashes = []
        timestamps = []
        total_amount = 0.0

        for recipient in successors:
            edge_data = graph[analyzed_address][recipient]
            related_hashes.extend(edge_data.get("tx_hashes", []))
            timestamps.extend(edge_data.get("timestamps", []))
            total_amount += edge_data.get("total_amount", 0.0)

        if timestamps:
            period_start = min(timestamps).isoformat()
            period_end = max(timestamps).isoformat()
        else:
            period_start = "unknown"
            period_end = "unknown"

        return [
            Finding(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                address=analyzed_address,
                network="ethereum",
                period_start=period_start,
                period_end=period_end,
                observed_value=num_recipients,
                threshold=FANOUT_THRESHOLD,
                related_transactions=related_hashes[:20],
                explanation=(
                    f"La dirección envió fondos a {num_recipients} "
                    f"destinatarios únicos, superando el umbral de "
                    f"{FANOUT_THRESHOLD}. Monto total distribuido: "
                    f"{total_amount:.6f} ETH."
                ),
                limitation=(
                    "Este patrón también ocurre en pagos legítimos, "
                    "distribuciones de airdrops o actividades automatizadas."
                ),
            )
        ]