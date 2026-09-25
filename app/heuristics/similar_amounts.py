"""
Heurística: Similar Amounts Pattern.

Detecta múltiples transferencias con montos iguales o muy similares
dentro de un período corto.

Este patrón es característico del "structuring" (dividir fondos en
cantidades similares), aunque también ocurre en pagos recurrentes.
"""

import networkx as nx

from app.heuristics.base import Heuristic
from app.models.finding import Finding


SIMILAR_AMOUNT_THRESHOLD = 4
SIMILAR_AMOUNT_TOLERANCE = 0.05  # 5% de diferencia máxima


class SimilarAmountsHeuristic(Heuristic):
    """Detecta múltiples montos similares."""

    @property
    def rule_id(self) -> str:
        return "SIMILAR_01"

    @property
    def rule_name(self) -> str:
        return "Similar Amounts Pattern"

    def analyze(self, graph: nx.DiGraph, analyzed_address: str) -> list:
        if analyzed_address not in graph:
            return []

        edges_info = []
        for _, recipient, data in graph.out_edges(analyzed_address, data=True):
            amount = data.get("total_amount", 0.0)
            tx_count = data.get("tx_count", 1)
            hashes = data.get("tx_hashes", [])
            edges_info.append({
                "recipient": recipient,
                "amount": amount,
                "tx_count": tx_count,
                "hashes": hashes,
            })

        if len(edges_info) < SIMILAR_AMOUNT_THRESHOLD:
            return []

        groups = self._find_similar_groups(edges_info)

        if not groups:
            return []

        largest_group = max(groups, key=len)

        if len(largest_group) < SIMILAR_AMOUNT_THRESHOLD:
            return []

        related_hashes = []
        for item in largest_group:
            related_hashes.extend(item["hashes"])

        example_amount = largest_group[0]["amount"]

        return [
            Finding(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                address=analyzed_address,
                network="ethereum",
                period_start="n/a",
                period_end="n/a",
                observed_value=len(largest_group),
                threshold=SIMILAR_AMOUNT_THRESHOLD,
                related_transactions=related_hashes[:20],
                explanation=(
                    f"Se detectaron {len(largest_group)} transferencias "
                    f"con montos similares (ejemplo: ~{example_amount:.6f} ETH, "
                    f"tolerancia {SIMILAR_AMOUNT_TOLERANCE * 100:.0f}%). "
                    f"Este patrón es característico del 'structuring'."
                ),
                limitation=(
                    "Este patrón también puede ocurrir en pagos recurrentes, "
                    "suscripciones o distribuciones programadas."
                ),
            )
        ]

    def _find_similar_groups(self, edges_info: list) -> list:
        """Agrupa aristas por montos similares."""
        groups = []
        used = [False] * len(edges_info)

        for i, item_i in enumerate(edges_info):
            if used[i]:
                continue

            group = [item_i]
            used[i] = True

            for j, item_j in enumerate(edges_info):
                if used[j] or i == j:
                    continue

                amount_i = item_i["amount"]
                amount_j = item_j["amount"]

                if amount_i == 0:
                    continue

                diff = abs(amount_i - amount_j) / amount_i
                if diff <= SIMILAR_AMOUNT_TOLERANCE:
                    group.append(item_j)
                    used[j] = True

            if len(group) >= 2:
                groups.append(group)

        return groups