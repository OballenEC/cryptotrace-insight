"""
Constructor de grafos de transacciones.

Convierte una lista de Transaction en un grafo dirigido (DiGraph)
donde los nodos son direcciones y las aristas son transacciones.
"""

import networkx as nx

from app.models.transaction import Transaction


def build_graph(transactions: list[Transaction]) -> nx.DiGraph:
    """
    Construye un grafo dirigido a partir de transacciones normalizadas.
    """
    graph = nx.DiGraph()

    for tx in transactions:
        sender = tx.sender
        receiver = tx.receiver

        graph.add_node(sender, address=sender)
        graph.add_node(receiver, address=receiver)

        if graph.has_edge(sender, receiver):
            graph[sender][receiver]["total_amount"] += tx.amount
            graph[sender][receiver]["tx_count"] += 1
            graph[sender][receiver]["tx_hashes"].append(tx.tx_hash)
            graph[sender][receiver]["timestamps"].append(tx.timestamp)
        else:
            graph.add_edge(
                sender,
                receiver,
                total_amount=tx.amount,
                tx_count=1,
                tx_hashes=[tx.tx_hash],
                timestamps=[tx.timestamp],
            )

    return graph


def graph_summary(graph: nx.DiGraph) -> dict:
    """
    Devuelve un resumen del grafo.
    """
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "total_transactions": sum(
            data.get("tx_count", 0) for _, _, data in graph.edges(data=True)
        ),
    }