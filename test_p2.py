"""
Script de prueba para P2: Graph Builder.
"""

from app.api.etherscan import fetch_transactions
from app.processing.normalizer import normalize_ethereum_transactions
from app.graph.builder import build_graph, graph_summary


def main():
    address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    print("Consultando...")

    raw = fetch_transactions(address, max_results=10)
    txs = normalize_ethereum_transactions(raw, address)

    print(f"Transacciones: {len(txs)}")

    graph = build_graph(txs)
    summary = graph_summary(graph)

    print()
    print("Resumen del grafo:")
    print(f"  Nodos (direcciones unicas): {summary['nodes']}")
    print(f"  Aristas (relaciones): {summary['edges']}")
    print(f"  Total de transacciones: {summary['total_transactions']}")

    print()
    print("Ejemplo de aristas:")
    for u, v, data in list(graph.edges(data=True))[:3]:
        print(f"  {u[:10]}... -> {v[:10]}...")
        print(f"    Monto total: {data['total_amount']:.6f} ETH")
        print(f"    Transacciones: {data['tx_count']}")


if __name__ == "__main__":
    main()