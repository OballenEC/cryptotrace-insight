"""
Script de prueba para P5: Heurística Similar Amounts.
Ejecuta las 3 heurísticas y muestra todos los hallazgos.
"""

from app.api.etherscan import fetch_transactions
from app.processing.normalizer import normalize_ethereum_transactions
from app.graph.builder import build_graph
from app.heuristics.fanout import FanOutHeuristic
from app.heuristics.velocity import VelocityHeuristic
from app.heuristics.similar_amounts import SimilarAmountsHeuristic


def main():
    address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    print("Consultando...")

    raw = fetch_transactions(address, max_results=100)
    txs = normalize_ethereum_transactions(raw, address)
    print(f"Transacciones: {len(txs)}")

    graph = build_graph(txs)
    print(f"Nodos: {graph.number_of_nodes()}, Aristas: {graph.number_of_edges()}")
    print()

    heuristics = [
        FanOutHeuristic(),
        VelocityHeuristic(),
        SimilarAmountsHeuristic(),
    ]

    total_findings = 0
    for h in heuristics:
        findings = h.analyze(graph, address)
        print(f"=== {h.rule_name} ===")
        print(f"Hallazgos: {len(findings)}")
        for f in findings:
            total_findings += 1
            print(f"  [{f.rule_id}] Observado: {f.observed_value}")
            print(f"  {f.explanation}")
            print(f"  Limitación: {f.limitacion}")
        print()

    print(f"TOTAL DE HALLAZGOS: {total_findings}")


if __name__ == "__main__":
    main()