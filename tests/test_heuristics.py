"""
Tests para las heurísticas.
"""

from datetime import datetime, timedelta

import networkx as nx

from app.models.transaction import Transaction
from app.heuristics.fanout import FanOutHeuristic
from app.heuristics.velocity import VelocityHeuristic
from app.heuristics.similar_amounts import SimilarAmountsHeuristic


def make_tx(sender, receiver, amount, minutes_offset=0):
    base = datetime(2024, 1, 1, 12, 0, 0)
    return Transaction(
        sender=sender,
        receiver=receiver,
        amount=amount,
        timestamp=base + timedelta(minutes=minutes_offset),
        tx_hash=f"0xhash{minutes_offset}",
        asset="ETH",
        network="ethereum",
        direction="outgoing",
    )


def build_test_graph(transactions):
    g = nx.DiGraph()
    for tx in transactions:
        if not g.has_edge(tx.sender, tx.receiver):
            g.add_edge(
                tx.sender,
                tx.receiver,
                total_amount=0.0,
                tx_count=0,
                tx_hashes=[],
                timestamps=[],
            )
        g[tx.sender][tx.receiver]["total_amount"] += tx.amount
        g[tx.sender][tx.receiver]["tx_count"] += 1
        g[tx.sender][tx.receiver]["tx_hashes"].append(tx.tx_hash)
        g[tx.sender][tx.receiver]["timestamps"].append(tx.timestamp)
    return g


def test_fanout_positive():
    address = "0xanalysis"
    txs = [make_tx(address, f"0xrecipient{i}", 0.1, i) for i in range(6)]
    graph = build_test_graph(txs)
    findings = FanOutHeuristic().analyze(graph, address)
    assert len(findings) == 1
    assert findings[0].observed_value == 6


def test_fanout_negative():
    address = "0xanalysis"
    txs = [make_tx(address, f"0xrecipient{i}", 0.1, i) for i in range(2)]
    graph = build_test_graph(txs)
    findings = FanOutHeuristic().analyze(graph, address)
    assert len(findings) == 0


def test_velocity_positive():
    address = "0xanalysis"
    txs = [make_tx(address, f"0xr{i}", 0.1, i) for i in range(6)]
    graph = build_test_graph(txs)
    findings = VelocityHeuristic().analyze(graph, address)
    assert len(findings) == 1
    assert findings[0].observed_value >= 5


def test_velocity_negative():
    address = "0xanalysis"
    txs = [make_tx(address, f"0xr{i}", 0.1, i) for i in range(4)]
    graph = build_test_graph(txs)
    findings = VelocityHeuristic().analyze(graph, address)
    assert len(findings) == 0


def test_similar_amounts_positive():
    address = "0xanalysis"
    txs = [
        make_tx(address, f"0xr{i}", 1.0 + (i * 0.001), i)
        for i in range(5)
    ]
    graph = build_test_graph(txs)
    findings = SimilarAmountsHeuristic().analyze(graph, address)
    assert len(findings) == 1
    assert findings[0].observed_value >= 4


def test_similar_amounts_negative():
    address = "0xanalysis"
    txs = [
        make_tx(address, "0xr1", 0.01, 0),
        make_tx(address, "0xr2", 1.0, 1),
        make_tx(address, "0xr3", 5.0, 2),
        make_tx(address, "0xr4", 10.0, 3),
    ]
    graph = build_test_graph(txs)
    findings = SimilarAmountsHeuristic().analyze(graph, address)
    assert len(findings) == 0