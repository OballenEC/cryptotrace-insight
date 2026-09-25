"""
Debug del flujo de Ethereum usando el dataset offline.
"""

import json

from app.processing.normalizer import normalize_ethereum_transactions
from app.graph.builder import build_graph, graph_summary
from app.heuristics.fanout import FanOutHeuristic
from app.heuristics.velocity import VelocityHeuristic
from app.heuristics.similar_amounts import SimilarAmountsHeuristic


def main():
    address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

    print("[1] Cargando dataset offline...")
    with open("data/sample_ethereum_transactions.json", "r") as f:
        raw = json.load(f)
    print(f"    OK: {len(raw)} transacciones crudas")

    print("[2] Normalizando...")
    txs = normalize_ethereum_transactions(raw, address)
    print(f"    OK: {len(txs)} transacciones normalizadas")

    print("[3] Construyendo grafo...")
    graph = build_graph(txs)
    summary = graph_summary(graph)
    print(f"    OK: {summary}")

    print("[4] Ejecutando heurísticas...")
    for h in [FanOutHeuristic(), VelocityHeuristic(), SimilarAmountsHeuristic()]:
        findings = h.analyze(graph, address)
        print(f"    {h.rule_name}: {len(findings)} hallazgos")

    print()
    print("TODO EL FLUJO FUNCIONA CON DATOS OFFLINE")


if __name__ == "__main__":
    main()