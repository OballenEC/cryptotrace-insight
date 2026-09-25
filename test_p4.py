"""
Script de prueba para P4: Heurística Velocity.
"""

from app.api.etherscan import fetch_transactions
from app.processing.normalizer import normalize_ethereum_transactions
from app.graph.builder import build_graph
from app.heuristics.fanout import FanOutHeuristic
from app.heuristics.velocity import VelocityHeuristic


def main():
    address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    print("Consultando...")

    raw = fetch_transactions(address, max_results=100)
    txs = normalize_ethereum_transactions(raw, address)
    print(f"Transacciones: {len(txs)}")

    graph = build_graph(txs)
    print(f"Nodos: {graph.number_of_nodes()}, Aristas: {graph.number_of_edges()}")
    print()

    print("=== Fan-out ===")
    fanout = FanOutHeuristic()
    findings_fanout = fanout.analyze(graph, address)
    print(f"Hallazgos: {len(findings_fanout)}")
    for f in findings_fanout:
        print(f"  {f.summary()}")
    print()

    print("=== Velocity ===")
    velocity = VelocityHeuristic()
    findings_velocity = velocity.analyze(graph, address)
    print(f"Hallazgos: {len(findings_velocity)}")
    for f in findings_velocity:
        print(f"  [{f.rule_id}] {f.rule_name}")
        print(f"  Observado: {f.observed_value} transacciones")
        print(f"  Período: {f.period_start} → {f.period_end}")
        print(f"  Explicación: {f.explanation}")
        print(f"  Limitación: {f.limitacion}")
        print()


if __name__ == "__main__":
    main()