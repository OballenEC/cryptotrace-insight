"""
CryptoTrace Insight — Interfaz principal con Streamlit.

Permite al usuario ingresar una dirección de wallet, consultar su
actividad en Ethereum y visualizar los patrones detectados.
"""

import sys
from pathlib import Path

# Añadir la raíz del proyecto al path para que los imports funcionen
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from app.processing.validator import is_valid_ethereum_address, normalize_address
from app.api.etherscan import fetch_transactions, EtherscanError
from app.processing.normalizer import normalize_ethereum_transactions
from app.graph.builder import build_graph, graph_summary
from app.heuristics.fanout import FanOutHeuristic
from app.heuristics.velocity import VelocityHeuristic
from app.heuristics.similar_amounts import SimilarAmountsHeuristic


# ============================================================
# Configuración de la página
# ============================================================
st.set_page_config(
    page_title="CryptoTrace Insight",
    page_icon="🔍",
    layout="wide",
)


# ============================================================
# Encabezado
# ============================================================
st.title("🔍 CryptoTrace Insight")
st.markdown(
    """
    **Herramienta open-source para explorar actividad blockchain.**

    Ingresa una dirección de wallet y analiza sus patrones
    transaccionales mediante grafos y heurísticas explicables.
    """
)

st.divider()


# ============================================================
# Formulario de entrada
# ============================================================
col1, col2 = st.columns([3, 1])

with col1:
    address_input = st.text_input(
        "Dirección de wallet",
        placeholder="0x...",
        help="Ingresa una dirección Ethereum (0x + 40 caracteres hex)",
    )

with col2:
    network = st.selectbox(
        "Red",
        options=["Ethereum"],
        index=0,
    )

analyze_button = st.button("🔎 Analizar", type="primary", use_container_width=True)


# ============================================================
# Lógica principal
# ============================================================
if analyze_button:
    if not address_input:
        st.warning("Por favor, ingresa una dirección de wallet.")
        st.stop()

    if not is_valid_ethereum_address(address_input):
        st.error(
            "La dirección no tiene un formato válido. "
            "Debe empezar con `0x` seguido de 40 caracteres hexadecimales."
        )
        st.stop()

    address = normalize_address(address_input)

    with st.spinner("Consultando transacciones en Etherscan..."):
        try:
            raw_txs = fetch_transactions(address, max_results=100)
        except EtherscanError as e:
            st.error(f"Error al consultar Etherscan: {e}")
            st.stop()

    if not raw_txs:
        st.info("Esta dirección no tiene transacciones registradas.")
        st.stop()

    with st.spinner("Normalizando transacciones..."):
        transactions = normalize_ethereum_transactions(raw_txs, address)

    with st.spinner("Construyendo grafo de transacciones..."):
        graph = build_graph(transactions)
        summary = graph_summary(graph)

    with st.spinner("Ejecutando heurísticas..."):
        heuristics = [
            FanOutHeuristic(),
            VelocityHeuristic(),
            SimilarAmountsHeuristic(),
        ]
        all_findings = []
        for h in heuristics:
            all_findings.extend(h.analyze(graph, address))

    st.divider()
    st.subheader("📊 Resumen de la investigación")

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("Transacciones", len(transactions))
    metric_col2.metric("Direcciones únicas", summary["nodes"])
    metric_col3.metric("Relaciones", summary["edges"])
    metric_col4.metric("Hallazgos", len(all_findings))

    st.markdown(f"**Dirección analizada:** `{address}`")
    st.markdown(f"**Red:** {network}")

    st.divider()

    st.subheader("🔍 Hallazgos")

    if not all_findings:
        st.info(
            "No se detectaron patrones anómalos con las heurísticas actuales. "
            "Esto no significa que la dirección sea segura; simplemente no "
            "coincide con los patrones que buscamos."
        )
    else:
        for finding in all_findings:
            with st.expander(
                f"⚠️ {finding.rule_name} — {finding.observed_value} observaciones",
                expanded=True,
            ):
                st.markdown(f"**ID:** `{finding.rule_id}`")
                st.markdown(f"**Explicación:** {finding.explanation}")
                st.markdown(f"**Limitación:** {finding.limitacion}")
                if finding.related_transactions:
                    st.markdown(
                        f"**Transacciones relacionadas:** "
                        f"{len(finding.related_transactions)} hashes"
                    )
                    with st.expander("Ver hashes"):
                        for h in finding.related_transactions:
                            st.code(h, language=None)

    st.divider()
    st.caption(
        "CryptoTrace Insight — GOYA HACK 2026 | "
        "Los patrones detectados no constituyen evidencia de actividad ilícita."
    )