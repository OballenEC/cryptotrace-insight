"""
Script de prueba para P3: Heurística Fan-out.
"""

from app.api.etherscan import fetch_transactions
from app.processing.normalizer import normalize_ethereum_transactions
from app.graph.builder import build_graph
from app.heuristics.fanout import FanOutHeuristic


def main():
    address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    print("Consultando...")

    raw = fetch_transactions(address, max_results=50)
    txs = normalize_ethereum_transactions(raw, address)
    print(f"Transacciones: {len(txs)}")

    graph = build_graph(txs)
    print(f"Nodos: {graph.number_of_nodes()}, Aristas: {graph.number_of_edges()}")
    print()

    heuristic = FanOutHeuristic()
    findings = heuristic.analyze(graph, address)

    print(f"Hallazgos: {len(findings)}")
    print()

    for finding in findings:
        print(f"  [{finding.rule_id}] {finding.rule_name}")
        print(f"  Dirección: {finding.address}")
        print(f"  Observado: {finding.observed_value}")
        print(f"  Explicación: {finding.explanation}")
        print(f"  Limitación: {finding.limitacion}")
        print()


if __name__ == "__main__":
    main()