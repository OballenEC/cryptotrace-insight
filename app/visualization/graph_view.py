"""
Visualización interactiva del grafo con PyVis.

Convierte un grafo de NetworkX en un HTML interactivo que se
puede incrustar en Streamlit.
"""

import networkx as nx
from pyvis.network import Network


def render_graph_html(
    graph: nx.DiGraph,
    analyzed_address: str,
    highlight_addresses: list = None,
) -> str:
    """
    Genera el HTML de un grafo interactivo.

    Args:
        graph: Grafo dirigido de NetworkX.
        analyzed_address: Dirección analizada (se resalta en rojo).
        highlight_addresses: Lista opcional de direcciones a resaltar.

    Returns:
        String con el HTML del grafo.
    """
    if highlight_addresses is None:
        highlight_addresses = []

    net = Network(
        height="600px",
        width="100%",
        directed=True,
        bgcolor="#0E1117",
        font_color="#FAFAFA",
    )

    net.set_options("""
    {
      "nodes": {
        "font": {"size": 14, "color": "#FAFAFA"},
        "borderWidth": 2
      },
      "edges": {
        "color": {"inherit": false, "color": "#4A90E2"},
        "smooth": {"type": "curvedCW", "roundness": 0.2},
        "arrows": {"to": {"enabled": true, "scaleFactor": 0.8}}
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)

    for node in graph.nodes():
        if node == analyzed_address:
            color = "#FF4B4B"
            size = 30
            label = "ANALIZADA"
        elif node in highlight_addresses:
            color = "#FFA500"
            size = 22
            label = node[:8] + "..."
        else:
            color = "#4A90E2"
            size = 15
            label = node[:8] + "..."

        net.add_node(
            node,
            label=label,
            title=f"{node}\n({graph.degree(node)} conexiones)",
            color=color,
            size=size,
        )

    for u, v, data in graph.edges(data=True):
        amount = data.get("total_amount", 0.0)
        tx_count = data.get("tx_count", 1)
        width = min(1 + tx_count * 0.5, 5)

        net.add_edge(
            u,
            v,
            title=f"{amount:.6f} ETH\n{tx_count} transacciones",
            width=width,
            value=tx_count,
        )

    html = net.generate_html(notebook=False)
    return html