"""
Heurística: High Velocity Pattern.

Detecta ráfagas de transacciones en un intervalo corto de tiempo.
"""

from datetime import timedelta

import networkx as nx

from app.heuristics.base import Heuristic
from app.models.finding import Finding


VELOCITY_THRESHOLD_COUNT = 5
VELOCITY_THRESHOLD_MINUTES = 10


class VelocityHeuristic(Heuristic):
    """Detecta ráfagas de transacciones en poco tiempo."""

    @property
    def rule_id(self) -> str:
        return "VELOCITY_01"

    @property
    def rule_name(self) -> str:
        return "High Velocity Pattern"

    def analyze(self, graph: nx.DiGraph, analyzed_address: str) -> list:
        if analyzed_address not in graph:
            return []

        timestamps = []
        related_hashes = []

        for _, _, data in graph.out_edges(analyzed_address, data=True):
            timestamps.extend(data.get("timestamps", []))
            related_hashes.extend(data.get("tx_hashes", []))

        for _, _, data in graph.in_edges(analyzed_address, data=True):
            timestamps.extend(data.get("timestamps", []))
            related_hashes.extend(data.get("tx_hashes", []))

        if len(timestamps) < VELOCITY_THRESHOLD_COUNT:
            return []

        timestamps.sort()
        window = timedelta(minutes=VELOCITY_THRESHOLD_MINUTES)

        max_count = 0
        best_start = None
        best_end = None

        for i in range(len(timestamps)):
            start = timestamps[i]
            end = start + window
            count = 0
            for j in range(i, len(timestamps)):
                if timestamps[j] <= end:
                    count += 1
                else:
                    break
            if count > max_count:
                max_count = count
                best_start = start
                best_end = timestamps[i + count - 1]

        if max_count < VELOCITY_THRESHOLD_COUNT:
            return []

        return [
            Finding(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                address=analyzed_address,
                network="ethereum",
                period_start=best_start.isoformat(),
                period_end=best_end.isoformat(),
                observed_value=max_count,
                threshold=VELOCITY_THRESHOLD_COUNT,
                related_transactions=related_hashes[:20],
                explanation=(
                    f"Se detectaron {max_count} transacciones en un "
                    f"intervalo de {VELOCITY_THRESHOLD_MINUTES} minutos "
                    f"o menos. Esto indica una ráfaga de actividad "
                    f"inusualmente concentrada."
                ),
                limitation=(
                    "Este patrón también puede ocurrir en actividades "
                    "legítimas automatizadas, pagos masivos o trading."
                ),
            )
        ]